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

def processNavigation( lessonname ) :
    f = open( "data/NAVIGATION.md", "r" )
    inp = f.read()
    f.close()

    if not os.path.exists("data/EMBED.yml") : 
       raise RuntimeError("No EMBED.yml file found in lesson")
    stram=open("data/EMBED.yml", "r")
    embeds=yaml.load(stram,Loader=yaml.BaseLoader)
    stram.close()

    ofile, inmermaid = open( "data/NAVIGATION.md", "w+"), False
    for line in inp.splitlines() : 
        if "```mermaid" in line : 
           inmermaid = True
           ofile.write( line + "\n")
        elif inmermaid and "```" in line :
           inmermaid = False 
           ofile.write( line + "\n" )
        elif inmermaid and "click" in line :
           name, islesson = line.split('"')[1], False 
           if name in embeds :
              if "title" in embeds[name] :
                 efile = open( "data/" + name + ".md", "w+" ) 
                 efile.write( "# " + lessonname + ": " + embeds[name]["title"] + "\n\n")
                 efile.write( line.split('"')[3] + "\n\n" )
                 efile.write("{% raw %}\n")
                 efile.write('<p align="center"><iframe width="630" height="472" src="' + embeds[name]["location"] + '" frameborder="0" allowfullscreen></iframe></p>\n')
                 efile.write("{% endraw %}\n")
                 efile.close()
              else : 
                 name, islesson = "../../" + embeds[name]["location"] + "/data/NAVIGATION.html", True
           elif "md" in name.split(".")[1] : 
              processMarkdown(name)
           elif "ipynb" in name.split(".")[1] :
              with open("data/" + name) as f : 
                  mynotebook = nbformat.read( f, as_version=4 )
              # Instantiate the exporter
              exporter = HTMLExporter(template_name = 'classic')
              (body, resources) = exporter.from_notebook_node( mynotebook )
              ipfile = open("data/" + name.split(".")[0] + ".html", "w+" )
              ipfile.write( body ) 
              ipfile.close() 
           else :
              raise RuntimeError("cannot process filname called " + name + " use md or ipynb extension")   
           # And write out the updated click line with the proper link 
           if islesson : ofile.write( line.split('"')[0] + '"' + name + '.html" "' + line.split('"')[3] + '"\n' )
           else : ofile.write( line.split('"')[0] + '"' + name.split(".")[0] + '.html" "' + line.split('"')[3] + '"\n' ) 
        else :
           ofile.write( line + "\n" )
    ofile.close()

def processMarkdown( filename ) :
    if not os.path.exists("data/" + filename) : 
       raise RuntimeError("Found no file called " + filename + " in lesson")
    f = open( "data/" + filename, "r" )
    inp = f.read()
    f.close()
 
    ofile, inplumed, plumed_inp, solutionfile, incomplete = open( "data/" + filename, "w+" ), False, "", "", False
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
        stram.close()
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

        # Check for the existence of a NAVIGATION file
        if not os.path.exists("data/NAVIGATION.md") : 
           raise RuntimeError("No NAVIGATION.md file found in lesson")
        # Process the navigation file
        processNavigation( config["title"] )

        # Get the lesson id from the path
        lesson_id = path[8:10] + "." + path[11:14]
        print("- id: '" + lesson_id + "'",file=eggdb)
        print("  title: " + config["title"],file=eggdb)
        print("  path: " + path + "data/NAVIGATION.html", file=eggdb)
        print("  instructors: " + config["instructors"], file=eggdb)
        print("  description: " + config["description"], file=eggdb)

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

