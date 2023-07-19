from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    ResendEmailVerificationSerializer,
)
from rest_framework import serializers
from helper.choices import Sex

from user.forms import AllAuthPasswordResetForm
from user.models import User


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True, allow_blank=True)
    email = None
    pass


class CustomPasswordResetSerializer(PasswordResetSerializer):
    redirect = serializers.CharField(required=False)

    @property
    def password_reset_form_class(self):
        if "allauth" in settings.INSTALLED_APPS:
            return AllAuthPasswordResetForm
        else:
            return PasswordResetForm

    def get_email_options(self):
        return {"email_subject": "Reset your password"}

    def save(self):
        if "allauth" in settings.INSTALLED_APPS:
            from allauth.account.forms import default_token_generator
        else:
            from django.contrib.auth.tokens import default_token_generator

        request = self.context.get("request")

        # Set some values to trigger the send_email method.

        opts = {
            "use_https": request.is_secure(),
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
            "token_generator": default_token_generator,
        }

        opts.update(self.get_email_options())

        return self.reset_form.save(**opts)


class PasswordTokenSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1)
    uidb64 = serializers.CharField(min_length=1)

    class Meta:
        fields = ["token", "uidb64"]

    def validate(self, attrs):
        try:
            token = attrs.get("token", "")
            uidb64 = attrs.get("uidb64", "")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if "allauth" in settings.INSTALLED_APPS:
                from allauth.account.forms import default_token_generator
            else:
                from django.contrib.auth.tokens import default_token_generator

            if not default_token_generator.check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    middle_name = serializers.CharField(max_length=150, required=False)
    gender = serializers.ChoiceField(choices=Sex.choices, default=Sex.MALE)
    redirect = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.middle_name = self.validated_data.get("middle_name", "")
        user.gender = self.validated_data.get("gender", "")
        user.save()
        pass

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["first_name"] = self.validated_data.get("first_name", "")
        data["last_name"] = self.validated_data.get("last_name", "")
        return data


class CustomResendEmailVerificationSerializer(ResendEmailVerificationSerializer):
    redirect = serializers.CharField(required=False)
