from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.inventory import ProductInventory
from product.models.product import Product
from product.serializers.product_serializers import ProductSerializer



class ProductInventorySerializer(serializers.ModelSerializer):
    inventory_product = ProductSerializer(required=False)
    
    class Meta:
        model = ProductInventory
    
        extra_fields=[]
        
        if hasattr(model, 'inventory_product'):
            extra_fields.append("inventory_product")
            
        fields=[
            "id",
            "quantity",
            "deleted_at",
            *extra_fields
        ]
        
        
    def to_internal_value(self, data):
        inventory_product = data.pop("inventory_product", None)
        
        if inventory_product:
            writable_nested_serializer(
                data=inventory_product, 
                Modal=Product,
                error=serializers.ValidationError(
                    {"inventory_product": "Product does not exist."}, 
                    404),
                Serializer=ProductSerializer
                )

        return super().to_internal_value(data)
