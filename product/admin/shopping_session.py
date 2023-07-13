from django.contrib import admin
from django import forms
from product.admin.cart_item import CartItemInline
from product.models.shopping_session import *



class ShoppingSessionAdminForm(forms.ModelForm):
    class Meta:
        model = ShoppingSession
        fields = (
        "user",
        "subtotal",
        "deleted_at",
        )
        
class ShoppingSessionAdmin(admin.ModelAdmin):
    inlines=[CartItemInline]
    form = ShoppingSessionAdminForm
    model = ShoppingSession
    
admin.site.register(ShoppingSession, ShoppingSessionAdmin)


class ShoppingSessionInline(admin.StackedInline):
    form = ShoppingSessionAdminForm
    extra=0
    model = ShoppingSession