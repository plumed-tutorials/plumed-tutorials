import os
import sys
import json
import getopt
import requests
import subprocess
from pathlib import Path
from datetime import date 
from bs4 import BeautifulSoup
import networkx as nx

def create_map( URL ) :
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    script_elements = soup.find_all("script")
    for script in script_elements : 
        lines = script.text.splitlines()
        for line in lines :
            if "var" not in line or "for" in line : continue
            if "xValues" in line and "=" in line :
               xdata = json.loads( line.split("=")[1].replace(";","") )
            if "yValues" in line and "=" in line :
               ydata = json.loads( line.split("=")[1].replace(";","") )
    
    return dict(map(lambda i,j : (i,j) , xdata,ydata))

def createModuleGraph( plumed_rootdir ) :
   # Get all the module dependencies
   # First from includes
   requires = {}
   for mod in plumed_rootdir.glob("src/*/Makefile" ) :
       if thismodule not in requires.keys() : requires[thismodule] = set()
       with open(mod) as file :
            modules = []
            for line in file :
                if re.search("USE=", line ) :
                   modules = line.replace("USE=","").split()
                   break
            startnode = modulelist[mod.parts[2]]
            for conn in modules : requires[thismodule].add( conn )
       
   # And from shortcuts
   for key, value in plumed_syntax.items() :
       if "module" not in value : continue
       thismodule = value["module"]
       if thismodule not in requires.keys() : requires[thismodule] = set()
       if "needs" in value :
          for req in value["needs"] :
              if plumed_syntax[req]["module"]!=thismodule : requires[thismodule].add( plumed_syntax[req]["module"] )

   of = open("manual.md", "w")
   ghead = """
The PLUMED CODE
------------------------

PLUMED is a community-developed code that can be used to incorporate additional functionality into multiple molecular dynamics codes and for analysing 
trajectories. PLUMED is a composed of a modules that contain a variety of different functionalities but that share a common basic syntax. You can find 
a list of the modules that are available within PLUMED in the following graph. The graph also shows the interdependencies between the various modules. 
If you click on the modules in the graph module-specific information will open.

Each module contains implementations of a number of actions. You can find a list of all the actions implemented in in PLUMED [here](actionlist.md).

If you are completely unfamiliar with PLUMED we would recommend that you start by working through [the following tutorial](https://plumed-school.github.io/lessons/21/001/data/NAVIGATION.html). 

```mermaid
   """
   of.write(ghead + "\n")
   of.write("flowchart TD\n")

   k, translate = 0, {}
   for key, data in requires.items() :
       of.write(  str(k) + "(\"" + key + "\")\n")
       translate[key] = k
       k = k + 1
   
   # And create the graph
   G = nx.DiGraph()
   for key, data in requires.items() :
       for dd in data : G.add_edge( translate[key], translate[dd] )

   # And create the graph showing the modules
   pG = nx.minimum_spanning_arborescence(G)
   for edge in pG.edges() :
       of.write( str(edge[0]) + "-->" + str(edge[1]) + ";\n" )

   # And finally the click stuff
   k=0
   for key, data in requires.items() :
       of.write("click " + str(k) + " \"" + key + ".md\" \"Information about the module [Authors: list of authors]\"\n" )
       k = k + 1

   of.write("```\n")
   of.close()

