import yaml
import sys
import getopt
import shutil
import re
import urllib.request
import zipfile
import os
import json
import pathlib
import subprocess
import nbformat
from nbconvert import HTMLExporter 
from contextlib import contextmanager
from PlumedToHTML import test_plumed, get_html, get_mermaid
import time

if not (sys.version_info > (3, 0)):
   raise RuntimeError("We are using too many python 3 constructs, so this is only working with python 3")

PLUMED_STABLE="plumed"
PLUMED_MASTER="plumed_master"

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def get_reference(doi):
    # initialize strings
    ref=""; ref_url=""
    # retrieve citation from doi
    if(len(doi)>0):
      # check if unpublished/submitted
      if(doi.lower()=="unpublished" or doi.lower()=="submitted"):
        ref=doi.lower()
      # get info from doi
      else:
        try:
          # get citation
          cit = subprocess.check_output('curl -LH "Accept: text/bibliography; style=science" \'http://dx.doi.org/'+doi+'\'', shell=True).decode('utf-8').strip()
          if("DOI Not Found" in cit):
           ref="DOI not found"
          else:
           # get citation
           ref=cit[3:cit.find(", doi")]
           # and url
           ref_url="http://dx.doi.org/"+doi
        except:
          ref="DOI not found"
    return ref,ref_url

def get_short_name_ini(lname, length):
    if(len(lname)>length): sname = lname[0:length]+"..."
    else: sname = lname
    return sname

def processNavigation( lessonname, actions, embeds ) :
    with open( "data/NAVIGATION.md", "r" ) as f:
      inp = f.read()
    
    ninputs=0
    nfail=0
    nfailm=0
    ofile = open( "data/NAVIGATION.md", "w+")
    inmermaid = False
    for line in inp.splitlines() : 
        if "```mermaid" in line : 
           inmermaid = True
           ofile.write( line + "\n")
        elif inmermaid and "```" in line :
           inmermaid = False 
           ofile.write( line + "\n" )
        elif inmermaid and "click" in line :
           name = line.split('"')[1]
           name_extension = name.split(".")[1] if len(name.split("."))>1 else ""
           islesson = False 
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
                 islesson = True
                 if embeds[name]["type"]=="internal" : name = "../../../" + embeds[name]["location"] + "/data/NAVIGATION.html" 
                 else : name = embeds[name]["location"]
           elif "md" in name_extension: 
              # Special treatment for README.md files as GitHub links to data/README.html don't work as pages opens the rendered README.md file when you open data/
              if "README.md" in name :
                 old_name=name
                 spl_name= name.split("/")
                 new_name = ""
                 for i in range(len(spl_name)-1) :
                    new_name += spl_name[i] + "/"
                 name = new_name + "GAT_SAFE_README.md"
                 shutil.copyfile("data/" + old_name, "data/" + name)
              ni, nf, nfm = processMarkdown( name, actions )
              ninputs = ninputs + ni
              nfail = nfail + nf
              nfailm = nfailm + nfm
           elif "ipynb" in name_extension:
              with open("data/" + name) as f : 
                  mynotebook = nbformat.read( f, as_version=4 )
              # Instantiate the exporter
              exporter = HTMLExporter(template_name = 'classic')
              body, _ = exporter.from_notebook_node( mynotebook )
              ipfile = open("data/" + name.split(".")[0] + ".html", "w+" )
              ipfile.write( body ) 
              ipfile.close() 
           elif "pdf" in name_extension:
              efile = open( "data/" + name.split(".")[0] + ".md", "w+" )
              efile.write( "# " + lessonname + " \n\n")
              efile.write( line.split('"')[3] + "\n\n" )
              efile.write("{% raw %}\n")
              efile.write('<p align="center"><iframe width="630" height="472" src="' + name + '" allowfullscreen></iframe></p>\n')
              efile.write("{% endraw %}\n")
              efile.close()
           else :
              print("failing for file named " + name )
              raise RuntimeError(f"cannot process filname called {name} use md, pdf or ipynb extension")   
           # And write out the updated click line with the proper link 
           if islesson :
              ofile.write( line.split('"')[0] + '"' + name + '" "' + line.split('"')[3] + '"\n' )
           else :
              ofile.write( line.split('"')[0] + '"' + name.split(".")[0] + '.html" "' + line.split('"')[3] + '"\n' ) 
        else :
           ofile.write( line + "\n" )
    ofile.close()
    return ninputs, nfail, nfailm 

