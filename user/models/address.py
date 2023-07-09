from django.db import models

from user.models.utils import UserOnToOne


class UserAddress(UserOnToOne):
    address1= models.TextField()
    address2= models.TextField(null=True, blank=True)
    # city=models.TextChoices()
    postal_code= models.CharField(max_length=50)
    # country=models.CharField()
    telephone=models.CharField(max_length=15, null=True, blank=True, help_text="")
    mobile=models.CharField(max_length=15,)
    
    # objects=