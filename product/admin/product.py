from django.contrib import admin
from django import forms
from product.admin.cart_item import CartItemInline
from product.admin.order_item import OrderItemInline
from product.admin.review import ProductReviewInline
from product.models.product import *


class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "desc",
            "sku",
            "brand_name",
            "category",
            "price",
            "discount",
            "inventory",
            "category",
            "delivery_type",
            "shipping_type",
            "deleted_at",
        )


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductReviewInline,
        CartItemInline,
        ProductReviewInline,
        OrderItemInline,
    ]
    form = ProductFormAdmin
    list_display = [
        "name",
        "sku",
        "brand_name",
        "category",
        "price",
    ]
    search_fields = [
        "name",
        "sku",
        "brand_name",
        "category",
    ]

    list_filter = [
        "category",
        "delivery_type",
        "shipping_type",
    ]


admin.site.register(Product, ProductAdmin)


class ProductInline(admin.StackedInline):
    form = ProductFormAdmin
    model = Product
    extra = 1