def processMarkdown( filename, actions ) :
    if not os.path.exists("data/" + filename) : 
       raise RuntimeError("Found no file called " + filename + " in lesson")

    with open( "data/" + filename, "r" ) as f:
       inp = f.read()
    
    ninputs = 0
    nfail = 0
    nfailm = 0
    inplumed = False
    plumed_inp = ""
    solutionfile = None
    incomplete = False
    usemermaid = ""
    with open( "data/" + filename, "w+" ) as ofile:
      for line in inp.splitlines() :
         # Detect and copy plumed input files 
         if "```plumed" in line :
            inplumed = True
            plumed_inp = ""
            solutionfile = None
            incomplete = False
            ninputs = ninputs + 1 
   
         # Test plumed input files that have been found in tutorial 
         elif inplumed and "```" in line : 
            inplumed = False
            # Create mermaid graphs from PLUMED inputs if this has been requested
            if usemermaid!="" :
               mermaidinpt = ""
               if usemermaid=="value" :
                  mermaidinpt = get_mermaid( PLUMED_MASTER, plumed_inp, False )
               elif usemermaid=="force" :
                  mermaidinpt = get_mermaid( PLUMED_MASTER, plumed_inp, True )
               else :
                  raise RuntimeError(usemermaid + "is invalid instruction for use mermaid") 
               ofile.write("```mermaid\n" + mermaidinpt + "\n```\n")
            if incomplete :
                  if solutionfile:
                     # Read solution from solution file
                     try:
                        with open( "data/" + solutionfile, "r" ) as sf:
                           solution = sf.read() 
                           plumed_inp += "#SOLUTION \n" + solution
                     except:
                        raise RuntimeError(f"error in opening {solutionfile} as solution"
                                          f" for an incomplete input from file {filename}")
                  else:
                     raise RuntimeError(f"an incomplete input from file {filename}"
                                       " does not have its solution file")      
            # Create the full input for PlumedToHTML formatter 
            else :
                  solutionfile = filename + "_working_" + str(ninputs) + ".dat"
                  with open( "data/" + solutionfile, "w+" ) as sf:
                     sf.write( plumed_inp )

            # Test whether the input solution can be parsed
            success = success=test_plumed( PLUMED_STABLE, "data/" + solutionfile )
            if(success!=0 and success!="custom") : nfail = nfail + 1
            # Json files are put in directory one up from us to ensure that
            # PlumedToHTML finds them when we do get_html (i.e. these will be in
            # the data directory where the calculation is run)
            if incomplete :
               success_master=test_plumed(PLUMED_MASTER, "data/" + solutionfile ) 
            else :
               success_master=test_plumed(PLUMED_MASTER, "data/" + solutionfile,
                                          printjson=True, jsondir="../" )
            if( success_master!=0 and success_master!="custom") :
               nfailm = nfailm + 1
            # Find the stable version 
            stable_version=subprocess.check_output(f'{PLUMED_STABLE} info --version',
                                                   shell=True).decode('utf-8').strip()
            # Use PlumedToHTML to create the input with all the bells and whistles
            html = get_html(plumed_inp,
                              solutionfile,
                              solutionfile,
                              ("v"+ stable_version,"master"),
                              (success,success_master),
                              (PLUMED_STABLE,PLUMED_MASTER),
                              usejson=(not success_master),
                              actions=actions )
            # Print the html for the solution
            ofile.write( "{% raw %}\n" + html + "\n {% endraw %} \n" )
         # This finds us the solution file
         elif inplumed and "#SOLUTIONFILE=" in line :
            solutionfile=line.replace("#SOLUTIONFILE=","")
         elif inplumed and "#MERMAID=" in line : 
            usemermaid = line.replace("#MERMAID=","").strip()
         elif inplumed :
            if "__FILL__" in line :
               incomplete = True 
            plumed_inp += line + "\n"
         # Just copy any line that isn't part of a plumed input
         elif not inplumed :
            ofile.write( line + "\n" )

    return ninputs, nfail, nfailm

