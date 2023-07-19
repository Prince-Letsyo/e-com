from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models import Order, OrderItem, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "provider",
            "status",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer()
    order_item_orders = OrderItemSerializer(required=False, many=True)

    class Meta:
        extra_fields = []
        model = Order

        if hasattr(model, "order_item_orders"):
            extra_fields.append("order_item_orders")

        fields = ["id", "user", "total", "payment", *extra_fields]

    def to_internal_value(self, data):
        order_item_orders = data.pop("order_item_orders", None)

        if order_item_orders:
            writable_nested_serializer(
                data=order_item_orders,
                Modal=OrderItem,
                error=serializers.ValidationError(
                    {"order_item_orders": "OrderItem does not exist."}, 404
                ),
                Serializer=OrderItemSerializer,
            )

        return super().to_internal_value(data)

    def to_internal_value(self, data):
        payment = data.pop("payment", None)

        if payment:
            writable_nested_serializer(
                data=payment,
                Modal=Payment,
                error=serializers.ValidationError(
                    {"payment": "Payment does not exist."}, 404
                ),
                Serializer=PaymentSerializer,
            )

        return super().to_internal_value(data)
