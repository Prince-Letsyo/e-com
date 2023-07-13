from rest_framework import serializers
from product.models.category import ProductCategory
from product.models.product import Product
from product.serializers.product_serializers import ProductSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    category_products = ProductSerializer(read_only=True, required=False,many=True)
    
    class Meta:
        model = ProductCategory
        
        extra_fields=[]
        
        if hasattr(model, 'category_products'):
            extra_fields.append("category_products")
        fields=[
            "id",
            "name",
            "desc",
            "banner",
            "deleted_at",
            *extra_fields
        ]

