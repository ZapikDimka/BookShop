from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name='Email address')
    policy_agreed = models.BooleanField(default=False, verbose_name="Agreed with policy")

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Унікальне ім'я для груп
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Унікальне ім'я для дозволів
        blank=True
    )

    def __str__(self):
        return self.username
