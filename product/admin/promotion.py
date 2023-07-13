from django.contrib import admin
from django import forms
from product.models.promotion import *
from product.models.product import *



class PromotionAdminForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = (
        "name",
        "prom_type",
        "state_date",
        "end_date",
        "products",
        )
        
class PromotionAdmin(admin.ModelAdmin):
    form = PromotionAdminForm
    model = Promotion
    
admin.site.register(Promotion, PromotionAdmin)
