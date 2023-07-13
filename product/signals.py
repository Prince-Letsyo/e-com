from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from product.models import  ShoppingSession, CartItem, Order
from product.models.order_item import OrderItem

def product_total_price(quantity, price, discount_percent):
    return quantity * price if discount_percent == 0.00 else (quantity * price)* ((100-discount_percent)/100)

@receiver(post_save, sender=CartItem)
def post_save_increase_shopping_session_subtotal(sender, instance, created, **kwargs):
    sessions = ShoppingSession.objects.filter(id=instance.session.id) 
    if sessions.exists():
        session = sessions.first()
        cart_items = session.session_cart_items.all()
        for item in cart_items:
            session.subtotal += product_total_price(item.quantity,item.product.price,item.product.discount.discount_percent )
        session.save()
        
@receiver(pre_delete, sender=CartItem)
def pre_delete_decrease_shopping_session_subtotal(sender, instance, **kwargs):
    sessions = ShoppingSession.objects.filter(id=instance.session.id) 
    if sessions.exists():
        session = sessions.first()
        cart_items = session.session_cart_items.all()
        for item in cart_items:
            session.subtotal -= product_total_price(item.quantity,item.product.price,item.product.discount.discount_percent )
        session.save()


@receiver(post_save, sender=Order)
def post_save_delete_(sender, instance, created, **kwargs):
    sessions = ShoppingSession.objects.filter(user_id=instance.user.id)
    if sessions.exists():
        session = sessions.first()
        cart_items = session.session_cart_items.all()
        
        for item in cart_items:
            OrderItem.objects.create(
                order=instance, 
                product=item.product, 
                quantity=item.quantity).save()

            item.delete()