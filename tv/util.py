import datetime
import requests

def get_show(show_id):
    """Get data on the shows with the specified ID from the TV Maze API."""
    
    url = f"https://api.tvmaze.com/shows/{show_id}"
    data = requests.get(url).json()
    if data["status"] != 404:
        show = update_show(data)
        return show


def get_shows(query):
    """Get data on all shows matching the search query from the TV Maze API."""

    url = f"https://api.tvmaze.com/search/shows?q={query}"
    results = requests.get(url).json()
    shows = [update_show(result["show"]) for result in results]
    return shows


def update_show(data):
    """Update the show data with additional fields."""

    data["image"] = get_image(data)
    data["channel"] = get_channel(data)
    data["startyear"] = get_start_year(data)
    data["endyear"] = get_end_year(data)
    data["mostrecentairdate"] = get_most_recent_airdate(data)

    return data


def get_image(data):
    """Get the image of the show."""
    if "image" in data and data["image"]:
        if "medium" in data["image"] and data["image"]["medium"]:
            return data["image"]["medium"]


def get_channel(data):
    """Set the channel of the show."""

    if "network" in data and data["network"]:
        return data["network"]["name"]
    elif "webChannel" in data and data["webChannel"]:
        return data["webChannel"]["name"]


def get_start_year(data):
    """Set the start year of the show."""

    try:
        return data["premiered"].split("-")[0]
    except AttributeError:
        return


def get_most_recent_airdate(data):
    """Set the most recent episode of the show."""

    if "nextepisode" in data["_links"] and data["_links"]["nextepisode"]:
        episode_url = data["_links"]["nextepisode"]["href"]
        episode = requests.get(episode_url).json()
        return episode["airdate"]
    elif "previousepisode" in data["_links"] and data["_links"]["previousepisode"]:
        episode_url = data["_links"]["previousepisode"]["href"]
        episode = requests.get(episode_url).json()
        return episode["airdate"]
    else:
        return "0000-00-00"


def get_end_year(data):
    """Set the end year of the show."""

    try:
        this_year = datetime.date.today().year
        end_year = get_most_recent_airdate(data).split("-")[0]
        if int(end_year) < this_year:
            return end_year
    except AttributeError:
        return