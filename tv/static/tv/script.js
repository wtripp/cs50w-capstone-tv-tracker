/*

document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#search').addEventListener('submit', function(event) {
    event.preventDefault();
    search();
  });

});

function search() {

    const query = document.getElementsByName('q')[0].value;
    const url = `https://api.tvmaze.com/search/shows?q=${query}`;
    fetch(url)
    .then(response => response.json())
    .then(results => {

      fetch('search', {
        method: 'POST',
        body: JSON.stringify({
          results: results,
        })
      })
      .catch(error => {
        console.log('Error: ', error);
      });

    })
    .catch(error => {
        console.log('Error: ', error);
    });
}

*/