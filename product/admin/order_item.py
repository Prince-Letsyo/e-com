from django.contrib import admin
from django import forms
from product.models.order_item import *


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = (
            "order",
            "product",
            "quantity",
        )


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = (
            "amount",
            "provider",
            "status",
        )


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "user",
            "total",
            "payment",
        )


class OrderItemInline(admin.StackedInline):
    form = OrderItemAdminForm
    extra = 0
    model = OrderItem


class OrderInline(admin.StackedInline):
    form = OrderAdminForm
    extra = 0
    model = Order


class PaymentAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    form = PaymentAdminForm
    model = Payment


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    form = OrderAdminForm
    model = Order


class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemAdminForm
    model = OrderItem


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
