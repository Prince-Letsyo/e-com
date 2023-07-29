from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from user.models.user import SiteOwnerProfile
from django.contrib.sites.models import Site
from guardian.shortcuts import get_objects_for_user
from django.shortcuts import redirect


class IndexTemplateView(TemplateView):
    template_name = "user_profile/index.html"
    extra_context = {"obj": "gfhldfjkg"}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SiteOwnerProfilePermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == "SITEOWNER":
            return redirect("user_profile:index")

        if not self.has_permission():
            return redirect("user_profile:index")

        return super(SiteOwnerProfilePermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class ProfileTemplateView(
    LoginRequiredMixin, SiteOwnerProfilePermissionRequiredMixin, TemplateView
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
