How to contribute a new lesson to the PLUMED-TUTORIALS
---------------------------------------------------
Adding a lesson to the PLUMED-TUTORIALS is free and easy. To do so you must:

* Collect the input files that the students will need to run the calculations that they will perform as they complete the exercise.  
* Write instructions in [markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) that explain the tasks that the students should work through during the lesson and how they should use the input files you provide.  More detailed information on how to do this is provided below.  Notice that you can divide your instructions inbetween as many markdown files as you feel is appropriate.
* Identify embedable objects (e.g. YouTube videos) and jupyter notebook files that you think it would be useful to share with students in order to help them complete your lesson.  
* Write a file called EMBED.yml that contains information about the location of the videos that you would like students to have access to.  See instructions below.
* Write a file called NAVIGATION.md that contains a flowchart that shows students the order they should work through your exercises.  See instructions below.
* Create and upload a zip file containing the input files, the jupyter notebooks, your markdown files, the EMBED.yml file and the NAVIGATION.md to your favorite repository. Popular solutions are [Zenodo](https://zenodo.org) and [GitHub](http://github.com) (we would recommend creating a git repository and using the second of these tools). Additional info about where to host your zip file can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).

To incorporate your lesson into the PLUMED-TUTORIALS website you then need to write a yaml file like the one below:

```yml
url: the location to download your zip archive from goes here
instructors: your name/s
title: the title of your lesson
description: a short description of the content covered in your lesson
command: the name of a python script that must be executed to build your tutorial
```

Once you have prepared this file email it to the <b><a href="mailto:plumed.nest@gmail.com">plumed.nest@gmail.com</a></b> and one of the PLUMED consortium coordinators will 
ensure that your content is loaded into the site.  The instruction page for your lesson is created from the README.md file you provide.  The list of additional 
resources, video pages and notebook pages are generated automatically from the information you provide in the yaml file  

Once your content is loaded on the PLUMED-TUTORIALS site, the lesson will upload if you edit the files in the zip archive whose link you shared with us.
If for some reason you need to change the location of zip file you will will need to contact the PLUMED developers in order to update your yaml file.

N.B. In the vast majority of cases you do not need to include the `command` key pair in the yaml file.  This option is used in cases where there is content in a lesson that 
changes as PLUMED develops.  You might use this option if you want to include a list of collective variables in your tutorial as folks are always implementing new CVs. If you 
would like to use this option then you can look at the scripts in <a href="https://github.com/plumed/installation-instructions">this tutorial</a> and 
its <a href="https://github.com/plumed-school/plumed-school/blob/main/lessons/20/001/lesson.yml">yaml file</a>.

Lastly, note that if you want to a a link to content that you have contributed to PLUMED-TUTORIALS to your personal website you can use a url like the one below:

````
https://www.plumed-tutorials.org/browse.html?search=yourname
````

__Please note that:__

* <b> All contributions are curated and manually uploaded by the coordinators of the PLUMED consortium. Therefore, a delay between submission and online publication should be expected.</b>
* PLUMED-TUTORIALS will not host your archive, so make sure the indicated URL remains accessible. More info about where to host your contribution can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).
* PLUMED-TUTORIALS does not test whether the exercises in your lesson are executed correctly.  It only tests whether the PLUMED can parse the input files you provided in the README instructions.

<center>
<p><b>Questions related to the submission to PLUMED-TUTORIALS can be directed to:</b></p>
<p><b><a href="mailto:plumed.nest@gmail.com">plumed.nest@gmail.com</a></b></p>
</center>

# Writing the NAVIGATION.md file