def process_lesson(path,action_counts,plumed_syntax,eggdb=None):
    if not eggdb:
        eggdb=sys.stdout

    with cd(path):
        # start timing
        start_time = time.perf_counter()
        # open file
        stram = open("lesson.yml", "r")
        config=yaml.load(stram,Loader=yaml.BaseLoader)
        stram.close()
        # check fields
        for field in ("url","instructors","title","doi"):
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
        # Check if there is a command to run in the config and run it if there is
        if "command" in config : 
           with cd("data") : 
             print("RUNNING COMMAND: " + config["command"] + " in " + os.getcwd() )
             result = subprocess.run(["python", config["command"]], capture_output=True)
             print( result )
             #subprocess.run(config["command"])

        # Check for the existence of a NAVIGATION file
        if os.path.exists("data/navigation.md") : os.rename("data/navigation.md","data/NAVIGATION.md")
        if not os.path.exists("data/NAVIGATION.md") : raise RuntimeError("No NAVIGATION.md file found in lesson")
        # Get the contents of the embeds file
        embeds = {}
        if os.path.exists("data/embed.yml") :
           stram=open("data/embed.yml", "r")
           embeds=yaml.load(stram,Loader=yaml.BaseLoader) or {}
           stram.close() 
        elif os.path.exists("data/EMBED.yml") :
           stram=open("data/EMBED.yml", "r")
           embeds=yaml.load(stram,Loader=yaml.BaseLoader) or {}
           stram.close()

        # Process the navigation file
        actions = set({})  # This holds the list of actions used in all the plumed input files in the markdown
        ninputs, nfail, nfailm = processNavigation( config["title"], actions, embeds )

        dependlist = []
        for key, data in embeds.items() :
            if "type" in data and data["type"]=="internal" : dependlist.append( data["location"] )

        # Get the lesson id from the path
        lesson_id = path[8:10] + "." + path[11:14]
        print("- id: '" + lesson_id + "'",file=eggdb)
        print("  title: " + config["title"],file=eggdb)
        print("  shortitle: '" + get_short_name_ini(config["title"],15) +"'",file=eggdb)
        print("  path: " + path + "data/NAVIGATION.html", file=eggdb)
        print("  instructors: " + config["instructors"], file=eggdb)
        # get citation
        ref,ref_url = get_reference(config["doi"])
        print("  doi: " + config["doi"],file=eggdb)
        print("  reference: '" + ref +"'",file=eggdb)
        print("  ref_url: '" + ref_url +"'",file=eggdb)
        print("  description: " + config["description"], file=eggdb)
        if "tags" in config.keys() : print("  tags: " + config["tags"], file=eggdb)
        print("  ninputs: " + str(ninputs), file=eggdb)
        print("  nfail: " + str(nfail), file=eggdb)
        print("  nfailm: " + str(nfailm), file=eggdb)
        if len(dependlist)>0 : 
           print("  depends: ", file=eggdb)
           for d in dependlist : print("    - " + str(d), file=eggdb ) 
        modules = set()  
        for a in actions :
            if a in plumed_syntax.keys() : 
               try :
                 modules.add( plumed_syntax[a]["module"] ) 
               except : 
                 raise Exception("could not find module for action " + a)
            if a in action_counts.keys() : action_counts[a] += 1
        astr = ' '.join(actions)
        print("  actions: " + astr, file=eggdb)
        modstr = ' '.join(modules)
        print("  modules: " + modstr, file=eggdb)
        # end timing
        end_time = time.perf_counter()
        # store time
        print("  time: " + str(end_time-start_time), file=eggdb)

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
    stable_version=subprocess.check_output(f'{PLUMED_STABLE} info --version', shell=True).decode('utf-8').strip()
    f=open("_data/plumed.yml","w")
    f.write("stable: v%s" % str(stable_version))
    f.close()
    # Get list of plumed actions from syntax file
    cmd = [PLUMED_MASTER, 'info', '--root']
    plumed_info = subprocess.run(cmd, capture_output=True, text=True )
    keyfile = plumed_info.stdout.strip() + "/json/syntax.json" 
    with open(keyfile) as f :
        try:
           plumed_syntax = json.load(f)
        except ValueError as ve:
           raise InvalidJSONError(ve)
    # Make a dictionary to hold all the actions
    action_counts = {}
    for key in plumed_syntax :
        if key=="vimlink" or key=="replicalink" or key=="groups" : continue
        action_counts[key] = 0
    # loop over lesson for this replica
    with open("_data/lessons" + str(replica) + ".yml","w") as eggdb:
        print("# file containing lesson database.",file=eggdb)

        # list of paths for this replica - not ordered
        pathlist = [line.strip() for line in open("pathlist"+str(replica), 'r')]

        # Reduce the number of lesson by reading in the eggs to use from a file -- used for testing
        if os.path.exists("selected_lessons.dat") :
           pathlist = []
           with open("selected_lessons.dat", "r") as file:
              for readline in file : pathlist.append( pathlib.Path( './' + readline.strip() ) )
        # cycle on ordered list
        for path in sorted(pathlist, reverse=True, key=lambda m: str(m)):
            # process lesson
            process_lesson(re.sub("lesson.yml$","",str(path)),action_counts,plumed_syntax,eggdb)
    # output yaml file with action counts
    action_list = [] 
    for key, value in action_counts.items() : action_list.append( {'name': key, 'number': value } )
    cfilename = "_data/actioncount" + str(replica) + ".yml"
    with open(cfilename, 'w' ) as file :
        yaml.safe_dump(action_list, file)

