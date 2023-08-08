from django.http import HttpResponse

from user.models.otp_proxy_models import CustomHOTPDevice, CustomTOTPDevice


def qrcode_view(request, device_type, pk):
    if device_type == "time_based":
        device = CustomTOTPDevice.objects.get(pk=pk)
    else:
        device = CustomHOTPDevice.objects.get(pk=pk)

    try:
        import qrcode
        import qrcode.image.svg

        img = qrcode.make(
            device.config_url(request), image_factory=qrcode.image.svg.SvgImage
        )
        response = HttpResponse(content_type="image/svg+xml")
        img.save(response)
    except ImportError:
        response = HttpResponse("", status=503)

    return response
