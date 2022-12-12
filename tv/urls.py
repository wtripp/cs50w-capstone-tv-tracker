from django.urls import path

from . import views

app_name = "tv"
urlpatterns = [
    path("", views.index, name="index"),
]
