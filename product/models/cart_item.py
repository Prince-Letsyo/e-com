from django.db import models
from product.models.product import Product
from helper import TimeStampsWithOrder
from product.models.shopping_session import ShoppingSession


class CartItemManager(models.Manager):
    use_in_migrations = True
    
class CartItem(TimeStampsWithOrder):
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE, related_name="session_cart_items")
    product = models.OneToOneField(Product, related_name="product_cart", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    objects = CartItemManager()
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
    def __str__(self) -> str:
        return f"{self.session.user.get_username()} has {self.quantity} {self.product.name}(s) in this cart"
    
     
    