from django.db import models
from user.models.utils import UserForeign

class UserPayment(UserForeign):
    payment_type=models.CharField(max_length=20)
    provider = models.CharField(max_length=20)
    account_no = models.CharField(max_length=20)
    expiry = models.DateField()