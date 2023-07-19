from django.db import models
from django.utils.text import slugify
from datetime import datetime


def product_ad_directory_path(instance, filename):
    return f"{instance.__class__.__name__.lower()}/{instance.name}/{filename}"


class ProductAd(models.Model):
    image = models.ImageField(upload_to=product_ad_directory_path)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Product Ad"
        verbose_name_plural = "Product Ads"

    def __str__(self) -> str:
        return f"{self.name} ad"

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.now()
            slug_datetime = now.strftime("%Y-%m-%d-%H-%M-%S")
            self.slug = slugify(f"{self.name}-{slug_datetime}")
        base_slug = self.slug
        num = 1
        while ProductAd.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{base_slug}-{num}"
            num += 1
        return super().save(*args, **kwargs)
