from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from product.models.shopping_session import ShoppingSession

from user.models.user import User


@receiver(post_save, sender=User)
def post_save_create_user_shopping_session(sender, instance, created, **kwargs):
    if created:
        ShoppingSession.objects.create(user=instance).save()
