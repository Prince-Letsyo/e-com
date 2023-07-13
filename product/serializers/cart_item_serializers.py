from rest_framework import serializers
from product.models.cart_item import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "session",
            "product",
            "quantity",
        ]

