import random
import string
from django.contrib.sites.models import Site
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from helper import (
    Sex,
    TimeStamps,
)
from django.utils.translation import gettext_lazy as _
from helper import DeletedAt


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_user_user_payments(self, user):
        return user.userpayment_set.all()

    def get_user_shopping_session(self, user):
        try:
            return user.shoppingsession
        except ObjectDoesNotExist:
            return None

    def get_user_user_address(self, user):
        try:
            return user.useraddress
        except ObjectDoesNotExist:
            return None

    def create_user(self, email, username, first_name, last_name, password=None):
        if first_name is None:
            raise TypeError("User should provide an user name")
        if username is None:
            raise TypeError("User should provide an first name")
        if last_name is None:
            raise TypeError("User should provide an last name")
        if email is None:
            raise TypeError("User should provide an email")

        if email == "":
            raise ValueError("User email should not be empty")
        if username == "":
            raise ValueError("User user name should not be empty")
        if first_name == "":
            raise ValueError("User first name should not be empty")
        if last_name == "":
            raise ValueError("User last name should not be empty")

        user = self.model(
            first_name=first_name,
            username=username,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        if password is None:
            raise TypeError("User should provide a password")
        if password == "":
            raise ValueError("User password should not be empty")

        user = self.create_user(
            email=email,
            first_name=first_name,
            username=username,
            last_name=last_name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStamps):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        SITEOWNER = "SITEOWNER", _("Site Owner")
        SITEUSER = "SITEUSER", _("Site User")

    base_role = Role.ADMIN

    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=Sex.choices, default=Sex.MALE)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(verbose_name="Role", max_length=50, choices=Role.choices)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


def generate_random_string(length):
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length
        )
    )


class SiteOwner(User):
    base_role = User.Role.SITEOWNER

    class Meta:
        proxy = True


class SiteUser(User):
    base_role = User.Role.SITEUSER

    class Meta:
        proxy = True


class SiteUserProfile(DeletedAt):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="site_user"
    )


class SiteOwnerProfile(DeletedAt):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="site_owner"
    )
    public_key = models.CharField(max_length=250, null=True, blank=True)
    secret_key = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.public_key and not self.secret_key:
            self.public_key = generate_random_string(32)
            self.secret_key = generate_random_string(64)
        return super().save(*args, **kwargs)
