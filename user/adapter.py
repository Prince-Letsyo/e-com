from allauth.account.adapter import DefaultAccountAdapter
from allauth.account import app_settings
from django.urls import reverse
from django.utils.encoding import force_str
from helper.utils import get_domain
from user.models import SiteOwner
from allauth.account.adapter import build_absolute_uri


class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    def _get_current_site(self):
        return get_domain(self.request, site_owner_model=SiteOwner)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = self._get_current_site()
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def format_email_subject(self, subject):
        prefix = app_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = self._get_current_site()
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_str(subject)

    def get_email_confirmation_url(self, request, emailconfirmation):
        public_key = request.META.get("HTTP_PUBLIC_KEY")
        secret_key = request.META.get("HTTP_SECRET_KEY")

        if public_key and secret_key:
            url = reverse(
                "user:account_confirm_email",
                current_app="user",
                args=[emailconfirmation.key],
            )
            return f"{build_absolute_uri(request, url)}?redirect={self._get_current_site().domain}"
        return super().get_email_confirmation_url(request, emailconfirmation)
