document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('.track-button').forEach(button => {
    button.onclick = function() {
        const show = this.closest('[id^="show-"]');
        track(show);

    }
  });
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