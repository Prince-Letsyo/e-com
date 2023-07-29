from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from helper.choices import Sex


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("First name"), "autocomplete": "first_name"}
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Last name"), "autocomplete": "last_name"}
        ),
    )
    middle_name = forms.CharField(
        label=_("Middle name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Middle name"), "autocomplete": "middle_name"}
        ),
    )
    gender = forms.ChoiceField(
        label=_("Sex"),
        choices=[
            ("", "____________select____________"),
            *[(choice[0], choice[1]) for choice in Sex.choices],
        ],
    )

    def custom_signup(self, request, user):
        data = request.POST
        user.gender = data["gender"]
        user.middle_name = data["middle_name"]
        user.save()
        return super().custom_signup(request, user)
