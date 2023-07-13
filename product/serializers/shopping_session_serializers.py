from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.cart_item import CartItem
from product.models.shopping_session import ShoppingSession
from product.serializers.cart_item_serializers import CartItemSerializer


class ShoppingSessionSerializer(serializers.ModelSerializer):
    session_cart_items = CartItemSerializer(required=False, many=True)
    
    class Meta:
        model = ShoppingSession
        extra_fields = []
        
        if hasattr(model, 'session_cart_items'):
            extra_fields.append("session_cart_items")
            
        fields=[
            "id",
            "user",
            "subtotal",
            "deleted_at",
            *extra_fields
        ]
        
    def to_internal_value(self, data):
        session_cart_items = data.pop("session_cart_items", None)
        
        if session_cart_items:
            writable_nested_serializer(
                data=session_cart_items, 
                Modal=CartItem,
                error=serializers.ValidationError(
                    {"session_cart_items": "Cart Item does not exist."}, 
                    404),
                Serializer=CartItemSerializer
                )
            
        return super().to_internal_value(data)
