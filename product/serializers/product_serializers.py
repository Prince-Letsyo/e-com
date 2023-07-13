from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.cart_item import CartItem
from product.models.order_item import OrderItem
from product.models.product import Product
from product.models.review import ProductReview
from product.serializers.cart_item_serializers import CartItemSerializer
from product.serializers.order_serializers import OrderItemSerializer
from product.serializers.review_serializers import ProductReviewSerializer


class ProductSerializer(serializers.ModelSerializer):
    product_cart = CartItemSerializer(required=False)
    product_reviews = ProductReviewSerializer(required=False, many=True)
    product_order = OrderItemSerializer(required=False)
    
    class Meta:
        extra_fields=[]
        model = Product
        
        if hasattr(model, 'product_cart'):
            extra_fields.append("product_cart")
            
        if hasattr(model, 'product_reviews'):
            extra_fields.append("product_reviews")

        if hasattr(model, 'product_order'):
            extra_fields.append("product_order")
        
        fields = [
            "id",
            "name",
            "desc",
            "sku",
            "brand_name",
            "category",
            "inventory",
            "price",
            "discount",
            "delivery_type",
            "shipping_type",
            "deleted_at", 
            *extra_fields
        ]
        read_only_fields = ('sku',)
    
    def to_internal_value(self, data):
        product_cart = data.pop("product_cart", None)
        product_reviews = data.pop("product_reviews", None)
        product_order = data.pop("product_order", None)
        
        if product_cart:
            writable_nested_serializer(
                data=product_cart, 
                Modal=CartItem,
                error=serializers.ValidationError(
                    {"product_cart": "Cart does not exist."}, 
                    404),
                Serializer=CartItemSerializer
                )
        
        if product_order:
            writable_nested_serializer(
                data=product_order, 
                Modal=OrderItem, 
                error=serializers.ValidationError(
                    {"product_order": "Order item does not exist."}, 404),
                Serializer=OrderItemSerializer
            )
        
        if product_reviews:
            if isinstance(product_reviews, list):
                for product_review in product_reviews:
                    writable_nested_serializer(
                        data=product_review, 
                        Modal=ProductReview, 
                        error=serializers.ValidationError(
                            {"product_reviews": "Product review does not exist."}, 404),
                        Serializer=ProductReviewSerializer
                    )
        return super().to_internal_value(data)

