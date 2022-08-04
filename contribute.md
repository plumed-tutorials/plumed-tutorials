How to contribute a new lesson to the PLUMED-SCHOOL
---------------------------------------------------
Adding a lesson to the PLUMED-SCHOOL is free and easy. To do so you must:

* Collect the input files that the students will need to run the calculations that they will perform as they complete the exercise.  
* Write a README file in [markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) that explains the tasks that the students should work through during the lesson and how they should use the input files you provide.  More detailed information on how to do this is provided below.
* Identify videos and jupyter notebook files that you think it would be useful to share with students in order to help them complete your lesson. 
* Create and upload a zip file containing the input files, the jupyter notebooks and your markdown README file to your favorite repository. Popular solutions are [Zenodo](https://zenodo.org) and [GitHub](http://github.com) (we would recommend creating a git repository and using the second of these tools). Additional info about where to host your zip file can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).

To incorporate your lesson into the PLUMED-SCHOOL website you then need to write a yaml file like the one below:

```yml
url: the location to download your zip archive from goes here
instructors: your name/s
title: the title of your lesson
resources:
  - title: the title for your first video
    description: a description of what is contained in your video
    type: video
    location: the embed link for the video you would like to share
  - title: the title for your notebook
    description: a description of the notebook that you are sharing
    type: notebook
    location: the location of the notebook in the zip file you uploaded
```

Once you have prepared this file email it to the <b><a href="mailto:plumed.nest@gmail.com">plumed.nest@gmail.com</a></b> and one of the PLUMED consortium coordinators will 
ensure that your content is loaded into the site.  The instruction page for your lesson is created from the README.md file you provide.  The list of additional 
resources, video pages and notebook pages are generated automatically from the information you provide in the yaml file  

Once your content is loaded on the PLUMED-SCHOOL site, the lesson will upload if you edit the README.md file or the jupyter notebooks that are in zip archive whose link you shared with us.
If you wish to list additional jupyter notebooks or videos on your pages you will need to contact the PLUMED developers in order to update your yaml file.

__Please note that:__

* <b> All contributions are curated and manually uploaded by the coordinators of the PLUMED consortium. Therefore, a delay between submission and online publication should be expected.</b>
* PLUMED-SCHOOL will not host your archive, so make sure the indicated URL remains accessible. More info about where to host your contribution can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).
* PLUMED-SCHOOL does not test whether the exercises in your lesson are executed correctly.  It only tests whether the PLUMED can parse the input files you provided in the README instructions.

<center>
<p><b>Questions related to the submission to PLUMED-SCHOOL can be directed to:</b></p>
<p><b><a href="mailto:plumed.nest@gmail.com">plumed.nest@gmail.com</a></b></p>
</center>

# Writing your README.md file

As explained in the instructions above, the instructions for your lessons must be written in file called `README.md` that is 
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
the plumed-school website.

# On cheating 

It is tempting to argue that providing incomplete inputs in the README.md file is pointless if the solutions are available in the repository. When things are organised this way students will 
"cheat" and go directly to the solutions without engaging with the exercise.  This argument is not particularly charitable to students. First of all, it is worth noting that students get no direct reward from 
completing the exercises on this website. It is thus unlikely that the sorts of students who "cheat" are bothering with these lessons.

If you are still woried that this defeats the object though, think about it from the student's point of view. When a student takes on one of these lessons they have to make sense of a lot of things; namely,
your README.md file, the list of resources you provide, everything else in your repository and the whole PLUMED manual. If, in wading through this mountain of data, students find the solutions
and work out that they are the solutions they are doing pretty well!
