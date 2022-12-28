document.addEventListener('DOMContentLoaded', function() {

    const filterGroupNames = ["channel", "status"];
    filterGroupNames.forEach(filterGroupName => {
      const filterGroup = create_filter_group(filterGroupName);
      const filters = filterGroup.querySelectorAll(".form-check-input");
      filters.forEach(filter => {
        filter.addEventListener('change', () => {
          toggle_checkbox(filter);
          apply_filters(filterGroupNames);
      });
    });
  });
});


function create_filter_group(filterGroupName) {
/* Create the filter check boxes for the specified filter group. */

  // Get the filter names for the group.
  const nodes = document.querySelectorAll(`.show-${filterGroupName}`);
  const values = Array.from(nodes).map(item => item.textContent);
  const uniqueValues = [...new Set(values)];

  // Create the check boxes for those filter names.
  const filterGroup = document.getElementById(`${filterGroupName}-filters`);
  for (const value of uniqueValues) {

    // Check box area
    const div = document.createElement("div");
    div.setAttribute("class","form-check form-check-inline");

    // Check box
    const input = document.createElement("input");
    input.setAttribute("class","form-check-input filter");
    input.setAttribute("type","checkbox");
    input.setAttribute("value","");
    input.setAttribute("id",`${value}-filter`);
    input.setAttribute("checked","");
    div.appendChild(input);

    // Check box label
    const label = document.createElement("label");
    label.setAttribute("class","form-check-label");
    label.setAttribute("for",`${value}-filter`);
    label.innerHTML = value;
    div.appendChild(label);

    // Add check box to group.
    filterGroup.appendChild(div);
  };

  return filterGroup;
}


function toggle_checkbox(filter) {

  if (filter.hasAttribute("checked")) {
    filter.removeAttribute("checked");
  } else {
    filter.setAttribute("checked","");
  }
}


function apply_filters(filterGroupNames) {
  /* Apply the filtering to the filter group. */

  const summaries = document.querySelectorAll(".show-summary");
  summaries.forEach(summary => {

    const display_summary = check_for_display(summary, filterGroupNames);

    if (display_summary) {
      summary.style.display = "block";
    } else {
      summary.style.display = "none";
    }

  }); 
}


function check_for_display(summary, filterGroupNames) {
/* Returns true if the show summary should be displayed. */

  const filter_checks = [];
  filterGroupNames.forEach(filterGroupName => {
  
    const filterGroup = document.getElementById(`${filterGroupName}-filters`);
    const filters = filterGroup.querySelectorAll(".form-check");
    filters.forEach(filter => {
      const isChecked = filter.querySelector(".form-check-input").hasAttribute("checked");
      const labelText = filter.querySelector(".form-check-label").textContent;
      const showDataText = summary.querySelector(`.show-${filterGroupName}`).textContent;

      if (labelText === showDataText) {
        filter_checks.push(isChecked);
      }
    });
  });

  return filter_checks.every(check => check === true);

}