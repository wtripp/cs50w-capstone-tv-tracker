from django.urls import path

from . import views

app_name = "tv"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("show/<int:show_id>/<str:show_name>", views.show, name="show"),

    # API routes
    path("track/<int:show_id>", views.track, name="track"),
    path("untrack/<int:show_id>", views.untrack, name="untrack"),

]
