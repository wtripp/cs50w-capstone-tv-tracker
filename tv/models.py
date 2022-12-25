from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Show(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(null=True, blank=True, max_length=50)
    premiered = models.CharField(null=True, blank=True, max_length=50)
    summary = models.CharField(null=True, blank=True, max_length=1000)
    startyear = models.CharField(null=True, blank=True, max_length=10)
    endyear = models.CharField(null=True, blank=True, max_length=10)
    mostrecentairdate = models.CharField(null=True, blank=True, max_length=10)
    image = models.URLField(null=True, blank=True, max_length=200)
    url = models.URLField(null=True, blank=True, max_length=200)
    status = models.CharField(null=True, blank=True, max_length=20)
    trackers = models.ManyToManyField(User, blank=True, related_name="shows")

    def __str__(self):
        return f"{self.name}"
