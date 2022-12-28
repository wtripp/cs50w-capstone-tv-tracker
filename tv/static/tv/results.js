document.addEventListener('DOMContentLoaded', function() {

  const url = `https://api.tvmaze.com/search/shows?q=${query}`
  fetch(url)
  .then(response => response.json())
  .then(results => {
    
    const summaries = document.getElementById("show-summaries");
    const template = document.getElementById("show-summary-template");
    const noResults = document.getElementById("no-results")

    if (results.length) {
      results.forEach(result => {

        const show = result.show;
        const episodeUrl = getLatestEpisodeUrl(show);

        getEpisode(episodeUrl).then(episode => {

          const summary = template.cloneNode(true);
          summary.id = `show-${show.id}`;

          const name = summary.querySelector(".show-name");
          name.innerHTML = show.name;
          const urlShowName = show.name.toLowerCase().replace(/ /g, '-');
          name.setAttribute("href",`/show/${show.id}/${urlShowName}`);

          summary.querySelector(".show-channel").innerHTML = get_channel(show);
          summary.querySelector(".show-year-range").innerHTML = get_year_range(show, episode);
          summary.querySelector(".show-airdate").innerHTML = get_most_recent_episode(episode);
          summary.querySelector(".show-status").innerHTML = show.status;
          summaries.appendChild(summary);

        })
        .catch(error => {
          console.log("Error: ", error);
        });
      });

      summaries.removeChild(noResults);

    } else {
      noResults.innerHTML = "No shows matching that query found.";
    }
    summaries.removeChild(template);

  }).catch(error => {
    console.log("Error: ", error);
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


function get_year_range(show, episode) {
/* Get the range of years that the show ran. */

  const startYear = get_start_year(show);
  const endYear = get_end_year(episode);

  if (startYear && endYear) {
    if (startYear === endYear) {
      return "(" + startYear + ")";
    } else {
      return "(" + startYear + "&ndash;" + endYear + ")";
    }
  } else if (startYear && !endYear) {
    return "(" + startYear + "&ndash;" + ")";
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


function get_start_year(show) {
/* Get the start year of the show. */

  try {
    return show.premiered.split("-")[0];
  } catch(error) {
    return "";
  }
}


function get_end_year(episode) {
/* Get the end year of the show. */

  try {
    const thisYear = new Date().getFullYear().toString();    
    const endYear = episode.airdate.split("-")[0];
    if (parseInt(endYear) < parseInt(thisYear)) {
      return endYear
    } 
  } catch(error) {
    return "";
  };
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