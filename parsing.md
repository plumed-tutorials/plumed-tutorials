Parsing action input 
--------------------

The input to any PLUMED [action](actions.md) consists of a series of keyword value pairs and flags that turn on or off various options.  
In the example input below:

```plumed
d1: DISTANCE ATOMS=1,2 NOPBC
```

`d1` is the action's [label](specifying_arguments.md) and `DISTANCE` is the action's name.  The input to the action is then the keyword value pair ATOMS and the flag NOPBC.
Every example input you encounter in this manual, in the [nest](www.plumed-nest.org) and the [tutorials](www.plumed-tutorials.org) has tooltips
that explain what options are turned on by flags and what the values provided in each keyword pair represents.  You will also find details of
all the keywords and flags that are available for an action on the manual page for that action.

## Reading constants

## Special replica syntax
