from allauth.account.adapter import get_adapter
from allauth.account.utils import user_email, user_pk_to_url_str
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import signals
from django.contrib import messages
from django.contrib.sites.models import Site


def perform_login(
    request,
    user,
    email_verification,
    redirect_url=None,
    signal_kwargs=None,
    signup=False,
    email=None,
):
    """
    Keyword arguments:

    signup -- Indicates whether or not sending the
    email is essential (during signup), or if it can be skipped (e.g. in
    case email verification is optional and we are only logging in).
    """
    # Local users are stopped due to form validation checking
    # is_active, yet, adapter methods could toy with is_active in a
    # `user_signed_up` signal. Furthermore, social users should be
    # stopped anyway.
    adapter = get_adapter(request)
    try:
        hook_kwargs = dict(
            email_verification=email_verification,
            redirect_url=redirect_url,
            signal_kwargs=signal_kwargs,
            signup=signup,
            email=email,
        )
        response = adapter.pre_login(request, user, **hook_kwargs)
        if response:
            return response
        adapter.login(request, user)
        response = adapter.post_login(request, user, **hook_kwargs)
        if response:
            return response
    except ImmediateHttpResponse as e:
        response = e.response
    return response


def complete_signup(request, user, email_verification, success_url, signal_kwargs=None):
    if signal_kwargs is None:
        signal_kwargs = {}
    signals.user_signed_up.send(
        sender=user.__class__, request=request, user=user, **signal_kwargs
    )
    return perform_login(
        request,
        user,
        email_verification=email_verification,
        signup=True,
        redirect_url=success_url,
        signal_kwargs=signal_kwargs,
    )

def send_email_confirmation(request, user, signup=False, email=None):
    """
    E-mail verification mails are sent:
    a) Explicitly: when a user signs up
    b) Implicitly: when a user attempts to log in using an unverified
    e-mail while EMAIL_VERIFICATION is mandatory.

    Especially in case of b), we want to limit the number of mails
    sent (consider a user retrying a few times), which is why there is
    a cooldown period before sending a new mail. This cooldown period
    can be configured in ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN setting.
    """
    from allauth.account.models import EmailAddress

    adapter = get_adapter(request)

    if not email:
        email = user_email(user)
    if email:
        try:
            email_address = EmailAddress.objects.get_for_user(user, email)
            if not email_address.verified:
                send_email = adapter.should_send_confirmation_mail(
                    request, email_address
                )
                if send_email:
                    email_address.send_confirmation(request, signup=signup)
            else:
                send_email = False
        except EmailAddress.DoesNotExist:
            send_email = True
            email_address = EmailAddress.objects.add_email(
                request, user, email, signup=signup, confirm=True
            )
            assert email_address
        # At this point, if we were supposed to send an email we have sent it.
        if send_email:
            adapter.add_message(
                request,
                messages.INFO,
                "account/messages/email_confirmation_sent.txt",
                {"email": email},
            )
    if signup:
        adapter.stash_user(request, user_pk_to_url_str(user))


