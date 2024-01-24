import json
import yaml

# Read in the syntax file to get the list of all actions
f = open('syntax.0.json')
syntax = json.load(f)
f.close()
print("Read python syntax")

# Make a dictionary that contains all the actions
counts = {}
for key in syntax :
    if key=="vimlink" or key=="replicalink" or key=="groups" : continue
    counts[key] = 0

print("Built initial counts")

# Now read the yaml 
with open("lessons.yml", "r") as stream:
    try:
        lessons = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print("Read all lessons")

# And work through the items in the yaml file
# Counting number of actions used in each 
for l in lessons :
    if l["actions"] : 
       for a in l["actions"].split() : 
          if a in counts.keys() : counts[a] += 1 

print("Obtained final action counts")

# Create the table summarising all the action counts
of = open("actioncount.md","w")
of.write("# Usage of actions\n\n")
of.write("<canvas id=\"myChart\" style=\"width:100%;\"></canvas>\n\n")
of.write("<script>\n")
allk, alln = [], []
for k, v in counts.items() : 
    allk.append(k)
    alln.append(v)
of.write("var xValues = " + str(allk) + ";\n")
of.write("var yValues = " + str(alln) + ";\n")
of.write("var barColors = \"green\";\n\n")
of.write("new Chart(\"myChart\", {\n")
of.write("  type: \"horizontalBar\",\n")
of.write("  data: {\n")
of.write("    labels: xValues,\n")
of.write("    datasets: [{\n")
of.write("      backgroundColor: barColors,\n")
of.write("      data: yValues\n")
of.write("    }]\n")
of.write("  },\n")
of.write("  options: {\n")
of.write("    legend: {display: false},\n")
of.write("    title: {\n")
of.write("      display: true,\n")
of.write("      text: \"Number of lessons using this action\"\n")
of.write("    }\n")
of.write("  }\n")
of.write("});\n")
of.write("</script>\n")
of.close()
