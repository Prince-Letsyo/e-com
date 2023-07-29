from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class SiteOwnerProfilePermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == "SITEOWNER":
            return redirect("user_profile:index")

        if not self.has_permission():
            return redirect("user_profile:index")

        return super(SiteOwnerProfilePermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
