from typing import Any
from django.db import models
from django.contrib.auth import get_user_model


# Get the UserModel
UserModel = get_user_model()


class UserOnToOne(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class UserForeign(UserOnToOne):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
