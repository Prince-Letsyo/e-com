from django import forms
from django.contrib.sites.models import Site
from helper.utils import is_valid_url


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            "name",
            "domain",
        ]

    def clean_domain(self):
        domain = self.cleaned_data["domain"]
        if not is_valid_url(domain):
            raise forms.ValidationError(f"{domain} is not a valid url", code=400)
        return domain
