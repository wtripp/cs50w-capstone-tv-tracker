from django.contrib.auth.models import AbstractUser
from django.db import models

class Show(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):

    shows = models.ManyToManyField(Show, related_name="trackers")

    def __str__(self):
        return f"{self.username}"