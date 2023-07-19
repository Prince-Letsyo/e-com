from django.contrib import admin
from django import forms
from product.admin.product import ProductInline
from product.models.discount import *


class ProductDiscountAdminForm(forms.ModelForm):
    class Meta:
        model = ProductDiscount
        fields = (
            "code",
            "desc",
            "discount_percent",
            "active",
            "deleted_at",
        )


class ProductDiscountAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    form = ProductDiscountAdminForm
    model = ProductDiscount


admin.site.register(ProductDiscount, ProductDiscountAdmin)
