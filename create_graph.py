from zipfile import ZipFile
import tarfile
import pathlib
import networkx as nx
import textwrap
import json
import yaml
import os

if __name__ == "__main__":
   lessondict, pathlist= [], list(pathlib.Path('.').glob('lesson-content*/lessons.tar'))
   for path in pathlist : 
       print("PROCESSING DATA IN", str(path) )
       num = str(path).split("/")[0].replace("lesson-content","")
       tar = tarfile.open( str(path) )
       lf = tar.extractfile("_data/lessons" + num + ".yml")
       theselessons = yaml.load(lf,Loader=yaml.BaseLoader)
       lf.close()
       for l in theselessons : lessondict.append(l)
   
   print("FOUND LESSONS", lessondict )    

   plessondict = {}
   for data in lessondict :
       if "depends" in data :
          key = data["id"]
          if key not in plessondict : plessondict[key] = data
          for dd in data["depends"] : 
              idname = dd.replace("/",".")
              if idname not in plessondict :
                 for data2 in lessondict :
                     if idname==data2["id"] : 
                        plessondict[idname]=data2
                        break

   print("LESSONS IN GRAPH", plessondict )
   
   of = open("summarygraph.md", "w")
   of.write("""
   Browse the lessons
   ------------------------
   The graph below shows a subset of the lessons that have been submitted to the PLUMED-TUTORIALS website and suggests an order for working through them.
   PLUMED-TUTORIAL monitors whether PLUMED input files in these lessons are compatible with the current and development
   versions of the code and integrates links from these files to the PLUMED manual.  Inputs in the tutorials listed below were last tested on {{ site.data.date.date }}.
   
   You can return to a complete list of the tutorials by clicking [here](browse.md).
   """)
   of.write("flowchart TD\n")
   
   k, translate = 0, {} 
   for key, data in plessondict.items() : 
       title = ""
       for t in textwrap.wrap(data["title"],30) : title += t + "\n"
       of.write(  str(k) + "[" + title + "]\n")
       translate[key] = k
       translate[key.replace(".","/")] = k
       k = k + 1
   
   G = nx.DiGraph()
   for key, data in plessondict.items() : 
       if "depends" not in data : continue
       for dd in data["depends"] : G.add_edge( translate[dd], translate[key] )
   
   pG = nx.minimum_spanning_arborescence(G)
   for edge in pG.edges() :
       of.write( str(edge[0]) + "-->" + str(edge[1]) + "\n" )
   
   k=0
   for key, data in plessondict.items() : 
       of.write("click " + str(k) + " \"" + data["path"] + "\" \"**Authors: " + data["instructors"] + "** " + data["description"] + "\"\n" )
       k = k + 1
   
   
   of.close()
