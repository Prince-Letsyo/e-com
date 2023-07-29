from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from product.models.shopping_session import ShoppingSession
from guardian.shortcuts import assign_perm

from user.models.user import (
    User,
    SiteUserProfile,
    SiteOwnerProfile,
    SiteUser,
    SiteOwner,
)


@receiver(post_save, sender=User)
def post_save_create_user_shopping_session(sender, instance, created, **kwargs):
    if created:
        ShoppingSession.objects.create(user=instance).save()


@receiver(post_save, sender=SiteUser)
def post_save_create_site_user(sender, instance, created, **kwargs):
    if created:
        site_user = SiteUserProfile.objects.create(user=instance).save()
        assign_perm("user.view_siteuserprofile", instance, site_user)


@receiver(post_save, sender=SiteOwner)
def post_save_create_site_owner(sender, instance, created, **kwargs):
    if created:
        site_owner = SiteOwnerProfile.objects.create(user=instance).save()
        assign_perm("user.view_siteownerprofile", instance, site_owner)