The NAVIGATION.md file is the first file that the user will see when they open your lesson.  This file should provide a flow chart that indicates the order in which the resources you have 
provided in your lesson should be accessed.  You can write these files using [mermaid flowcharts](https://mermaid-js.github.io/mermaid/#/flowchart) which can be emdedded directly into 
[github markdown files](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).  The following snippet 
shows an example flow chart for a lesson that contains a single video, a markdown file and a python notebook.  In this exercise you are also strongly encouraging them to complete masterclass
21/001 before starting your masterclass.

````
```mermaid
flowchart LR
A[PLUMED intro] ==> B[Lecture I]
B ==> C[Instructions]
C ==> D[solution]
click A "ref1" "You should complete this earlier masterclass before completing this exercise"
click B "video1" "A video that introduces the exercise"
click C "README.md" "The instructions for the exercise"
click D "notebooks/solultion.ipynb" "A python notebook containing a full set of solutions for the exercise"
```
```` 

When the PLUMED-TUTORIALS website is built the nodes in the flowchart thus serve as links to the various pages that are built from the resources you provide.  The NAVIGATION.md file is parsed and
the name of the file or object to embed that is provided in the first set of inverted commas after each click command is replaced by a suitable hyperlink.  (the text in the second set of inverted commas 
on these lines will appear in a tooltip)

# Writing the EMBED.yml file

If there are HTML objects (e.g. YouTube videos, GeoGebra apps) that you would like to embed into your lesson pages, if you would like students to complete some earlier masterclass before trying yours or if you 
want users to connsult an external link you should list them in a yml file called EMBED.yml that will look as follows:

```yml
video1: 
  title: <insert title to use on page that embeds your resource here> 
  location: <insert embed link here>
ref1: 
  location: <insert unique ID of earlier masterclass here e.g. 21/001>
  type: internal
ref2:
  location: <insert link to exeternal website>
  type: external
``` 

Notice that keys in this file are used when constructing the flowchart in the NAVIGATION.md file in place of the location of the file that should be included.

# Writing your markdown files

As explained in the instructions above, the instructions for your lessons must be written in files called `<name>.md` that are
written in [markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax). The 
website we have linked above gives a good introduction to markdown.  It is worth noting, however, that Markdown also allows you to:

* [Display mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)
* [Include blocks of code](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks) with syntax highlighting

There are, in fact, many [advanced features](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting) in the markdown syntax that you can use.
Furthermore, working markdown is particularly straightforward if you edit your markdown files directly on [GitHub](http://github.com).

We have also extended the markdown syntax so that you can include PLUMED input files in your tutorials using the following syntax:

````
```plumed
d1: DISTANCE ATOMS=1,2
PRINT ARG=d1 FILE=colvar
```
````

When blocks that contain PLUMED input like the one above are encountered in a `README.md` file the scripts that build the website will test that PLUMED can parse the input.  When
these inputs are displayed various badges are displayed to indicate that PLUMED can/cannot parse the input.  Furthermore, a suitably highlighted version of the input that contains 
links and tooltips with information from the PLUMED manual is included in the final website.

We have found it useful to include incomplete inputs in tutorials.  You can include incomplete inputs as shown below:

````
```plumed
#SOLUTIONFILE=work/plumed_input.dat
d1: DISTANCE __FILL__
PRINT ARG=__FILL__ FILE-colvar
```
````

To prevent broken badges from appearing by these incomplete inputs you must include a complete version of the input in your repository. Within the `README.md` file you provide the location of the complete
input in your zip archive by using the `#SOLUTIONFILE` instruction as shown above.  This `#SOLUTIONFILE` comment will NOT appear in the version of the input file that is rendered on 
the PLUMED-TUTORIALS website.

# On cheating 

It is tempting to argue that providing incomplete inputs in the README.md file is pointless if the solutions are available in the repository. When things are organised this way students will 
"cheat" and go directly to the solutions without engaging with the exercise.  This argument is not particularly charitable to students. First of all, it is worth noting that students get no direct reward from 
completing the exercises on this website. It is thus unlikely that the sorts of students who "cheat" are bothering with these lessons.

If you are still woried that this defeats the object though, think about it from the student's point of view. When a student takes on one of these lessons they have to make sense of a lot of things; namely,
your README.md file, the list of resources you provide, everything else in your repository and the whole PLUMED manual. If, in wading through this mountain of data, students find the solutions
and work out that they are the solutions they are doing pretty well!
