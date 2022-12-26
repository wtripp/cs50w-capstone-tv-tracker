document.addEventListener('DOMContentLoaded', function() {

  const nameSortButton = document.getElementById("name-sort");
  const channelSortButton = document.getElementById("channel-sort");
  const airdateSortButton = document.getElementById("airdate-sort");

  //sort_by_name(nameSortButton);
  sort_shows(airdateSortButton, ".show-airdate");

  document.querySelectorAll('.track-button').forEach(button => {
    button.onclick = function() {
        const show = this.closest('[id^="show-"]');
        track(show);

    }
  });

  nameSortButton.addEventListener('click', () => sort_shows(nameSortButton, ".show-name"));
  channelSortButton.addEventListener('click', () => sort_shows(channelSortButton, ".show-channel"));
  airdateSortButton.addEventListener('click', () => sort_shows(airdateSortButton, ".show-airdate"));

});


function track(show) {

  const show_id = parseInt(show.id.replace(/\D/g, "")); 
  const button = show.getElementsByClassName("track-button")[0];
  const track_text = button.innerHTML.trim();

    if (track_text === "Track") {

      fetch(`/track/${show_id}`, {
        method: 'POST'
      })
      .catch(error => {
          console.log('Error: ', error);
      });
      
      button.innerHTML = "Untrack";

  } else if (track_text === "Untrack") {
    
    fetch(`/untrack/${show_id}`, {
      method: 'POST'
    })
    .catch(error => {
        console.log('Error: ', error);
    });

    button.innerHTML = "Track";
  }
}

/* Sort shows based on a sorting class key and update the button toggle. */
function sort_shows(button, sortKeyClass) {

  // Get show summaries.
  const summaries = document.querySelectorAll('.show-summary');

  // Get text of the keys to sort by.
  const keys = [];
  for (const summary of summaries) {
    const key = summary.querySelector(sortKeyClass).textContent;
    keys.push(key);
  }

  // Sort the keys.
  if (sortKeyClass === ".show-airdate") {

    var sortedKeys = keys.sort((a, b) => {
      const dateA = new Date(a);
      const dateB = new Date(b);
      return dateB - dateA;  // most recent dates first
    });

  } else {
    var sortedKeys = keys.sort();
  }

  // Get the summaries sorted by the show titles.
  const sortedSummaries = [];
  for (const sortedKey of sortedKeys) {
    for (const summary of summaries) {
      const key = summary.querySelector(sortKeyClass).textContent;
      if (key === sortedKey) {
        sortedSummaries.push(summary);
      }
    }
  }

  // Sort ascending or descending.
  const parent = summaries[0].parentNode;
  const upArrow = button.querySelector(".up-arrow");
  const downArrow = button.querySelector(".down-arrow");
  let sortAscending = downArrow.classList.contains("active-sort")
  let sortDescending = upArrow.classList.contains("active-sort")
  if (!sortAscending && !sortDescending) {
    sortAscending = true;
  }

  if (sortAscending) {
    for (const sortedSummary of sortedSummaries) {
      parent.insertBefore(sortedSummary, parent.lastChild);
      upArrow.classList.add("active-sort");
      downArrow.classList.remove("active-sort");
    }
    upArrow.style.fontWeight = "bold";
    downArrow.style.fontWeight = "";

  } else if (sortDescending) {
    for (const sortedSummary of sortedSummaries) {
      parent.insertBefore(sortedSummary, parent.firstChild);
      upArrow.classList.remove("active-sort");
      downArrow.classList.add("active-sort");
    }
    upArrow.style.fontWeight = "";
    downArrow.style.fontWeight = "bold";
  }
}