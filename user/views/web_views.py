from django.views.generic import CreateView
from django.contrib.sites.models import Site
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, resolve_url
from urllib.parse import urlparse

from user.models.user import SiteOwner


class SiteOwnerUserPermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        if not self.has_permission():
            return redirect("/")
        return super(SiteOwnerUserPermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class SiteOwnerUserView(
    LoginRequiredMixin, SiteOwnerUserPermissionRequiredMixin, CreateView
):
    permission_required = (
        "user.add_siteowner",
        "user.view_siteowner",
    )
    queryset = Site.objects.all()
    template_name = "user/create_domain.html"
    success_url = "/"
    fields = [
        "domain",
        "name",
    ]

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            form_valid = self.form_valid(form)
            site = self.queryset.filter(domain=request.POST["domain"]).first()
            SiteOwner.objects.create(user=request.user, site=site)
            return form_valid
        else:
            return self.form_invalid(form)
