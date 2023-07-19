from django.contrib import admin
from django import forms
from product.models.cart_item import *


class CartItemAdminForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = (
            "session",
            "product",
            "quantity",
        )


class CartItemAdmin(admin.ModelAdmin):
    form = CartItemAdminForm
    model = CartItem


admin.site.register(CartItem, CartItemAdmin)


class CartItemInline(admin.StackedInline):
    form = CartItemAdminForm
    extra = 0
    model = CartItem
