from django.contrib import admin
from django.http import HttpResponse
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django_otp.plugins.otp_hotp.admin import HOTPDeviceAdmin
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_hotp.models import HOTPDevice
from django_otp.conf import settings
from django.core.exceptions import PermissionDenied

from user.models.otp_proxy_models import CustomHOTPDevice, CustomTOTPDevice


@admin.register(CustomTOTPDevice)
class CustomTOTPDeviceAdmin(TOTPDeviceAdmin):
    def qrcode_view(self, request, pk):
        if settings.OTP_ADMIN_HIDE_SENSITIVE_DATA:
            raise PermissionDenied()

        device = CustomTOTPDevice.objects.get(pk=pk)
        if not self.has_view_or_change_permission(request, device):
            raise PermissionDenied()

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


admin.site.unregister(TOTPDevice)


@admin.register(CustomHOTPDevice)
class CustomHOTPDeviceAdmin(HOTPDeviceAdmin):
    def qrcode_view(self, request, pk):
        if settings.OTP_ADMIN_HIDE_SENSITIVE_DATA:
            raise PermissionDenied()

        device = CustomHOTPDevice.objects.get(pk=pk)
        if not self.has_view_or_change_permission(request, device):
            raise PermissionDenied()

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


admin.site.unregister(HOTPDevice)
