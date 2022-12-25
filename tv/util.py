import datetime
import requests
from .models import Show

def get_show(show_id):
    """Get data on the shows with the specified ID from the TV Maze API."""
    
    url = f"https://api.tvmaze.com/shows/{show_id}"
    show_data = requests.get(url).json()
    if show_data["status"] != 404:
        show = create_show(show_data)
        return show


def get_shows(query):
    """Get data on all shows matching the search query from the TV Maze API."""

    url = f"https://api.tvmaze.com/search/shows?q={query}"
    results = requests.get(url).json()
    all_show_data = [result["show"] for result in results]
    shows = [create_show(show_data) for show_data in all_show_data]
    return shows


def create_show(show_data):
    """Create a Show object and add it to the database."""

    return Show.objects.get_or_create(
        id=show_data["id"],
        name=show_data["name"],
        image=get_image(show_data),
        summary=show_data["summary"],
        premiered=show_data["premiered"],
        url=show_data["url"],
        status=show_data["status"],
        channel=get_channel(show_data),
        startyear=get_start_year(show_data),
        endyear=get_end_year(show_data),
        mostrecentairdate=get_most_recent_airdate(show_data),
    )[0]


def get_image(show_data):
    """Get the image of the show."""
    if "image" in show_data and show_data["image"]:
        if "medium" in show_data["image"] and show_data["image"]["medium"]:
            return show_data["image"]["medium"]


def get_channel(show_data):
    """Set the channel of the show."""

    if "network" in show_data and show_data["network"]:
        return show_data["network"]["name"]
    elif "webChannel" in show_data and show_data["webChannel"]:
        return show_data["webChannel"]["name"]


def get_start_year(show_data):
    """Set the start year of the show."""

    try:
        return show_data["premiered"].split("-")[0]
    except AttributeError:
        return


def get_most_recent_airdate(show_data):
    """Set the most recent episode of the show."""

    if "nextepisode" in show_data["_links"] and show_data["_links"]["nextepisode"]:
        episode_url = show_data["_links"]["nextepisode"]["href"]
        episode = requests.get(episode_url).json()
        return episode["airdate"]
    elif "previousepisode" in show_data["_links"] and show_data["_links"]["previousepisode"]:
        episode_url = show_data["_links"]["previousepisode"]["href"]
        episode = requests.get(episode_url).json()
        return episode["airdate"]


def get_end_year(show_data):
    """Set the end year of the show."""

    try:
        this_year = datetime.date.today().year
        end_year = get_most_recent_airdate(show_data).split("-")[0]
        if int(end_year) < this_year:
            return end_year
    except AttributeError:
        return