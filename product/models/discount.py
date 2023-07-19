import random
import uuid
from django.db import models
from helper import TimeDeletedStampsWithOrder


class ProductDiscountManager(models.Manager):
    use_in_migrations = True

    def get_discount_product(self, discount):
        return discount.discount_product.all()


class ProductDiscount(TimeDeletedStampsWithOrder):
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    desc = models.TextField()
    discount_percent = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=False)

    objects = ProductDiscountManager()

    class Meta:
        verbose_name = "Product Discount"
        verbose_name_plural = "Product Discounts"

    def __str__(self):
        return (
            f"Discount code: {self.code} for {int(self.discount_percent)}/100 percent"
        )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4().fields[-1])[:8].upper()
        return super().save(*args, **kwargs)
