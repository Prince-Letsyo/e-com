from django.contrib import admin
from django import forms
from product.models.category import *


class ProductCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = (
            "name",
            "desc",
            "banner",
            "deleted_at",
        )


class ProductCategoryAdmin(admin.ModelAdmin):
    form = ProductCategoryAdminForm
    model = ProductCategory


admin.site.register(ProductCategory, ProductCategoryAdmin)
