
from django.conf import settings
from django.contrib.sites.models import Site
from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.encoding import (smart_bytes)
from django.utils.http import urlsafe_base64_encode
from dj_rest_auth.app_settings import api_settings

from .shortcuts import get_current_site


if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import ResetPasswordForm as DefaultPasswordResetForm
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (
        filter_users_by_email,
        user_pk_to_url_str,
        user_username,
    )
    from allauth.utils import build_absolute_uri


def default_url_generator(request, uid, temp_key):
    path = reverse(
        'password_reset_confirm',
        args=[uid, temp_key],
    )

    if api_settings.PASSWORD_RESET_USE_SITES_DOMAIN :
        url = build_absolute_uri(None,location=path) 
    else:
        url = build_absolute_uri(request=request, location=path)

    url = url.replace('%3F', '?')

    return url


class AllAuthPasswordResetForm(DefaultPasswordResetForm):
    
    def __init__(self, *args, **kwargs):
        super(AllAuthPasswordResetForm,self).__init__(*args, **kwargs)
        self.fields['site']=forms.ChoiceField(required=False,
            choices=[*[( obj.domain,obj.name) for obj in Site.objects.all()]])

    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request, self.cleaned_data['site'])
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)
        for user in self.users:

            temp_key = token_generator.make_token(user)
            uid=urlsafe_base64_encode(smart_bytes(user_pk_to_url_str(user)))
            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            url_generator = kwargs.get('url_generator', default_url_generator)
            url = url_generator(request= request, uid=uid, temp_key=temp_key)
            redirect_url=f'?redirect_url={current_site.domain}'
            url=url+redirect_url
            
            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context,domain=current_site.domain
            )
        return {"email":self.cleaned_data['email'], "token": temp_key, "uid": uid}
