from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

from user.managers import CustomUserManager

class User(AbstractUser):
    # что если я потом захочу добвать еще одного типа пользователя?
    class Role(models.TextChoices):
        SUPPORT = 'support'
        CUSTOMER = 'customer'
        ADMIN = 'admin'

    base_role = Role.CUSTOMER

    role = models.CharField(max_length=8, choices=Role.choices)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    is_support = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


# class CustomerManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         result = super().get_queryset(*args, **kwargs)
#         return result.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER

#
# class SupportManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         result = super().get_queryset(*args, **kwargs)
#         return result.filter(role=User.Role.SUPPORT)


class Support(User):
    base_role = User.Role.SUPPORT
