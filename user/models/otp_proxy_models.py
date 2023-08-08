from base64 import b32encode
from urllib.parse import quote, urlencode
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_hotp.models import HOTPDevice
from helper.utils import get_domain
from django.contrib.sites.models import Site
from user.models import SiteOwnerProfile


def get_domain_name(request):
    return get_domain(request, site_owner_model=SiteOwnerProfile, site=Site).name


class CustomHOTPDevice(HOTPDevice):
    def config_url(self, request):
        label = self.user.get_username()
        params = {
            "secret": b32encode(self.bin_key),
            "algorithm": "SHA1",
            "digits": self.digits,
            "counter": self.counter,
        }
        urlencoded_params = urlencode(params)

        issuer = get_domain_name(request)
        if callable(issuer):
            issuer = issuer(self)
        if isinstance(issuer, str) and (issuer != ""):
            issuer = issuer.replace(":", "")
            label = "{}:{}".format(issuer, label)
            urlencoded_params += "&issuer={}".format(
                quote(issuer)
            )  # encode issuer as per RFC 3986, not quote_plus

        url = "otpauth://hotp/{}?{}".format(quote(label), urlencoded_params)

        return url

    class Meta(HOTPDevice.Meta):
        proxy = True


class CustomTOTPDevice(TOTPDevice):
    def config_url(self, request):
        label = str(self.user.get_username())
        params = {
            "secret": b32encode(self.bin_key),
            "algorithm": "SHA1",
            "digits": self.digits,
            "period": self.step,
        }
        urlencoded_params = urlencode(params)

        issuer = get_domain_name(request)
        if issuer:
            issuer = issuer.replace(":", "")
            label = "{}:{}".format(issuer, label)
            urlencoded_params += "&issuer={}".format(
                quote(issuer)
            )  # encode issuer as per RFC 3986, not quote_plus

        image = self._read_str_from_settings("OTP_TOTP_IMAGE")
        if image:
            urlencoded_params += "&image={}".format(quote(image, safe=":/"))

        url = "otpauth://totp/{}?{}".format(quote(label), urlencoded_params)

        return url

    class Meta(TOTPDevice.Meta):
        proxy = True
