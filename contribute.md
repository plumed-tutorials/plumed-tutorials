How to contribute a new lesson to PLUMED-TUTORIALS
---------------------------------------------------
Adding a lesson to PLUMED-TUTORIALS is free and easy. To do so you must:

* Collect the input files that the students will need to run the calculations that they will perform as they complete the exercise.  
* Write instructions in [markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) that explain the tasks that the students should work through during the lesson and how they should use the input files you provide.  More detailed information on how to do this is provided [here](instructions.md).  Notice that you can divide your instructions inbetween as many markdown files as you feel is appropriate.
* Identify embedable objects (e.g. YouTube videos) and jupyter notebook files that you think it would be useful to share with students in order to help them complete your lesson.  
* Write a file called EMBED.yml that contains information about the location of the videos that you would like students to have access to.  See instructions [here](instructions.md).
* Write a file called NAVIGATION.md that contains a flowchart that shows students the order they should work through your exercises.  See instructions [here](instructions.md).
* Create and upload a zip file containing the input files, the jupyter notebooks, your markdown files, the EMBED.yml file and the NAVIGATION.md to your favorite repository. Popular solutions are [Zenodo](https://zenodo.org) and [GitHub](http://github.com) (we would recommend creating a git repository and using the second of these tools). Additional info about where to host your zip file can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).
* Please keep you zip file around 100 MB.
* Fill in the sections of the form below. All fields are required, unless otherwise specified.

The fields you must fill are:

* __ID:__ please select *"new"* for a new submission, or your ID in case of resubmission/update of an existing lesson
* __Title:__ the title of your lesson 
* __URL:__ the location of the zipped archive containing your lesson
* __Keywords:__ keywords describing the lesson
* __Instructors:__ your name/s
* __Contact:__ the name of a contact person to communicate with the coordinators of the PLUMED consortium
* __Contact email:__ the email of the contact person
* __Comments (optional):__ comments related to the submission or feedback on existing tutorials

__Please note that:__

* <b> All contributions are curated and manually uploaded by the coordinators of the PLUMED consortium. Therefore, a delay between submission and online publication should be expected.</b>
* The name and email of the contact person will not appear on the PLUMED-TUTORIALS website.
* If necessary, you will be able to edit the information on [GitHub](https://github.com/plumed-school/plumed-school) later or send us a revised version of the form. In the latter case, please specify a list of changes in the "Comments" field.
* PLUMED-TUTORIALS will not host your archive, so make sure the indicated URL remains accessible. More info about where to host your contribution can be found [here](https://github.com/plumed-nest/plumed-nest/blob/master/README.md#zip-info).
* PLUMED-TUTORIALS does not test whether the exercises in your lesson are executed correctly.  It only tests whether the PLUMED can parse the input files you provided in the README instructions.

Lastly, note that if you want to a a link to content that you have contributed to PLUMED-TUTORIALS to your personal website you can use a url like the one below:

````
https://www.plumed-tutorials.org/browse.html?search=yourname
````

<center>
<p><b>Questions related to the submission to PLUMED-TUTORIALS can be directed to:</b></p>
<p><b><a href="mailto:plumed.tutorials@gmail.com">plumed.tutorials@gmail.com</a></b></p>
</center>

Fields marked with "<sup>*</sup>" are optional

{% assign sorted_less = site.data.lessons | sort: "id" | reverse %}
<form class="wj-contact" method="POST" action="https://formspree.io/f/xyzgopbq">
  <table>
    <tr>
      <td><label for="id">ID</label></td>
      <td width="600"><select id="id" type="texy" name="ID"><option>new (ID to be assigned)</option>{% for item in sorted_less %}<option>{{ item.id }}:{{ item.shortitle }}</option>{% endfor %} required</select> </td>
    </tr>
    <tr>  
      <td><label for="title">Title</label></td>
      <td width="600"><input id="title" type="text" name="title" required> </td>
    </tr>
    <tr>
      <td><label for="url">URL</label></td>
      <td width="600"><input id="url" type="text" name="url" required> </td>
    </tr>  
    <tr>
      <td><label for="keywords">Keywords</label></td>
      <td width="600"><input id="keywords" type="text" name="keywords" placeholder="examples: metadynamics, RNA, protein folding, small molecules, ..." required></td>
    </tr>
    <tr>
      <td><label for="instructor">Instructors</label></td>
      <td width="600"><input id="instructor" type="text" name="instructor" required></td>
    </tr>
    <tr>
      <td><label for="contact">Contact</label></td>
      <td width="600"><input id="contact" type="text" name="contact" required></td>
    </tr>
    <tr>
      <td><label for="email">Contact email</label></td>
      <td width="600"><input id="email" type="text" name="_replyto" required></td>
    </tr>  
    <tr>
      <td><label for="comments">Comments<sup>*</sup></label></td>
      <td width="600"><input id="comments" type="text" name="comments"></td>
    </tr>
  </table>
  <input type="text" name="_gotcha" style="display:none"> <br>
  <button type="submit">Submit</button>
  <input type="hidden" name="_subject" id="_subject" value="PLUMED-TUTORIALS submission"> <br>
</form>

<style>
form.wj-contact input[type="text"], form.wj-contact textarea[type="text"], form.wj-contact input[type="email"]{
    width: 100%;
    height: 100%;
    vertical-align: middle;
    padding: 0.25em;
    font-family: monospace, sans-serif;
    font-weight: lighter;
    border-style: solid;
    border-color: #444;
    outline-color: #2e83e6;
    border-width: 1px;
    border-radius: 3px;
    transition: box-shadow .2s ease;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: auto;
    margin-right: auto
    box-sizing: border-box;
}
</style>
    
