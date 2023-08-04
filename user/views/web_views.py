from django.http import HttpResponse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_hotp.models import HOTPDevice


def qrcode_view(request, device_type, pk):
    if device_type == "time_based":
        device = TOTPDevice.objects.get(pk=pk)
    else:
        device = HOTPDevice.objects.get(pk=pk)

    try:
        import qrcode
        import qrcode.image.svg

        img = qrcode.make(device.config_url, image_factory=qrcode.image.svg.SvgImage)
        response = HttpResponse(content_type="image/svg+xml")
        img.save(response)
    except ImportError:
        response = HttpResponse("", status=503)

    return response
