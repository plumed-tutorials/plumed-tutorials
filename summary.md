# Usage of actions

{% assign ninp   = 0 %}
{% assign nfail  = 0 %}
{% assign nfailm = 0 %}
{% assign failed = ''  | split: ',' %}
{% assign missing = '' | split: ',' %}
{% assign preprint = '' | split: ',' %}
{% assign date = "now" | date: "%Y-%m-%d %H:%M" %}

{% for item in site.data.lessons %}
   {% assign ninp   = ninp   | plus: item.ninputs %} 
   {% assign nfail  = nfail  | plus: item.nfail %}
   {% assign nfailm = nfailm | plus: item.nfailm %}
   {% if item.nfail > 0 or item.nfailm > 0 %}
     {% assign failed = failed | push: item %}
   {% endif %}
{% endfor %}

Total number of lessons and PLUMED input files deposited in PLUMED-TUTORIALS, along with number of failed inputs 
with current ({{ site.data.plumed.stable }}) and master PLUMED versions.

|   Date   |  # lessons | # inputs | ![current](https://img.shields.io/badge/current-failed-red.svg) | ![master](https://img.shields.io/badge/master-failed-red.svg) |
| :------: |  :------:  |  :------:  | :------:  | :------:  |
|  {{ date }} | {{ site.data.lessons.size }} | {{ ninp }} | {{ nfail }} | {{ nfailm }} |

__List of lessons with failed tests__

There are {{ failed.size }} tutorials with failing inputs.

{:#browse-table .display}
| ID | Name | Instructors | # inputs | # current | # master |
| :------: |  :------:  |  :------: | :------: | :------:  | :------: |
{% for item in failed %}| {{ item.id }} | [{{ item.title }}]({{ item.path }}) | {{ item.instructors | split: " " | last}} {{ item.instructors | split: " " | first | slice: 0}}. | {{ item.ninputs }} | {{ item.nfail }} | {{ item.nfailm }} |
{% endfor %}

__Action usage chart__

The chart below shows how many lessons make use of each of the available actions in PLUMED.

{% assign actionlist = site.data.actioncount0 | map: "name" %}
{% assign actionno = site.data.actioncount0 | map: "number" %}
{% assign actionno1 = site.data.actioncount1 | map: "number" %}
{% assign nactions=actionno.size %}

{% assign astr="" %}
{% assign ano=actionno[0] | plus: actionno1[i] %}
{% assign astr=astr | append: ano %}
{% for i in (1..nactions) %}
   {% assign ano=actionno[i] | plus: actionno1[i] %}
   {% assign astr=astr | append: ", " | append: ano %}
{% endfor %}

<canvas id="myChart" style="width:100%;"></canvas>

<script>
var xValues = [ {{ actionlist | join: '", "' | prepend: '"' | append: '"' }} ];
var yValues = [ {{ astr }} ];
// do sorting in descending order based on yValues
//1) combine the arrays:
var list = [];
for (var j = 0; j < xValues.length; j++) 
    list.push({'x': xValues[j], 'y': yValues[j]});
//2) sort:
list.sort(function(a, b) {
    return ((a.y > b.y) ? -1 : ((a.y == b.y) ? 0 : 1));
});
//3) separate them back out:
for (var k = 0; k < list.length; k++) {
    xValues[k] = list[k].x;
    yValues[k] = list[k].y;
} 
var barColors = "green";

new Chart("myChart", {
  type: "horizontalBar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    maintainAspectRatio: false,
    legend: {display: false},
    title: {
      display: true,
      text: "Number of lessons using this action"
    }
  }
});
</script>
