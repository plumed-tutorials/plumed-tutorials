from zipfile import ZipFile
import tarfile
import pathlib
import networkx as nx
import numpy as np
import textwrap
import json
import yaml
import os

if __name__ == "__main__":
   lessondict, pathlist= [], list(pathlib.Path('.').glob('lesson-content*/lessons.tar'))
   for path in pathlist : 
       num = str(path).split("/")[0].replace("lesson-content","")
       tar = tarfile.open( str(path) )
       try:
         lf = tar.extractfile("_data/lessons" + num + ".yml")
         theselessons = yaml.load(lf,Loader=yaml.BaseLoader)
       except Exception as e:
         print("FILE ","_data/lessons" + num + ".yml")
         print("ERROR ",e)
         raise e
       lf.close()
       for l in theselessons : lessondict.append(l)

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
   
   of = open("summarygraph.md", "w")
   ghead = """
Browse the lessons
------------------------

The graph below shows a subset of the lessons that have been submitted to the PLUMED-TUTORIALS website and suggests an order for working through them. PLUMED-TUTORIAL monitors whether PLUMED input files in these lessons are compatible with the current and development versions of the code and integrates links from these files to the PLUMED manual.  Inputs in the tutorials listed below were last tested on {{ site.data.date.date }}.
   
You can return to a complete list of the tutorials by clicking [here](browse.md).

```mermaid
   """
   of.write(ghead + "\n")
   of.write("flowchart TD\n")
   
   k, translate, backtranslate = 0, {}, [] 
   for key, data in plessondict.items() : 
       title, wrappedtext = "", textwrap.wrap(data["title"],30)
       for i in range(len(wrappedtext)-1) : title += wrappedtext[i] + "\n"
       title += wrappedtext[-1]
       of.write(  str(k) + "(\"" + title + "\")\n")
       translate[key] = k
       translate[key.replace(".","/")] = k
       backtranslate.append(title)
       k = k + 1
   
   G = nx.DiGraph()
   for key, data in plessondict.items() : 
       if "depends" not in data : continue
       for dd in data["depends"] : 
           if dd not in translate.keys() : raise Exception("could not find key " + dd + " in list of lessons")
           if key not in translate.keys() : raise Exception("could not find key " + key + " in list of lessons")
           G.add_edge( translate[dd], translate[key] )
   
   # Find any closed loops in the graph and remove them
   cycles = list( nx.simple_cycles(G) )
   for cyc in cycles :
      for i in range(len(cyc)-1) : G.remove_edge( cyc[i], cyc[(i+1)%len(cyc)] )

   pG = nx.transitive_reduction(G)

   # Create a matrix with the connections
   graphmat = np.zeros([k,k])
   for edge in pG.edges() : graphmat[edge[0],edge[1]] = 1
   for cyc in cycles :
       for i in range(len(cyc)-1) : graphmat[cyc[i], cyc[(i+1)%len(cyc)]] = 1

   drawn = np.zeros(k)
   for i in range(k) :
       group = set([i])
       for j in range(k) :
           if np.sum(graphmat[:,i])>0 and np.all(graphmat[:,j]==graphmat[:,i]) and drawn[j]==0 : group.add(j)

       # This code ensures that if there are more than 2 nodes that have identical dependencies we draw them in 
       # a subgraph.  The resulting flow chart is less clustered with arrows       
       if len(group)>2 :
          of.write("subgraph g" + str(i) + " [ ]\n")
          ncols, lgroup, row, col = 5, [], 0, 0
          for j in group :
              lgroup.append(j)
              if drawn[j]==0 :
                 of.write(  str(j) + "(\"" + backtranslate[j] + "\")\n")
                 if row>0 :
                    ind = lgroup[(row-1)*ncols + col]
                    # Commenting out this line as graphs command doesn't work on github pages
                    #of.write( str(ind) + "~~~" + str(j) + ";\n")
                 col = col + 1
                 if col%ncols==0 : col, row = 0, row + 1


                 drawn[j]=1
          of.write("end\n")
          for l in range(k) :
              if graphmat[l,j]>0 :
                 if drawn[l]==0 :
                    of.write(  str(l) + "(\"" + backtranslate[l] + "\")\n")
                    drawn[l]=1
                 of.write( str(l) + "--> g" + str(i) + ";\n" )
          for j in group : graphmat[:,j] = 0

   for i in range(k) :
       if drawn[i]==0 : of.write( str(i) + "(\"" + backtranslate[i] + "\")\n" )
       for j in range(k) :
           if graphmat[i,j]>0 : of.write( str(i) + "-->" + str(j) + ";\n" )

   # for edge in pG.edges() :
   #     of.write( str(edge[0]) + "-->" + str(edge[1]) + ";\n" )
   # 
   # # Add in the cycles
   # for cyc in cycles :
   #     for i in range(len(cyc)-1) : of.write( str(cyc[i]) + "-->" + str(cyc[(i+1)%len(cyc)]) + ";\n" ) 

   k=0
   for key, data in plessondict.items() : 
       of.write("click " + str(k) + " \"" + data["path"] + "\" \""  + data["description"] + " [Authors: " + data["instructors"] + "]\"\n" )
       k = k + 1
   
   of.write("```\n")
   of.close()
