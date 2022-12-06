from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # что если я потом захочу добвать еще одного типа пользователя?
    class Role(models.TextChoices):
        SUPPORT = 'support'
        CUSTOMER = 'customer'

    base_role = Role.CUSTOMER

    role = models.CharField(max_length=8, choices=Role.choices)
    email = models.EmailField(max_length=200, unique=True)

    # is_student = models.BooleanField(default=False)
    # is_teacher = models.BooleanField(default=False)

    # USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER

    class Meta:
        proxy = True


class SupportManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.SUPPORT)


class Support(User):
    base_role = User.Role.SUPPORT

    class Meta:
        proxy = True