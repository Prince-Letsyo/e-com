from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.discount import ProductDiscount
from product.models.product import Product
from product.serializers.product_serializers import ProductSerializer


class ProductDiscountSerializer(serializers.ModelSerializer):
    discount_products = ProductSerializer(required=False, many=True)

    class Meta:
        model = ProductDiscount

        extra_fields = []

        if hasattr(model, "discount_products"):
            extra_fields.append("discount_products")
        fields = [
            "id",
            "code",
            "desc",
            "discount_percent",
            "active",
            "deleted_at",
            *extra_fields,
        ]
        read_only_fields = ("code",)

    def to_internal_value(self, data):
        discount_products = data.pop("discount_products", None)

        if discount_products:
            if isinstance(discount_products, list):
                for discount_product in discount_products:
                    writable_nested_serializer(
                        data=discount_product,
                        Modal=Product,
                        error=serializers.ValidationError(
                            {"discount_product": "Product does not exist."}, 404
                        ),
                        Serializer=ProductSerializer,
                    )

        return super().to_internal_value(data)
