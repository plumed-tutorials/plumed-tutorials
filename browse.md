Browse the lessons 
-----------------------------
The lessons that have been submitted to the PLUMED-SCHOOL are listed below.  PLUMED-SCHOOL monitors whether PLUMED input files in these lessons are compatible with the current and development 
versions of the code and integrates links from these files to the PLUMED manual.

{:#browse-table .display}
| ID | Name | Contributor |
|:--------:|:--------:|:---------:|
{% for item in site.data.lessons %}| [{{ item.id }}]({{ item.path }}) | {{ item.name }} | {{ item.contributor | split: " " | last}} {{ item.contributor | split: " " | first | slice: 0}}. |
{% endfor %}

<script>
$(document).ready(function() {
var table = $('#browse-table').DataTable({
  "dom": '<"search"f><"top"il>rt<"bottom"Bp><"clear">',
  language: { search: '', searchPlaceholder: "Search project..." },
  buttons: [
        'copy', 'excel', 'pdf'
  ],
  "order": [[ 0, "desc" ]]
  });
$('#browse-table-searchbar').keyup(function () {
  table.search( this.value ).draw();
  });
});
</script>
