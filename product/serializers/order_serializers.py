from rest_framework import serializers
from product.models.order_item import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=[
            "id",
            "user",
            "total",
            "payment",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields=[
            "id",
            "order",
            "product",
            "quantity",
        ]

