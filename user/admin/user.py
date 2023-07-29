from django.contrib.sites.admin import SiteAdmin
from guardian.admin import GuardedModelAdmin
from django.contrib import admin
from django import forms
from product.admin import OrderInline, UserReviewSessionInline, ShoppingSessionInline
from django.contrib.sites.models import Site
from user.models.user import User, SiteOwnerProfile, SiteUserProfile


class SiteOwnerProfileAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["public_key"].widget.attrs.update({"disabled": True})
        self.fields["secret_key"].widget.attrs.update({"disabled": True})

    class Meta:
        model = SiteOwnerProfile
        fields = (
            "user",
            "public_key",
            "secret_key",
            "deleted_at",
        )


class SiteUserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = SiteUserProfile
        fields = (
            "user",
            "deleted_at",
        )


class SiteOwnerProfileInline(admin.StackedInline):
    form = SiteOwnerProfileAdminForm
    extra = 0
    model = SiteOwnerProfile


class SiteUserProfileInline(admin.StackedInline):
    form = SiteUserProfileAdminForm
    extra = 0
    model = SiteUserProfile


class UserAdmin(admin.ModelAdmin):
    inlines = [
        SiteOwnerProfileInline,
        SiteUserProfileInline,
        ShoppingSessionInline,
        OrderInline,
        UserReviewSessionInline,
    ]
    list_display = [
        "username",
        "email",
    ]
    search_fields = ["username"]


admin.site.unregister(Site)


@admin.register(Site)
class MySiteAdmin(GuardedModelAdmin, SiteAdmin):
    pass


admin.site.register(User, UserAdmin)
