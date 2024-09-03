# this is using ruff==0.6.2 to check that the code won't explode badly
# pip install ruff==0.6.2
# ruff format testLesson.py
# ruff check testLesson.py
from compile import process_lesson

DEFAULT_PLUMED = "plumed"
if __name__ == "__main__":
    import subprocess
    import json
    import sys

    # args here:
    # first "naked" argument is the path to lesson.y(a)ml
    plumed_to_use = DEFAULT_PLUMED
    cmd = [plumed_to_use, "info", "--root"]
    plumed_info = subprocess.run(cmd, capture_output=True, text=True)
    keyfile = plumed_info.stdout.strip() + "/json/syntax.json"

    with open(keyfile) as f:
        try:
            plumed_syntax = json.load(f)
        except ValueError as ve:
            raise json.InvalidJSONError(ve)

    action_counts = {}
    for key in plumed_syntax:
        if key == "vimlink" or key == "replicalink" or key == "groups":
            continue
        action_counts[key] = 0

    lessonPath = sys.argv[1]
    if "lesson.yml" in lessonPath:
        lessonPath = lessonPath.replace("lesson.yml", "")
    process_lesson(sys.argv[1], action_counts, plumed_syntax)
