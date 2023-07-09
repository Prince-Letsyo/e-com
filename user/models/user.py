from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from helper import (Sex, TimeStamps, )


class UserManager(BaseUserManager):
    def create_user(self, email,username, first_name, last_name, password=None):
        if first_name is None:
            raise TypeError('User should provide an user name')
        if username is None:
            raise TypeError('User should provide an first name')
        if last_name is None:
            raise TypeError('User should provide an last name')
        if email is None:
            raise TypeError('User should provide an email')

        if email == '':
            raise ValueError('User email should not be empty')
        if username == '':
            raise ValueError('User user name should not be empty')
        if first_name == '':
            raise ValueError('User first name should not be empty')
        if last_name == '':
            raise ValueError('User last name should not be empty')

        user = self.model(
            first_name=first_name,
            username=username,
                          last_name=last_name, 
                          email=self.normalize_email(email)
                          )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username, first_name, last_name, password):
        if password is None:
            raise TypeError('User should provide a password')
        if password == '':
            raise ValueError('User password should not be empty')

        user = self.create_user(
            email=email, 
            first_name=first_name,
            username=username,
            last_name=last_name, 
            password=password
            )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStamps):
    username = models.CharField(max_length=150,unique=True,null=False, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=2,
                              choices=Sex.choices, default=Sex.MALE)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', "email"]

    objects = UserManager()

    def __str__(self):
        return self.email
