# Usage of actions

{% assign actionlist = site.data.actioncount | map: "name" %}
{% assign actionnumber = site.data.actioncount | map: "number" %}

<canvas id="myChart" style="width:100%;"></canvas>
<script>
var xValues = [ {{ actionlist | join: '", "' | prepend: '"' | append: '"' }} ];
var yValues = [ {{ actionnumber | join: ", " }} ];
var barColors = \"green\";


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
