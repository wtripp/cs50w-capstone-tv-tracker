import datetime
import requests

def get_show(show_id):
    """Get data on the shows with the specified ID from the TV Maze API."""
    
    url = f"https://api.tvmaze.com/shows/{show_id}"
    show = requests.get(url).json()
    add_show_fields(show)
    return show


def get_shows(query):
    """Get data on all shows matching the search query from the TV Maze API."""

    url = f"https://api.tvmaze.com/search/shows?q={query}"
    results = requests.get(url).json()
    shows = [result["show"] for result in results]
    for show in shows:
        add_show_fields(show)
    return shows


def add_show_fields(show):
    """Add additional fields to the show."""

    set_channel(show)
    set_start_year(show)
    set_most_recent_episode(show)
    set_end_year(show)
    set_url_name(show)


def set_start_year(show):
    """Set the start year of the show."""

    show["startyear"] = None
    try:
        start_year = show["premiered"].split("-")[0]
        show["startyear"] = start_year
    except AttributeError:
        pass


def set_channel(show):
    """Set the channel of the show."""

    show["channel"] = None
    if "network" in show and show["network"]:
        show["channel"] = show["network"]["name"]
    elif "webChannel" in show and show["webChannel"]:
        show["channel"] = show["webChannel"]["name"]


def set_most_recent_episode(show):
    """Set the most recent episode of the show."""

    show["mostrecentairdate"] = None
    if "nextepisode" in show["_links"] and show["_links"]["nextepisode"]:
        episode_url = show["_links"]["nextepisode"]["href"]
        episode = requests.get(episode_url).json()
        show["mostrecentairdate"] = episode["airdate"]
    elif "previousepisode" in show["_links"] and show["_links"]["previousepisode"]:
        episode_url = show["_links"]["previousepisode"]["href"]
        episode = requests.get(episode_url).json()
        show["mostrecentairdate"] = episode["airdate"]


def set_end_year(show):
    """Set the end year of the show."""

    show["endyear"] = None
    try:
        this_year = datetime.date.today().year
        end_year = show["mostrecentairdate"].split("-")[0]
        if int(end_year) < this_year:
            show["endyear"] = end_year
    except AttributeError:
        pass


def set_url_name(show):
    """Set the name of the show to use in the URL"""

    show["urlname"] = show["name"].lower().replace(" ","-")