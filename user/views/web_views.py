from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import  CreateView

@login_required
@permission_required(
    (
        "user.add_siteowner",
        "user.view_siteowner",
    ),
)
def create_domain(request, *args, **kwargs):
    return render(request, "user/create_domain.html", context={})


class SiteOwnerUserView(CreateView):
    # def g
    pass
