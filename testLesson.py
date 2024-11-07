# this is using ruff==0.6.2 to check that the code won't explode badly
# pip install ruff==0.6.2
# ruff format testLesson.py
# ruff check testLesson.py


DEFAULT_PLUMED = "plumed"
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog="testLesson",
        description="""
Test the correctness (if the lesson can be compiled) of a single lesson.

%(prog)s needs plumed installed and runnable to work.

%(prog)s will check only if the lesson can be compiuled and could pass the GitHub workflow.
Note that %(prog)s will not find any rendering error due to wrong Markdown or HTML syntax.
""",
    )
    parser.add_argument(
        "lessonPath",
        help="The path to the lesson.yml file to test or to the directory containing it",
    )
    args = parser.parse_args()

    from compile import process_lesson
    import subprocess
    import json
    import sys

    lessonPath = args.lessonPath
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

    if "lesson.yml" in lessonPath:
        lessonPath = lessonPath.replace("lesson.yml", "")
    process_lesson(lessonPath, action_counts, plumed_syntax, plumeds_to_use=(plumed_to_use,),plumed_version_names=("local",))
