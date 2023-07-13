from django.contrib import admin
from django import forms
from product.admin.product import ProductInline
from product.models.inventory import *




class ProductInventoryAdminForm(forms.ModelForm):
    class Meta:
        model = ProductInventory
        fields = (
        "quantity",
        "deleted_at",
        )
        
class ProductInventoryAdmin(admin.ModelAdmin):
    inlines=[ProductInline]
    form = ProductInventoryAdminForm
    model = ProductInventory

admin.site.register(ProductInventory, ProductInventoryAdmin)
