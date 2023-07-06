from allauth.account.adapter import  DefaultAccountAdapter
from allauth.account import  app_settings
from django.utils.encoding import force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

from .shortcuts import get_current_site


class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context,domain ):
        msg = self.render_mail(template_prefix, email, context,domain=domain)
        msg.send()


    def send_confirmation_mail(self, request, emailconfirmation, signup , domain):
        current_site = get_current_site(request, domain)
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
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx,domain)


    def render_mail(self, template_prefix, email, context, domain,headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject,domain)

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
        return msg

    def format_email_subject(self, subject,domain ):
        prefix = app_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = get_current_site(self.request, domain)
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_str(subject)


    