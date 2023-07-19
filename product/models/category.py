from django.db import models

from helper import TimeDeletedStampsWithOrder


def product_category_directory_path(instance, filename):
    return f"{instance.__class__.__name__.lower()}/{instance.name}/{filename}"


class ProductCategoryManager(models.Manager):
    use_in_migrations = True

    def get_category_product(self, category):
        return category.category_product.all()


class ProductCategory(TimeDeletedStampsWithOrder):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    banner = models.ImageField(upload_to=product_category_directory_path)

    objects = ProductCategoryManager()

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return f"{self.name} category"
