import yaml
import sys
import getopt
import shutil
import re
import urllib.request
import zipfile
import os
import pathlib
import subprocess
import nbformat
from nbconvert import HTMLExporter 
from contextlib import contextmanager
from PlumedToHTML import test_plumed, get_html

if not (sys.version_info > (3, 0)):
   raise RuntimeError("We are using too many python 3 constructs, so this is only working with python 3")

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def processResource( lessonname, rind, data, rfile ) :
    if data["type"]=="video" :
       ofile = open("data/resources/RESOURCE" + str(rind) + ".md", "w+" ) 
       ofile.write("# " + lessonname + ": " + data["title"] + "\n\n")
       ofile.write( data["description"] + "\n\n" )
       ofile.write("{% raw %}\n")
       ofile.write('<p align="center"><iframe width="630" height="472" src="' + data["location"] + '" frameborder="0" allowfullscreen></iframe></p>\n')
       ofile.write("{% endraw %}\n")
       ofile.close()
    elif data["type"]=="notebook" :
       with open("data/" + data["location"]) as f : 
           mynotebook = nbformat.read( f, as_version=4 )
       # Instantiate the exporter
       exporter = HTMLExporter(template_name = 'classic')
       (body, resources) = exporter.from_notebook_node( mynotebook )
       ofile = open("data/resources/RESOURCE" + str(rind) + ".html", "w+" )
       ofile.write( body ) 
       ofile.close()
    else :
       raise RuntimeError("cannot process resource of type " + data["type"] )
    # Print information on this resource to the resource file
    rfile.write("- title: " + data["title"] + "\n" )
    rfile.write("  path: RESOURCE" + str(rind) + "\n"  )
    rfile.write("  type: " + data["type"] + "\n" )
    rfile.write("  description: " + data["description"] ) 
    if data["type"]=="notebook" : rfile.write(".  A copy of this notebook can be found at " + data["location"] + " in the exercise archive you downloaded") 
    rfile.write("\n" )


def processLesson( path ) :
    f = open( "data/README.md", "r" )
    inp = f.read()
    f.close()
 
    ofile, inplumed, plumed_inp, solutionfile, incomplete = open( "data/README.md", "w+" ), False, "", "", False
    for line in inp.splitlines() :
        # Detect and copy plumed input files 
        if "```plumed" in line :
           inplumed, plumed_inp, solutionfile, incomplete  = True, "", "", False 
        # Test plumed input files that have been found in tutorial 
        elif inplumed and "```" in line : 
           inplumed = False
           if incomplete :
               # Read solution from solution file
               sf = open( "data/" + solutionfile, "r" )
               solution = sf.read() 
               sf.close()
               # Create the full input for PlumedToHTML formatter 
               plumed_inp += "#SOLUTION \n" + solution
           else : 
               solutionfile = "this_input_should_work.dat"
               sf = open( "data/" + solutionfile, "w+" )
               sf.write( plumed_inp )
               sf.close()
           # Test whether the input solution can be parsed
           success = success=test_plumed( "plumed", "data/" + solutionfile )
           success_master=test_plumed( "plumed_master", "data/" + solutionfile  )
           # Find the stable version 
           stable_version=subprocess.check_output('plumed info --version', shell=True).decode('utf-8').strip()
           # Use PlumedToHTML to create the input with all the bells and whistles
           html = get_html( plumed_inp, solutionfile, ("v"+ stable_version,"master"), (success,success_master), ("plumed","plumed_master") )
           # Print the html for the solution
           ofile.write( "{% raw %}\n" + html + "\n {% endraw %} \n" )
        # This finds us the solution file
        elif inplumed and "#SOLUTIONFILE=" in line : solutionfile=line.replace("#SOLUTIONFILE=","")
        elif inplumed :
             if "__FILL__" in line : incomplete = True 
             plumed_inp += line + "\n"
        # Just copy any line that isn't part of a plumed input
        elif not inplumed : ofile.write( line + "\n" )
    ofile.close()

