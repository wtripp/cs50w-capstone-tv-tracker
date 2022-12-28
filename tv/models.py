from django.contrib.auth.models import AbstractUser
from django.db import models

class Show(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):

    shows = models.ManyToManyField(Show, blank=True, related_name="trackers")

    def __str__(self):
        return f"{self.username}"