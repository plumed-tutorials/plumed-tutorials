import os
import sys
import json
import getopt
import requests
import subprocess
from bs4 import BeautifulSoup

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

def createActionPage( key, value, neggs, nlessons, actdb ) :
    with open("manual/" + key + ".md", "w") as f : 
         f.write("# Action: " + key + "\n\n")
         f.write("| Description    | Usage |\n")
         f.write("|:--------:|:--------:|\n") 
         f.write("| " + value["description"] + " | ")
         if nlessons>0 : 
            f.write("[![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-" + str(nlessons) + "-green.svg)](https://plumed-school.github.io/browse.html?search=" + key + ")")
         else : 
            f.write("![used in " + str(nlessons) + " tutorials](https://img.shields.io/badge/tutorials-0-red.svg)")
         if neggs>0 : 
            f.write("[![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-" + str(neggs) + "-green.svg)](https://www.plumed-nest.org/browse.html?search=" + key + ")")
         else : 
            f.write("![used in " + str(neggs) + " eggs](https://img.shields.io/badge/nest-0-red.svg)") 
         f.write(" | \n\n## Further details and examples \n")
         f.write("Information for the manual from the code would go in here \n")
         f.write("## Syntax \n")
         f.write("The following table describes the keywords and options that can be used with this action \n")
         f.write("| Keyword | Type | Default | Description |\n")
         f.write("|:-------:|:----:|:-------:|:-----------:|\n")
         for key, docs in value["syntax"].items() : 
             if key=="output" : continue 
             if docs["type"]=="atoms" or key=="ARG" : f.write("| " + key + " | input | none | " + docs["description"] + " |\n") 
         for key, docs in value["syntax"].items() : 
             if key=="output" : continue
             if docs["type"]=="compulsory"  : f.write("| " + key + " | compulsory | none | " + docs["description"] + " |\n") 
         for key, docs in value["syntax"].items() :
             if key=="output" : continue
             if docs["type"]=="flag" : f.write("| " + key + " | optional | false | " + docs["description"] + " |\n")
             if docs["type"]=="optional" : f.write("| " + key + " | optional | not used | " + docs["description"] + " |\n")

    print("- name: " + key, file=actdb)
    print("  path: manual/" + key + ".html", file=actdb)
    print("  description: replace with proper description from syntax", file=actdb)
    #print("  description: " + value["description"], file=actdb)    


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
   # Get list of plumed actions from syntax file
   cmd = ['plumed_master', 'info', '--root']
   plumed_info = subprocess.run(cmd, capture_output=True, text=True )
   keyfile = plumed_info.stdout.strip() + "/json/syntax.json"
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
           if key=="vimlink" or key=="replicalink" or key=="groups" : continue
           # Now create the page contents
           if k%nreplicas==replica : 
              neggs, nlessons = 0, 0
              if key in nest_map.keys() : neggs = nest_map[key]
              if key in school_map.keys() : nlessons = school_map[key] 
              createActionPage( key, value, neggs, nlessons, actdb ) 
           k = k + 1

