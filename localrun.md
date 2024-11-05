### How to test locally that your tutorial can be compiled


You can run a compilation test on a single lesson from your desktop

```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
python testLesson.py -h
python testLesson.py path/to/lesson.yml
```
You will need a runnable `plumed` avaiable at the time of launching `python testLesson.py`

the lesson.yml file must me preparated as normally, like:
```yaml
url: https://github.com/Iximiel/plumed-school-benchmark/releases/download/School/plumed-school-benchmark.zip
instructors: Daniele Rapetti
title: Benchmarking PLUMED 
description: This tutorial shows you how to use the plumed benchmark tool to measure the performance of the code
doi: unpublished
tags: developers, benchmark, manual
```
This test will only check if the lesson will be compiled by the GitHub CI,
the correcteness of the rendering will not be checked.
