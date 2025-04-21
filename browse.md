Browse the lessons 
-----------------------------
The lessons that have been submitted to the PLUMED-TUTORIALS are listed below.  PLUMED-TUTORIALS monitors whether PLUMED input files in these lessons are compatible with the current and development
versions of the code and integrates links from these files to the PLUMED manual.  Inputs in the tutorials listed below were last tested on {{ site.data.date.date }}.

Suggestions for an order to work through the tutorials can be found [here](summarygraph.md).
A complete bibliography of papers connected to these lessons can be found [here](bibliography.md).

{% raw %}
<div id="diplay_description"> </div>
{% endraw %}

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
      document.getElementById("diplay_description").innerHTML = "";
  } else if( searchfor[0]=="action" ) {
      fetch("./syntax.0.json")
        .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
        })
        .then( data => document.getElementById("diplay_description").innerHTML = "<b>Showing lessons that use:</br></br>" + searchfor[1] + " (action): " + data[ searchfor[1] ]["description"] + " <a href=\"" + data[ searchfor[1] ]["hyperlink"] + "\">More details</a></b>")
      table.columns(5).search( "\\b" + searchfor[1] + "\\b", true, false, false ).draw();
  } else if( searchfor[0]=="module" ) {
      fetch("./syntax.0.json")
        .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
        })
        .then( data => document.getElementById("diplay_description").innerHTML = "<b>Showing lessons that use:</br></br>" + searchfor[1] + " (module): " + data["modules"][ searchfor[1] ]["description"] + " <a href=\"" + data["modules"][ searchfor[1] ]["hyperlink"] + "\">More details</a></b>")
      table.columns(6).search( "\\b" + searchfor[1] + "\\b", true, false, false ).draw();
  }
});
</script>
