from django.contrib import admin
from django import forms
from product.models.review import *


class ProductReviewAdminForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = (
            "product",
            "rating",
            "desc",
        )


class ProductReviewAdmin(admin.ModelAdmin):
    form = ProductReviewAdminForm
    model = ProductReview


class ProductReviewInline(admin.StackedInline):
    extra = 0
    form = ProductReviewAdminForm
    model = ProductReview


class UserReviewSessionAdminForm(forms.ModelForm):
    class Meta:
        model = UserReviewSession
        fields = [
            "id",
            "user",
            "review",
        ]


class UserReviewSessionAdmin(admin.ModelAdmin):
    form = UserReviewSessionAdminForm
    model = UserReviewSession


class UserReviewSessionInline(admin.StackedInline):
    extra = 0
    form = UserReviewSessionAdminForm
    model = UserReviewSession


admin.site.register(UserReviewSession, UserReviewSessionAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