def process_lesson(path,eggdb=None):
    if not eggdb:
        eggdb=sys.stdout

    with cd(path):
        stram = open("lesson.yml", "r")
        config=yaml.load(stram,Loader=yaml.BaseLoader)
        # check fields
        for field in ("url","instructors","title"):
            if not field in config:
               raise RuntimeError(field+" not found")
        print(path,config)

        #if re.match("^.*\.zip$",config["url"]):
        if os.path.exists("download"):
           shutil.rmtree("download")
        os.mkdir("download")
        # try to download
        try:
         urllib.request.urlretrieve(config["url"], 'file.zip')
        except urllib.error.URLError:
         return
        # try to open the zip file
        try:
          zf = zipfile.ZipFile("file.zip", "r")
        except zipfile.BadZipFile:
          return
        zf_namelist = zf.namelist()
        root=list(set([ x.split("/")[0] for x in zf_namelist]))
        # there is a main root directory
        if(len(root)==1 and len(zf_namelist)!=1): root="download/" + root[0]
        # there is not (or special case of one single file)
        else:        root="download/"
        zf.extractall(path="download")
        if os.path.exists("data"):
           shutil.rmtree("data")
        shutil.move(root,"data")

        # Check for the existence of a README file
        if not os.path.exists("data/README.md") : 
           raise RuntimeError("No README.md file found in lesson")
        # Process the readme file to construct the lesson
        processLesson( path )

        # Get the lesson id from the path
        lesson_id = path[8:10] + "." + path[11:14]
        print("- id: '" + lesson_id + "'",file=eggdb)
        print("  title: " + config["title"],file=eggdb)
        print("  path: " + path + "data", file=eggdb)
        print("  instructors: " + config["instructors"], file=eggdb)
 
        # Create a resourcelist file 
        os.mkdir("data/resources")
        rfile = open( "data/resources/RESOURCELIST.md", "w+" )
        rfile.write("# Additional resources: " + config["title"] + "\n\n" )
        rfile.write("The authors of the lesson on [" + config["title"] + "](..) have provided the additional videos and python notebooks in the table below to help you complete the exercises.\n\n")
        rfile.write("{:browse-table .display}\n")
        rfile.write("| Name | Type | Description |\n")
        rfile.write("|:--------:|:--------:|:---------:|\n")
        rfile.write("{% for item in site.data.res" + lesson_id.replace(".","l") + " %}| [{{ item.title }}]({{ item.path }}) | {{ item.type }} | {{ item.description }} | \n")
        rfile.write("{% endfor %}\n\n")
        rfile.write('<script>\n')
        rfile.write('$(document).ready(function() {\n')
        rfile.write("var table = $('#browse-table').DataTable({\n")
        rfile.write("  \"dom\": '<\"search\"f><\"top\"il>rt<\"bottom\"Bp><\"clear\">',\n")
        rfile.write("  language: { search: '', searchPlaceholder: \"Search resource...\"\n },")
        rfile.write("  buttons: [\n")
        rfile.write("        'copy', 'excel', 'pdf'\n")
        rfile.write('  ],\n')           
        rfile.write('  "order": [[ 0, "desc" ]]\n')
        rfile.write('  });\n')       
        rfile.write("$('#browse-table-searchbar').keyup(function () {\n")
        rfile.write('  table.search( this.value ).draw();\n')
        rfile.write('  });\n')   
        rfile.write('});\n')
        rfile.write('</script>\n')
        rfile.close()

        # Now get the resources from the yml file
        rind, ryfile = 1, open( "../../../_data/res" +  lesson_id.replace(".","l") + ".yml", "w+" )
        ryfile.write("# file containing resources database for this lesson \n")
        for resource in config["resources"] :
            processResource( config["title"], rind, resource, ryfile )
            if rind<3 :
               print("  resource" + str(rind) + ": " + resource["title"], file=eggdb)
               print("  rpath" + str(rind) + ": " + path + "data/resources/RESOURCE" + str(rind), file=eggdb)
            rind = rind + 1
        ryfile.close()
        print("  resource3: all resources for lesson", file=eggdb)
        print("  rpath3: " + path + "data/resources/RESOURCELIST", file=eggdb)
     

if __name__ == "__main__":
    nreplicas, replica, argv = 1, 0, sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hn:r:",["nreplicas=","replica="])
    except:
       print('compile.py -n <nreplicas> -r <replica number>')

    for opt, arg in opts:
       if opt in ['-h'] :
          print('compile.py -n <nreplicas> -r <replica number>')
          sys.exit()
       elif opt in ["-n", "--nreplicas"]:
          nreplicas = int(arg)
       elif opt in ["-r", "--replica"]:
          replica = int(arg)
    print("RUNNING", nreplicas, "REPLICAS. THIS IS REPLICA", replica )
    # write plumed version to file
    stable_version=subprocess.check_output('plumed info --version', shell=True).decode('utf-8').strip()
    f=open("_data/plumed.yml","w")
    f.write("stable: v%s" % str(stable_version))
    f.close()
    with open("_data/lessons" + str(replica) + ".yml","w") as eggdb:
        print("# file containing lesson database.",file=eggdb)

        # list of paths - not ordered
        pathlist=list(pathlib.Path('.').glob('lessons/*/*/lesson.yml'))
        # Reduce the number of lesson by reading in the eggs to use from a file -- used for testing
        if os.path.exists("selected_lessons.dat") :
           pathlist = []
           with open("selected_lessons.dat", "r") as file:
              for readline in file : pathlist.append( pathlib.Path( './' + readline.strip() ) )
        # cycle on ordered list
        k=0
        for path in sorted(pathlist, reverse=True, key=lambda m: str(m)):

            if k%nreplicas==replica : process_lesson(re.sub("lesson.yml$","",str(path)),eggdb)
            k = k + 1

