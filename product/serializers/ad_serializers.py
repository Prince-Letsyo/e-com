from rest_framework import serializers
from product.models.ad import ProductAd


class ProductAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAd
        fields = [
            "id",
            "name",
            "image",
            "slug",
        ]
        read_only_fields = ('slug',)
