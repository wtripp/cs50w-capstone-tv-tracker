import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime

from .models import User, Show

def index(request):
    return render(request, "tv/index.html")


def search(request):

    query = request.GET.get("q")
    url = f"https://api.tvmaze.com/search/shows?q={query}"
    results = requests.get(url).json()

    shows = [result["show"] for result in results]
    for show in shows:

        # Set network channel
        if "network" in show and show["network"]:
            show["channel"] = show["network"]["name"]
        elif "webChannel" in show and show["webChannel"]:
            show["channel"] = show["webChannel"]["name"]
        else:
            show["channel"] = None

        # Set start year
        show["startyear"] = None
        try:
            start_year = show["premiered"].split("-")[0]
            show["startyear"] = start_year
        except AttributeError:
            pass

        # Set most recent episode airdate
        if "nextepisode" in show["_links"] and show["_links"]["nextepisode"]:
            episode_url = show["_links"]["nextepisode"]["href"]
            episode = requests.get(episode_url).json()
            show["mostrecentairdate"] = episode["airdate"]
        if "previousepisode" in show["_links"] and show["_links"]["previousepisode"]:
            episode_url = show["_links"]["previousepisode"]["href"]
            episode = requests.get(episode_url).json()
            show["mostrecentairdate"] = episode["airdate"]
        else:
            show["mostrecentairdate"] = None
        
        # Set end year
        show["endyear"] = None
        try:
            this_year = datetime.date.today().year
            end_year = show["mostrecentairdate"].split("-")[0]
            if int(end_year) < this_year:
                show["endyear"] = end_year
        except AttributeError:
            pass
        
    return render(request, "tv/search.html", {
        "shows": shows
    })


def show(request, show_id, show_name):
    return render(request, "tv/show.html", {
        "id": show_id,
        "name": show_name,
    })
    


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