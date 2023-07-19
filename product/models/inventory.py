from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from helper import TimeDeletedStampsWithOrder


class ProductInventoryManager(models.Manager):
    use_in_migrations = True

    def get_inventory_product(self, inventory):
        try:
            return inventory.inventory_product
        except ObjectDoesNotExist:
            return None


class ProductInventory(TimeDeletedStampsWithOrder):
    quantity = models.IntegerField(default=0)

    objects = ProductInventoryManager()

    class Meta:
        verbose_name = "Product Inventory"
        verbose_name_plural = "Product Inventories"

    def __str__(self):
        return f"{self.quantity} product(s)"
