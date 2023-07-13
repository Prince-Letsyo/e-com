from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.product import Product
from product.models.promotion import Promotion
from product.serializers.product_serializers import ProductSerializer


class PromotionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(required=False, many=True)
    
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "prom_type",
            "prom_type",
            "state_date",
            "end_date",
            "products",
        ]

        
    def to_internal_value(self, data):
        products = data.pop("products", None)
        
        if products:
            if isinstance(products, list):
                for products in products:
                    writable_nested_serializer(
                        data=products, 
                        Modal=Product,
                        error=serializers.ValidationError(
                            {"products": "Product does not exist."}, 
                            404),
                        Serializer=ProductSerializer
                        )

        return super().to_internal_value(data)