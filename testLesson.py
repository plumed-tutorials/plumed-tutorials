# this is using ruff==0.6.2 to check that the code won't explode badly
# pip install ruff==0.6.2
# ruff format testLesson.py
# ruff check testLesson.py

from compile import process_lesson, prepare_action_count_and_syntax



DEFAULT_PLUMED = "plumed"
if __name__ == "__main__":
    import subprocess
    import json
    import sys

    # args here:
    # first "naked" argument is the path to lesson.y(a)ml
    plumed_to_use = DEFAULT_PLUMED
    action_counts, plumed_syntax = prepare_action_count_and_syntax(plumed_to_use)

    lessonPath = sys.argv[1]
    if "lesson.yml" in lessonPath:
        lessonPath = lessonPath.replace("lesson.yml", "")
    process_lesson(lessonPath, action_counts, plumed_syntax)
