from django import forms
from django_otp.models import Device
from django_otp.forms import OTPTokenForm
from django_otp import devices_for_user
from user.models.otp_proxy_models import CustomHOTPDevice, CustomTOTPDevice


class OTPDeviceForm(forms.ModelForm):
    type_of_key = forms.ChoiceField(
        choices=[("Time based", "time_based"), ("Counter based", "counter_based")],
        required=True,
    )

    class Meta:
        model = Device
        fields = ["name", "type_of_key"]


def get_user_device_list(user, json=False):
    options = []
    for device in list(d for d in devices_for_user(user)):
        if not isinstance(device, CustomTOTPDevice) and not isinstance(
            device, CustomHOTPDevice
        ):
            options.append(device)
    if not json:
        return list((d.persistent_id, d.name) for d in options)
    return list((d.persistent_id, d) for d in options)


class CustomOTPTokenForm(OTPTokenForm):
    def __init__(self, user, request=None, *args, **kwargs):
        super(CustomOTPTokenForm, self).__init__(user, request, *args, **kwargs)
        self.user = user
        self.fields["otp_device"].choices = get_user_device_list(user)
