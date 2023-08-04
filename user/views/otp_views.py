from django.contrib.auth import BACKEND_SESSION_KEY, login as auth_login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django_otp.forms import OTPTokenForm


class HasVerifiedOTP(UserPassesTestMixin):
    login_url = reverse_lazy("account_login")
    if_configured = False

    def test_func(self):
        return not self.request.user.otp_device

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            path = reverse("user_profile:profile")
            return redirect_to_login(
                path,
                self.login_url,
                self.get_redirect_field_name(),
            )
        return super().dispatch(request, *args, **kwargs)


class OTPCheckPointView(LoginRequiredMixin, HasVerifiedOTP, FormView):
    template_name = "user/otp_check_point.html"
    form_class = OTPTokenForm
    if_configured = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        if not hasattr(user, "backend"):
            user.backend = self.request.session[BACKEND_SESSION_KEY]
            auth_login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = (
            self.request.GET.get("next") if self.success_url is None else "/"
        )
        return super().get_success_url()
