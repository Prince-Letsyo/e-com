import json
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import BACKEND_SESSION_KEY, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
from guardian.shortcuts import assign_perm, get_objects_for_user
from django_otp import devices_for_user
from django_otp.forms import OTPTokenForm
from django_otp.plugins.otp_hotp.models import HOTPDevice
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_static.lib import add_static_token

from user.forms import CreateSiteForm


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


def get_site_view(request, *args, **kwargs):
    site, response = get_site_and_res(request.user)
    if response:
        return response
    return JsonResponse({"name": site.name, "domain": site.domain}, status=200)


def update_site_view(request, *args, **kwargs):
    site, response = get_site_and_res(request.user)
    if response:
        return response

    form = CreateSiteForm(json.loads(request.body) or None, instance=site)
    if form.is_valid():
        site = form.save()
        return JsonResponse(form.data, status=200)
    status = form.errors.get_json_data()["domain"][0]["code"]
    return JsonResponse(form.errors, status=400)


def create_device(device_model, user, data, key_type):
    device_list = device_model.objects.filter(user=user, **data)
    if device_list.exists():
        return JsonResponse({"device": "Device already exits."}, status=400)
    else:
        device = device_model.objects.create(user=user, **data)

        for op in list((d.persistent_id, d) for d in devices_for_user(user)):
            if op[1].name == device.name and op[1].user == device.user:
                options = op[0]
                break

        return JsonResponse(
            {
                "link": reverse(
                    "user:qrcode", kwargs={"pk": device.pk, "device_type": key_type}
                ),
                "otp_device": options,
            },
            status=201,
        )


def create_user_token_device(request, *args, **kwargs):
    data = json.loads(request.body)
    key_type = data.pop("type_of_key")
    if key_type == "time_based":
        return create_device(
            device_model=TOTPDevice, user=request.user, data=data, key_type=key_type
        )
    else:
        return create_device(
            device_model=HOTPDevice, user=request.user, data=data, key_type=key_type
        )


def json_token_check_view(request, *args, **kwargs):
    form = OTPTokenForm(
        user=request.user, request=request, data=json.loads(request.body) or None
    )
    if form.is_valid():
        user = form.get_user()
        if not hasattr(user, "backend"):
            user.backend = request.session[BACKEND_SESSION_KEY]
            auth_login(request, form.get_user())
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({}, status=400)


def create_backup_token_code_view(request, *args, **kwargs):
    static_devices = StaticDevice.objects.filter(user=request.user)
    device_count = 10

    if static_devices.exists():
        static_device = static_devices.first()
        if not (static_device.token_set.all().count() >= device_count):
            for _ in range(device_count):
                add_static_token(username=request.user.username)

        static_token_list = [
            static_token.token for static_token in static_device.token_set.all()
        ]

        return JsonResponse({"codes": static_token_list}, status=200)
    return JsonResponse({"device": "Device does not exist."}, status=400)

def get_user_backup_codes(request, *args, **kwargs):
    static_devices = StaticDevice.objects.filter(user=request.user)

    if static_devices.exists():
        static_device = static_devices.first()
        static_token_list = [
            static_token.token for static_token in static_device.token_set.all()
        ]

        return JsonResponse({"codes": static_token_list}, status=200)
    return JsonResponse({"device": "Device does not exist."}, status=400)
