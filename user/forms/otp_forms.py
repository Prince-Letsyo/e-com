from django import forms
from django_otp.models import Device

from user.models.user import User


class OTPDeviceForm(forms.ModelForm):
    type_of_key = forms.ChoiceField(
        choices=[("Time based", "time_based"), ("Counter based", "counter_based")],
        required=True,
    )

    class Meta:
        model = Device
        fields = ["name", "type_of_key"]
