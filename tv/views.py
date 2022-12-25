from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from . import util
from .models import User, Show

def index(request):

    if request.user.is_authenticated:
        tracked_shows = Show.objects.filter(trackers=request.user)
        shows = [util.get_show(tracked_show.id) for tracked_show in tracked_shows]
    else:
        shows = []
    return render(request, "tv/index.html", {
        "shows": shows
    })

def search(request):
    query = request.GET.get("q")
    shows = util.get_shows(query)
    return render(request, "tv/search.html", {
        "shows": shows
    })


def show(request, show_id, show_name):
    show = util.get_show(show_id)
    return render(request, "tv/show.html", {
        "show": show,
    })


@csrf_exempt
@login_required
def track(request, show_id):

    if request.method == "POST":

        try:
            show = util.get_show(show_id)
            request.user.shows.add(show)
            request.user.save()
            return HttpResponse(status=204)
        except AttributeError:
            return JsonResponse({"error": "Show to track not found."}, status=404)

    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


@csrf_exempt
@login_required
def untrack(request, show_id):

    try:
        tracked_show = Show.objects.get(pk=show_id)
    except Show.DoesNotExist:
        return JsonResponse({"error": "Show to untrack not found."}, status=404)

    if request.method == "POST":
        request.user.shows.remove(tracked_show)
        request.user.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tv:index"))
        else:
            return render(request, "tv/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tv/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("tv:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tv/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tv/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("tv:index"))
    else:
        return render(request, "tv/register.html")