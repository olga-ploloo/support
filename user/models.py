from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager


class User(AbstractUser):
    # что если я потом захочу добвать еще одного типа пользователя?
    class Role(models.TextChoices):
        SUPPORT = 'support'
        CUSTOMER = 'customer'
        ADMIN = 'admin'

    base_role = Role.CUSTOMER

    role = models.CharField(max_length=8, choices=Role.choices)
    username = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=200, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk and not self.is_superuser:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def is_support(self):
        return self.role == User.Role.SUPPORT
