import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
from guardian.shortcuts import assign_perm, get_objects_for_user

from user.forms import CreateSiteForm


@csrf_exempt
def create_site_view(request, *args, **kwargs):
    form = CreateSiteForm(json.loads(request.body) or None)
    if form.is_valid():
        site = form.save()
        assign_perm("change_site", request.user, site)
        assign_perm("view_site", request.user, site)
        return JsonResponse(form.data, status=200)
    status = form.errors.get_json_data()["domain"][0]["code"]
    return JsonResponse(form.errors, status=status)


def get_site_and_res(user):
    response = None
    site = None
    sites = get_objects_for_user(user, ["change_site"], Site)
    if sites.exists():
        site = sites.first()
    else:
        response = JsonResponse({"error": f"Site does not exist"}, status=400)
    return site, response


@csrf_exempt
def get_site_view(request, *args, **kwargs):
    site, response = get_site_and_res(request.user)
    if response:
        return response
    return JsonResponse({"name": site.name, "domain": site.domain}, status=200)


@csrf_exempt
def update_site_view(request, *args, **kwargs):
    site, response = get_site_and_res(request.user)
    if response:
        return response

    form = CreateSiteForm(json.loads(request.body) or None, instance=site)
    if form.is_valid():
        site = form.save()
        return JsonResponse(form.data, status=200)
    status = form.errors.get_json_data()["domain"][0]["code"]
    return JsonResponse(form.errors, status=status)
