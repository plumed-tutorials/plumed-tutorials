# Usage of actions

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
var barColors = "green";

new Chart("myChart", {
  type: "horizontalBar",
  data: 
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
