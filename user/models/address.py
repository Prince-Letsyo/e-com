from django.db import models
from django_countries.fields import CountryField

from user.models.utils import UserOnToOne
from helper import city_choices

class UserAddress(UserOnToOne):
    address1= models.TextField()
    address2= models.TextField(null=True, blank=True)
    city=models.CharField(max_length=15,choices=city_choices)
    postal_code= models.CharField(max_length=50)
    country= CountryField(default="GH")
    telephone=models.CharField(max_length=15, null=True, blank=True, help_text="")
    mobile=models.CharField(max_length=15,)
    
    # objects=
    
    class Meta:
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        
    
    def __str__(self):
        return f"{self.user.get_username()}'s address: {self.address1}"
    