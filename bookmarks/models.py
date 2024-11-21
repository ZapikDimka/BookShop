from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,  # Дозволяємо null тимчасово
        blank=True  # Дозволяємо blank тимчасово
    )

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    category = models.ForeignKey(
        Category,
        related_name='bookmarks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    favorite = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        null=True,  # Дозволяємо null тимчасово
        blank=True  # Дозволяємо blank тимчасово
    )

    def __str__(self):
        return self.title
