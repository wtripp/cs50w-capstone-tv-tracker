const button = document.getElementById('navSortFilterButton');
const menu = document.getElementById('navSortFilter');

button.addEventListener('click', function () {
  menu.classList.toggle('show');
  button.classList.toggle('collapsed');
});