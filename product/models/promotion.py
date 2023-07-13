from django.db import models
from product.models.product import Product
from helper import PromotionType


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    prom_type = models.CharField(choices=PromotionType.choices, default=PromotionType.DISCOUNT, max_length=30)
    state_date = models.DateTimeField()
    end_date = models.DateTimeField()
    products = models.ManyToManyField(Product, related_name="product_list",)
    
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        
    def __str__(self):
        return f"{self.name} promotion for {self.products.name}"
    