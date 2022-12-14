from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Show(models.Model):

    name = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.name}"