def createModulePage( modname, neggs, nlessons ) :
    with open( modname + ".md", "w") as f :
         f.write("# Module: " + modname + "\n\n")
         f.write("| Description    | Usage |\n")
         f.write("|:--------|:--------:|\n")
         f.write("| Description of module | ")
         if nlessons>0 :
            f.write("[![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-" + str(nlessons) + "-green.svg)](https://plumed-school.github.io/browse.html?search=" + modname + ")")
         else : 
            f.write("![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-0-red.svg)")
         if neggs>0 : 
            f.write("[![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-" + str(neggs) + "-green.svg)](https://www.plumed-nest.org/browse.html?search=" + modname + ")")
         else : 
            f.write("![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-0-red.svg)")
         f.write("|\n\n")
         f.write("## Actions \n\n")
         f.write("The following actions are part of this module\n\n")
         f.write("{% assign moduleacts = site.data.actionlist | where: \"module\", \"" + modname + "\" %}\n")
         f.write("{:#browse-table .display}\n")
         f.write("| Name | Description |\n")
         f.write("|:--------:|:--------|\n")
         f.write("{% for item in moduleacts %}| [{{ item.name }}]({{ item.path }}) | {{ item.description }} |\n")
         f.write("{% endfor %}\n")
         f.write("<script>\n")
         f.write("$(document).ready(function() {\n")
         f.write("var table = $('#browse-table').DataTable({\n")
         f.write("  \"dom\": '<\"search\"f><\"top\"il>rt<\"bottom\"Bp><\"clear\">',\n")
         f.write("  language: { search: '', searchPlaceholder: \"Search project...\" },\n")
         f.write("  buttons: [\n")
         f.write("        'copy', 'excel', 'pdf'\n")
         f.write("  ],\n")
         f.write("  \"order\": [[ 0, \"desc\" ]]\n")
         f.write("  });\n")
         f.write("$('#browse-table-searchbar').keyup(function () {\n")
         f.write("  table.search( this.value ).draw();\n")
         f.write("  });\n")
         f.write("  hu = window.location.search.substring(1);\n")
         f.write("  searchfor = hu.split(\"=\");\n")
         f.write("  if( searchfor[0]==\"search\" ) {\n") 
         f.write("      table.search( searchfor[1] ).draw();\n")
         f.write("  }\n")
         f.write("});\n")
         f.write("</script>\n")

def createActionPage( action, value, neggs, nlessons, actdb ) :
    with open("manual/" + action + ".md", "w") as f : 
         f.write("# Action: " + action + "\n\n")
         f.write("| Description    | Usage |\n")
         f.write("|:--------|:--------:|\n") 
         f.write("| " + value["description"] + " | ")
         if nlessons>0 : 
            f.write("[![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-" + str(nlessons) + "-green.svg)](https://plumed-school.github.io/browse.html?search=" + action + ")")
         else : 
            f.write("![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-0-red.svg)")
         if neggs>0 : 
            f.write("[![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-" + str(neggs) + "-green.svg)](https://www.plumed-nest.org/browse.html?search=" + action + ")")
         else : 
            f.write("![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-0-red.svg)") 
         if "output" in value["syntax"] and "value" in value["syntax"]["output"] : 
            f.write("|\n | **output value** | **type** |\n")
            f.write("| " + value["syntax"]["output"]["value"]["description"] + " | scalar |\n\n" )
         else : 
            f.write(" | \n\n")

         if "output" in value["syntax"] and len(value["syntax"]["output"].keys())>1 :
            f.write("## Output components\n\n")
            if "value" in value["syntax"]["output"] and len(value["syntax"]["output"])==1 :
               pass
            else :
               onlydefault = True
               for key, docs in value["syntax"]["output"].items() :
                   if docs["flag"]!="default" : onlydefault = False
               if onlydefault :
                  f.write("This action calculates the quantities in the following table.  These quantities can be referenced elsewhere in the input by using this Action's label followed by a dot and the name of the quantity required from the list below.\n\n")
                  f.write("| Name | Type | Description |\n")
                  f.write("|:-------|:-----|:-------|\n")
                  for key, docs in value["syntax"]["output"].items() :
                      if key=="value" : continue 
                      f.write("| " + key + " | scalar | " + docs["description"] + " | \n") 
                  f.write("\n\n")
               else : 
                  f.write("This action can calculate the quantities in the following table when the associated keyword is included in the input for the action. These quantities can be referenced elsewhere in the input by using this Action's label followed by a dot and the name of the quantity required from the list below.\n\n")
                  f.write("| Name | Type | Keyword | Description |\n")
                  f.write("|:-------|:-----|:----:|:-------|\n")
                  for key, docs in value["syntax"]["output"].items() :
                      if key=="value" : continue 
                      f.write("| " + key + " | scalar | " + docs["flag"] + " | " + docs["description"] + " | \n")
                  f.write("\n\n")
         
         f.write("## Input\n\n")
         f.write("The input for this action is specified using one or more of the keywords in the following table.\n\n")
         f.write("| Keyword |  Description |\n")
         f.write("|:-------|:-----------|\n")
         for key, docs in value["syntax"].items() :
             if key=="output" : continue
             if docs["type"]=="atoms" or key=="ARG" : f.write("| " + key + " | " + docs["description"] + " |\n")
         f.write("\n\n")

         f.write("## Further details and examples \n")
         f.write("Information for the manual from the code would go in here \n")
         f.write("## Syntax \n")
         f.write("The following table describes the keywords and options that can be used with this action \n\n")
         f.write("| Keyword | Type | Default | Description |\n")
         f.write("|:-------|:----:|:-------:|:-----------|\n")
         for key, docs in value["syntax"].items() : 
             if key=="output" : continue 
             if docs["type"]=="atoms" or key=="ARG" : f.write("| " + key + " | input | none | " + docs["description"] + " |\n") 
         for key, docs in value["syntax"].items() : 
             if key=="output" or key=="ARG" : continue
             if docs["type"]=="compulsory"  : f.write("| " + key + " | compulsory | none | " + docs["description"] + " |\n") 
         for key, docs in value["syntax"].items() :
             if key=="output" or key=="ARG" : continue
             if docs["type"]=="flag" : f.write("| " + key + " | optional | false | " + docs["description"] + " |\n")
             if docs["type"]=="optional" : f.write("| " + key + " | optional | not used | " + docs["description"] + " |\n")

    print("- name: " + action, file=actdb)
    print("  path: manual/" + action + ".html", file=actdb)
    print("  description: " + value["description"], file=actdb)    
    print("  module: " + value["module"], file=actdb)

