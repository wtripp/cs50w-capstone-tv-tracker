document.addEventListener('DOMContentLoaded', function() {

  const url = `https://api.tvmaze.com/shows/${show_id}`
  fetch(url)
  .then(response => response.json())
  .then(show => {
    const episodeUrl = getLatestEpisodeUrl(show);
    getEpisode(episodeUrl).then(episode => {

      document.querySelector("show").id = `show-${show.id}`;
      document.querySelector("show-name").innerHTML = show.name;

      // TODO
      const image = document.querySelector("show-image");

      document.querySelector("show-summary").innerHTML = show.summary;
      document.querySelector(".show-channel").innerHTML = get_channel(show);
      document.querySelector(".show-premiered").innerHTML = show.premiered;

      // TODO
      summary.querySelector(".show-airdate").innerHTML = get_most_recent_episode(episode);

      // TODO
      const showUrl = document.querySelector("show-url");
      
      document.querySelector(".show-status").innerHTML = show.status;

      })
      .catch(error => {
        console.log("Error: ", error);
      });
    });
});


function getLatestEpisodeUrl(show) {
/* Get the URL for the latest episode. */
  if ("nextepisode" in show._links && show._links.nextepisode != null) {
    return show._links.nextepisode.href;
  } else if ("previousepisode" in show._links && show._links.previousepisode != null) {
    return show._links.previousepisode.href;
  } else {
    return "";
  }
}


function get_channel(show) {
/* Get the name of the network or streaming channel. */
  if ("network" in show && show.network != null) {
    return " &mdash; " + show.network.name;
  }
  else if ("webChannel" in show && show.webChannel != null) {
    return " &mdash; " + show.webChannel.name;
  } else {
    return "";
  }
}


function get_most_recent_episode(episode) {
/* Get the most recent episode of a show */

  try {
    return episode.airdate;
  } catch(error) {
    return "0000-00-00";
  }
}


async function getEpisode(url) {
/* Get episode data from the URL endoint */
try {
  const response = await fetch(url);
  const episode = await response.json();
  return episode;
} catch (error) {
  console.log("Error: ", error);
}

};