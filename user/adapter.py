from allauth.account.adapter import  DefaultAccountAdapter
from allauth.account import  app_settings
from allauth.account.app_settings import EmailVerificationMethod
from allauth.utils import (
    build_absolute_uri,
)
from django.urls import reverse
from django.utils.encoding import force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.utils.translation import gettext_lazy as _

from .shortcuts import get_current_site



class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    domain = None

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(viewname = "user:account_confirm_email", args=[emailconfirmation.key], current_app="user")
        ret = build_absolute_uri(request, url)
        redirect_url=f'?redirect_url={self.domain}'
        return ret + redirect_url if self.domain else ret

    def send_confirmation_mail(self, request, emailconfirmation, signup ):
        current_site = get_current_site(request, domain=self.domain if self.domain else "")
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
        self.send_mail(email_template, emailconfirmation.email_address.email,ctx)


    def render_mail(self, template_prefix, email, context,headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"  # Main content is now text/html
        CustomDefaultAccountAdapter.domain=None
        return msg

    def format_email_subject(self, subject ):
        prefix = app_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site =  get_current_site(self.request, domain=self.domain if self.domain else "")
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_str(subject)



    def pre_login(
        self,
        request,
        user,
        *,
        email_verification,
        signal_kwargs,
        email,
        signup,
        redirect_url
    ):
        from allauth.account.utils import has_verified_email, send_email_confirmation

        CustomDefaultAccountAdapter.domain = redirect_url

        if not user.is_active:
            return self.respond_user_inactive(request, user)
        
        if email_verification == EmailVerificationMethod.NONE:
            pass
        elif email_verification == EmailVerificationMethod.OPTIONAL:
            # In case of OPTIONAL verification: send on signup.
            if not has_verified_email(user, email) and signup:
                send_email_confirmation(request, user, signup=signup, email=email)
        elif email_verification == EmailVerificationMethod.MANDATORY:
            if not has_verified_email(user, email):
                send_email_confirmation(request, user, signup=signup, email=email)
                return self.respond_email_verification_sent(request, user)
