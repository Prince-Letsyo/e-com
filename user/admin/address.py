from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib import admin
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from user.models.address import UserAddress

# Register your models here.


class UserAddressFormAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].widget.attrs.update({"class": "user_address_city"})
        self.fields["country"].widget.attrs.update({"class": "user_address_country"})

    class Meta:
        model = UserAddress
        fields = [
            "user",
            "address1",
            "address2",
            "postal_code",
            "country",
            "city",
            "mobile",
            "telephone",
        ]


class UserAddressAdmin(admin.ModelAdmin):
    form = UserAddressFormAdmin
    list_display = ["user", "city", "country"]
    search_fields = ["city"]

    class Media:
        js = ("js/admin/user/user_address_admin.js",)


admin.site.register(UserAddress, UserAddressAdmin)


class UserAddressInline(admin.StackedInline):
    form = UserAddressFormAdmin
    extra = 0
    model = UserAddress
