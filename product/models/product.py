import random
import string

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from product.models.category import ProductCategory
from product.models.inventory import ProductInventory
from helper import TimeDeletedStampsWithOrder,DeliveryType,ShippingType
from product.models.discount import ProductDiscount


class ProductManager(models.Manager):
    use_in_migrations=True
    
    def get_product_cartitem(self, product):
        try:
            return product.product_cart
        except ObjectDoesNotExist:
            return None
        
    def get_product_reviews(self, product):
        return product.product_reviews.all()

        
    def get_product_order(self, product):
        try:
            return product.product_order
        except ObjectDoesNotExist:
            return None


# Create your models here.
class Product(TimeDeletedStampsWithOrder):
    name = models.CharField(max_length=200,)
    desc = models.TextField()
    sku = models.CharField(max_length=25, null=True, blank=True)
    brand_name = models.CharField(max_length=150)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="category_products")
    inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE, related_name="inventory_product")
    price = models.DecimalField(decimal_places=2, default=0, max_digits=16)
    discount = models.ForeignKey(ProductDiscount, on_delete=models.CASCADE, related_name="discount_products")
    delivery_type = models.CharField(max_length=30, choices=DeliveryType.choices, default= DeliveryType.INSTOREPICKUP)
    shipping_type = models.CharField(max_length=30, choices=ShippingType.choices, default= ShippingType.POSTALSERVICE)
    
    objects = ProductManager()
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.sku:
            product_name = ''.join(e for e in self.name if e.isalnum())
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.sku = f'{product_name[:4].upper()}{self.brand_name[:2].upper()}{self.category.name[:2].upper()}{random_chars}'
        return super().save(*args, **kwargs)