if __name__ == "__main__" : 
   nreplicas, replica, argv = 1, 0, sys.argv[1:]
   try:
       opts, args = getopt.getopt(argv,"hn:r:",["nreplicas=","replica="])
   except:
      print('build_manual.py -n <nreplicas> -r <replica number>')

   for opt, arg in opts:
      if opt in ['-h'] :
         print('compile.py -n <nreplicas> -r <replica number>')
         sys.exit()
      elif opt in ["-n", "--nreplicas"]:
         nreplicas = int(arg)
      elif opt in ["-r", "--replica"]:
         replica = int(arg)
   print("RUNNING", nreplicas, "REPLICAS. THIS IS REPLICA", replica )
   nest_map = create_map("https://www.plumed-nest.org/summary.html")
   school_map = create_map("https://plumed-school.github.io/summary.html")
   # Print the date to the data directory
   today = { "date": date.today().strftime('%B %d, %Y') }
   df = open("_data/date.json","w")
   json.dump( today, df, indent=4 )
   df.close()
   # Get list of plumed actions from syntax file
   cmd = ['plumed_master', 'info', '--root']
   plumed_info = subprocess.run(cmd, capture_output=True, text=True )
   keyfile = plumed_info.stdout.strip() + "/json/syntax.json"
   plumed_rootdir = Path(plumed_info.stdout.strip())
   with open(keyfile) as f :
       try:
          plumed_syntax = json.load(f)
       except ValueError as ve:
          raise InvalidJSONError(ve)
   # Create a page for each action
   os.mkdir("manual")
   with open("_data/actionlist" + str(replica) + ".yml","w") as actdb :
       print("# file containing action database.",file=actdb) 
 
       k=0
       for key, value in plumed_syntax.items() :
           if key=="vimlink" or key=="replicalink" or key=="groups" or key!=value["displayname"] : continue
           # Now create the page contents
           if k%nreplicas==replica : 
              neggs, nlessons = 0, 0
              if key in nest_map.keys() : neggs = nest_map[key]
              if key in school_map.keys() : nlessons = school_map[key] 
              createActionPage( key, value, neggs, nlessons, actdb ) 
           k = k + 1

   # Create a list of modules
   modules = {}
   for key, value in plumed_syntax.items() :  
     if key=="vimlink" or key=="replicalink" or key=="groups" or key!=value["displayname"] : continue
     if value["module"] not in modules.keys() :
        modules[value["module"]] = { "neggs": nest_map[key], "nlessons": school_map[key] }
     else : modules[value["module"]]["neggs"], modules[value["module"]]["nlessons"] = modules[value["module"]]["neggs"] + nest_map[key], modules[value["module"]]["nlessons"] + school_map[key]

   # And create each module page
   for module, value in modules.items() : createModulePage( module, value["neggs"], value["nlessons"] )
   # Create the graph that shows all the modules
   createModuleGraph( plumed_rootdir )
