from typing import Any
from allauth.account import app_settings as allauth_account_settings
from allauth.account.models import EmailAddress
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from dj_rest_auth.views import api_settings
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
    UserDetailsView,
)
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ResendEmailVerificationView,
)
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.jwt_auth import get_refresh_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenVerifyView
from helper import CustomRedirect
from helper.permissions import IsVerified
from user.serializers.user_serializers import (
    LogInResponseWithExpirationSerializer,
    LogInResponseWithoutExpirationSerializer,
)

from user.utils import complete_signup
from user.serializers import (
    PasswordTokenSerializer,
    CustomResendEmailVerificationSerializer,
)
from user.models import User

try:
    from allauth.account.adapter import get_adapter
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


class CustomLoginView(LoginView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """

    @swagger_auto_schema(
        responses={
            200: LogInResponseWithExpirationSerializer
            if api_settings.JWT_AUTH_RETURN_EXPIRATION
            else LogInResponseWithoutExpirationSerializer
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


log_out_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="CustomLogout",
    properties={
        "refresh": openapi.Schema(
            title="Refresh token",
            type=openapi.TYPE_STRING,
        ),
    },
    required=["refresh"],
)

log_out_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="CustomLogout",
    properties={
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING, default="Successfully logged out."
        ),
    },
)


class CustomLogoutView(LogoutView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (IsVerified,)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=log_out_request, responses={200: log_out_response}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


password_change_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="CustomPasswordChange",
    properties={
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING, default="New password has been saved."
        ),
    },
)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    @swagger_auto_schema(responses={200: password_change_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


password_reset_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title=" CustomPasswordReset",
    properties={
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING, default="Password reset e-mail has been sent."
        ),
    },
)


class CustomPasswordResetView(PasswordResetView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    @swagger_auto_schema(responses={200: password_reset_response})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            data,
            status=status.HTTP_200_OK,
        )


password_reset_confirm_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title=" CustomPasswordResetConfirm",
    properties={
        "detail": openapi.Schema(
            type=openapi.TYPE_STRING,
            default="Password has been reset with the new password.",
        ),
    },
)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """

    @swagger_auto_schema(responses={200: password_reset_confirm_response})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = PasswordTokenSerializer

    @swagger_auto_schema(
        auto_schema=None,
    )
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url", "")
        current_site = get_current_site(request)
        valued = "?token_valid=False"
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if "allauth" in settings.INSTALLED_APPS:
                from allauth.account.forms import default_token_generator
            else:
                from django.contrib.auth.tokens import default_token_generator

            if not default_token_generator.check_token(user, token):
                if redirect_url and len(redirect_url) > 3:
                    return CustomRedirect(f"{redirect_url}{valued}")
                else:
                    return CustomRedirect(f"{current_site}{valued}")
            else:
                valued = f"?token_valid=True&message=Credential_valid&uidb64={uidb64}&token={token}"
                if redirect_url and len(redirect_url) > 3:
                    return CustomRedirect(f"{redirect_url}{valued}")
                else:
                    return CustomRedirect(f"{current_site}{valued}")

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "success": True,
                "token": serializer.data["token"],
                "uidb64": serializer.data["uidb64"],
            },
            status=status.HTTP_200_OK,
        )


class CustomUserDetailsView(UserDetailsView):
    permission_classes = (IsVerified,)
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    pass


class CustomRegisterView(RegisterView):
    @swagger_auto_schema(
        responses={201: LogInResponseWithoutExpirationSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if (
            allauth_account_settings.EMAIL_VERIFICATION
            != allauth_account_settings.EmailVerificationMethod.MANDATORY
        ):
            if api_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif not api_settings.SESSION_LOGIN:
                # Session authentication isn't active either, so this has to be
                #  token authentication
                api_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request._request,
            user,
            allauth_account_settings.EMAIL_VERIFICATION,
            serializer.validated_data.get("redirect"),
        )
        return user


class CustomVerifyEmailView(VerifyEmailView):
    @swagger_auto_schema(
        auto_schema=None,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomInVerifyEmailView(CustomVerifyEmailView):
    def __init__(self, request, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.request = request
        super(VerifyEmailView, self).__init__(**kwargs)


class ConfirmEmailAPIView(GenericAPIView):
    @swagger_auto_schema(
        auto_schema=None,
    )
    def get(self, request, key, *args, **kwargs):
        verify_email = CustomInVerifyEmailView(request, **kwargs)
        path = reverse(viewname="user:rest_verify_email", current_app="user")

        request.path = path
        request.data["key"] = key
        request.method = "POST"
        response = verify_email.post(request, *args, **kwargs)
        redirect_url = request.GET.get("redirect_url", "")
        valued = "?valid_email=False"

        if response.status_code == 200:
            valued = "?valid_email=True"
            return CustomRedirect(f"{redirect_url}{valued}")
        else:
            return CustomRedirect(f"{redirect_url}{valued}")


verify_email_resend = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title=" CustomResendEmailVerificationView",
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING, default="Ok"),
    },
)


class CustomResendEmailVerificationView(ResendEmailVerificationView):
    serializer_class = CustomResendEmailVerificationSerializer

    @swagger_auto_schema(
        responses={200: verify_email_resend},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        site = request.data.pop("redirect")

        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email and not email.verified:
            adapter = get_adapter(request)
            adapter.__class__.domain = site
            email.send_confirmation(request)

        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


verify_token = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title=" CustomResendEmailVerificationView",
    properties={
        "data": openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
    },
)


class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={200: verify_token},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


refresh_token = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title=" CustomResendEmailVerificationView",
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access": openapi.Schema(
                    title="Access token",
                    type=openapi.TYPE_STRING,
                ),
                "access_expiration": openapi.Schema(
                    title="Access expiration",
                    type=openapi.FORMAT_DATETIME,
                )
                if api_settings.JWT_AUTH_RETURN_EXPIRATION
                else None,
            },
        ),
    },
)


class CustomRefreshToken(get_refresh_view()):
    @swagger_auto_schema(
        responses={200: refresh_token},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
