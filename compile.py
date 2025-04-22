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
from PlumedToHTML import processMarkdown, get_javascript, get_css
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

def processNavigation( lessonname, actions, embeds, plumeds_to_use,plumed_version_names):
    # Print the js for plumedToHTML to a file
    with open( "data/plumedtohtml.js", "w+") as jf : jf.write( get_javascript() )
    # Print the css for plumed to html to a file
    with open( "data/plumedtohtml.css", "w+") as cf : cf.write( get_css() )
    # First process the NAVIGATION file with processMarkdown to deal with 
    # any plumed inputs that have been included
    ninputs, nf = processMarkdown( "data/NAVIGATION.md", 
                                   plumeds_to_use,
                                   plumed_version_names, 
                                   actions )
    nfail = []
    for failNum in nf:
      nfail.append( failNum )

    with open( "data/NAVIGATION.md", "r" ) as f:
      inp = f.read()
    
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
                 if embeds[name]["type"]=="internal" : 
                    prevlesson = embeds[name]["location"]
                    if "." in prevlesson :
                        fdot = prevlesson.split(".")
                        if len(fdot)!=2 : raise Exception("previous lesson name " + prevlesson + " is invalid")
                        prevlesson = fdot[0] + "/" + fdot[1]
                    elif "/" not in prevlesson : raise Exception("previous lesson name " + prevlesson + " is invalid")
                    name = "../../../" + prevlesson + "/data/NAVIGATION.html" 
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
              nspl_name = name.split("/")
              if len(nspl_name)>1 : 
                 path = ""
                 for i in range(len(nspl_name)-1) : path += nspl_name[i] + "/"
                 # Print the js for plumedToHTML to a file
                 with open( "data/" + path + "/plumedtohtml.js", "w+") as jf : jf.write( get_javascript() )
                 # Print the css for plumed to html to a file
                 with open( "data/" + path + "/plumedtohtml.css", "w+") as cf : cf.write( get_css() )
              # And process the markdown 
              ni, nf = processMarkdown( "data/" + name,
                                        plumeds_to_use,
                                        plumed_version_names,
                                        actions )
              ninputs = ninputs + ni
              for i,failNum in enumerate(nf):
                  nfail[i]+=failNum
              
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
              pdfname = name.split("/")[-1]
              efile = open( "data/" + name.split(".")[0] + ".md", "w+" )
              efile.write( "# " + lessonname + " \n\n")
              efile.write( line.split('"')[3] + "\n\n" )
              efile.write("{% raw %}\n")
              efile.write('<p align="center"><iframe width="630" height="472" src="' + pdfname + '" allowfullscreen></iframe></p>\n')
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
    first, manlink = True, "https://www.plumed.org/doc-master/user-doc/html/actionlist/?actions="
    for a in actions :
        if first : 
           manlink += a 
           first = False
        else : 
           manlink += "," + a
    ofile.write("{% raw %}\n")
    ofile.write("<b><a href=\"" + manlink + "\" target=\"_blank\">Click here</a> to open manual pages for actions discussed in this tutorial.</b>\n")
    ofile.write("{% endraw %}\n")
    ofile.close()
    return ninputs, nfail

def process_lesson(path,action_counts,plumed_syntax,eggdb=None,plumeds_to_use=(PLUMED_STABLE,PLUMED_MASTER),plumed_version_names=("stable","master")):
    if not eggdb:
        eggdb=sys.stdout

    try:
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
          raise RuntimeError("Bad URL for path " + path )
        # try to open the zip file
        try:
          zf = zipfile.ZipFile("file.zip", "r")
        except zipfile.BadZipFile:
          raise RuntimeError("Bad zip file for path " + path )
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
        ninputs, nfail = processNavigation( config["title"], actions, embeds,
                                                   plumeds_to_use=plumeds_to_use,
                                                   plumed_version_names=plumed_version_names )

        dependlist = []
        for key, data in embeds.items() :
            if "type" in data and data["type"]=="internal" : dependlist.append( data["location"] )

        # Get the lesson id from the path
        lesson_id = path[8:10] + "." + path[11:14]
        # Get the reference
        ref,ref_url = get_reference(config["doi"])
        # Get the modules and the actions
        modules = set()  
        for a in actions :
            if a in plumed_syntax.keys() : 
               try :
                 modules.add( plumed_syntax[a]["module"] ) 
               except : 
                 raise Exception("could not find module for action " + a)
            if a in action_counts.keys() :
               action_counts[a] += 1
        astr = ' '.join(actions)
        modstr = ' '.join(modules)
        # to future me:
        # is a list of a single dict to get the '-' at the start of the dump
        # I am using dict.update() to keep the key ordering
        datadict = {"id":lesson_id,
         "title":config["title"],
         "shortitle":get_short_name_ini(config["title"],15),
         "path":path + "data/NAVIGATION.html",
         "instructors":config["instructors"],
         "doi":config["doi"],
         "reference":ref,
         "ref_url":ref_url,
         "description":config["description"],
        }
        if "tags" in config:
          datadict.update({"tags":config["tags"]})
        faildict = {"ninputs":ninputs,}
        if len(nfail)>=2 :
         #prints standard fo the site, this assumes that the tuple is stable, master:
            faildict.update({"nfail":nfail[0],
                   "nfailm":nfail[1]})
        fd={}
        for i,fail in enumerate(nfail) :
            fd[plumed_version_names[i]]=fail
        faildict.update({"inputfails":fd})
        datadict.update(faildict)
        if len(dependlist)>0 :
           datadict.update({"depends":dependlist})
        datadict.update({"actions":astr,
                         "modules":modstr,})        
        
        # end timing
        end_time = time.perf_counter()
        # store time
        datadict.update({"time":end_time-start_time})
        yaml.dump([datadict],
                  stream=eggdb,
                  #to not break lines
                  width=256,
                  sort_keys=False)

    except Exception as e:
      print("+++ EXCEPTION RAISED IN: ", path)
      print("+++ EXCEPTION stack:")
      import traceback
      print(traceback.format_exc())
      return (path, e)
    return None

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
    plumeds_to_use=(PLUMED_STABLE,PLUMED_MASTER)
    stable_version=subprocess.check_output(f'{plumeds_to_use[0]} info --version', shell=True).decode('utf-8').strip()
    
    plumed_version_names=("v"+ stable_version,"master")
    print(f"USING {plumeds_to_use=}")
    print(f"USING {plumed_version_names=}")
    f=open("_data/plumed.yml","w")
    f.write("stable: v%s" % str(stable_version))
    f.close()
    # Get list of plumed actions from syntax file
    cmd = [plumeds_to_use[1], 'info', '--root']
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
    listOfErrors = []
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
            error=process_lesson(re.sub("lesson.yml$","",str(path)),action_counts,plumed_syntax,eggdb,plumeds_to_use=plumeds_to_use,plumed_version_names=plumed_version_names)
            if error is not None :
               listOfErrors.append(error)
    if len(listOfErrors) > 0 :
        for path,e in listOfErrors :
           print("+++ EXCEPTION RAISED IN: ", path)
           print("+++ EXCEPTION text:" , e)

        raise Exception("Errors while compiling lessons")
    # output yaml file with action counts
    action_list = [] 
    for key, value in action_counts.items() : action_list.append( {'name': key, 'number': value } )
    cfilename = "_data/actioncount" + str(replica) + ".yml"
    with open(cfilename, 'w' ) as file :
        yaml.safe_dump(action_list, file)

