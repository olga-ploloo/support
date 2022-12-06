from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # что если я потом захочу добвать еще одного типа пользователя?
    class UserType(models.TextChoices):
        SUPPORT = 'support'
        CUSTOMER = 'customer'

    role = models.CharField(choices=UserType.choices, default=UserType.CUSTOMER)
