from django.db import models
from user.models.utils import UserOnToOne
from helper import TimeDeletedStampsWithOrder


class ShoppingSessionManager(models.Manager):
    use_in_migrations=True

    def get_session_cart_items(self, session):
        return session.session_cart_items.all()
    
class ShoppingSession(UserOnToOne, TimeDeletedStampsWithOrder):
    subtotal = models.DecimalField(decimal_places=2, default=0, max_digits=16)
    
    objects = ShoppingSessionManager()
    
    class Meta:
        verbose_name = 'Shopping Session'
        verbose_name_plural = 'Shopping Sessions'
        
    def __str__(self):
        return f"{self.user.get_username()} currently has a total of {self.subtotal} shop item(s)"
    