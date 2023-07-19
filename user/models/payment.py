from django.db import models
from user.models.utils import UserForeign
from helper import PaymentType, payment_provider_choices


class UserPayment(UserForeign):
    payment_type = models.CharField(choices=PaymentType.choices, max_length=20)
    provider = models.CharField(choices=payment_provider_choices, max_length=20)
    account_no = models.CharField(max_length=20)
    expiry = models.DateField()

    class Meta:
        verbose_name = "User Payment"
        verbose_name_plural = "User Payments"

    def __str__(self):
        return f"{self.user.get_username()} | {self.account_no}"
