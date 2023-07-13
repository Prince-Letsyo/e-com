from django.contrib import admin
from django import forms
from product.models.ad import *



class ProductAdAdminForm(forms.ModelForm):
    class Meta:
        model = ProductAd
        fields = (
        "name",
        "image",
        "slug",
        )
        
class ProductAdAdmin(admin.ModelAdmin):
    form = ProductAdAdminForm
    model = ProductAd
    
admin.site.register(ProductAd, ProductAdAdmin)
