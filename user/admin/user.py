from django.contrib import admin
from django import forms
from product.admin import OrderInline, UserReviewSessionInline, ShoppingSessionInline

from user.models.user import User, SiteOwner


class SiteOwnerAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["public_key"].widget.attrs.update({"disabled": True})
        self.fields["secret_key"].widget.attrs.update({"disabled": True})

    class Meta:
        model = SiteOwner
        fields = (
            "user",
            "public_key",
            "secret_key",
            "deleted_at",
        )


class SiteOwnerInline(admin.StackedInline):
    form = SiteOwnerAdminForm
    extra = 0
    model = SiteOwner


class UserAdmin(admin.ModelAdmin):
    inlines = [
        SiteOwnerInline,
        ShoppingSessionInline,
        OrderInline,
        UserReviewSessionInline,
    ]
    list_display = [
        "username",
        "email",
    ]
    search_fields = ["username"]


admin.site.register(User, UserAdmin)
