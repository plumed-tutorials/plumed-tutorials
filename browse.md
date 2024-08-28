Browse the lessons 
-----------------------------
The lessons that have been submitted to the PLUMED-TUTORIALS are listed below.  PLUMED-TUTORIALS monitors whether PLUMED input files in these lessons are compatible with the current and development
versions of the code and integrates links from these files to the PLUMED manual.  Inputs in the tutorials listed below were last tested on {{ site.data.date.date }}.

Suggestions for an order to work through the tutorials can be found [here](summarygraph.md).

{:#browse-table .display}
| ID | Name | Instructors | Description | Tags | Actions | Modules |
|:--------:|:--------:|:---------:|:---------:|:---------:|:---------:|:---------:|
{% for item in site.data.lessons %}| {{ item.id }} | [{{ item.title }}]({{ item.path }}) | {{ item.instructors }} | {{ item.description }} | {{ item.tags }} | {{ item.actions }} | {{ item.modules }} |
{% endfor %}


<script>
$(document).ready(function() {
var table = $('#browse-table').DataTable({
  "dom": '<"search"f><"top"il>rt<"bottom"Bp><"clear">',
  language: { search: '', searchPlaceholder: "Search project..." },
  buttons: [
        'copy', 'excel', 'pdf'
  ],
  "columnDefs": [ 
     { "targets": 4, "visible": false },
     { "targets": 5, "visible": false },
     { "targets": 6, "visible": false }
  ],
  "order": [[ 0, "desc" ]]
  });
$('#browse-table-searchbar').keyup(function () {
  table.search( this.value ).draw();
  });
  hu = window.location.search.substring(1);
  searchfor = hu.split("=");
  if( searchfor[0]=="search" ) {
      table.search( searchfor[1].replace("%20"," ") ).draw();
  }
});
</script>
