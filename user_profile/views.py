from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from user.models.user import SiteOwnerProfile
from django.contrib.sites.models import Site
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import redirect
from django_otp import user_has_device


class IndexTemplateView(TemplateView):
    template_name = "user_profile/index.html"
    extra_context = {"obj": "gfhldfjkg"}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteOwnerProfilePermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == "SITEOWNER" or not self.has_permission():
            return redirect("user_profile:index")

        return super(SiteOwnerProfilePermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class OtpRequired(UserPassesTestMixin):
    login_url = reverse_lazy("account_login")
    if_configured = False

    def test_func(self):
        return self.request.user.is_verified() or (
            self.if_configured
            and self.request.user.is_authenticated
            and not user_has_device(self.request.user)
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            path = reverse("user_profile:profile")
            return redirect_to_login(
                path,
                "user:require_otp",
                self.get_redirect_field_name(),
            )
        return super().dispatch(request, *args, **kwargs)


class ProfileTemplateView(
    LoginRequiredMixin,
    SiteOwnerProfilePermissionRequiredMixin,
    OtpRequired,
    TemplateView,
):
    permission_required = ("user.view_siteownerprofile",)
    template_name = "user_profile/profile.html"

    def get(self, request, *args, **kwargs):
        site_owner_profile = get_objects_for_user(
            request.user, ["view_siteownerprofile"], SiteOwnerProfile
        ).first()

        site = get_objects_for_user(
            request.user, ["view_site", "change_site"], Site
        ).first()

        self.extra_context = {
            "site": site,
            "site_owner_profile": site_owner_profile,
        }

        return super().get(request, *args, **kwargs)
