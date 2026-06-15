# AI-driven mapper for Lot Sizing Problems

## Context
Traditional MIP solvers naively handle variables and constraints, instantiating them in the same manner regardless of their role and assigning indices solely based on their order of appearance. In single-index MIP problems, this isn’t an issue, and the solver can still provide solutions within acceptable time spans. In multi-index time-dependent problems (i.e. the Lot Sizing Problem) instances of considerable dimensions, solvers handle variables and constraints using the same naive logic, which makes finding integer pseudo-optimal solutions less efficient. Not knowing whether *v_k* is an *x_jt* or a *y_jt* variable, nor the values of the indices *i* and *j* leads to inefficient handling in the solver-side.

The solution to the aforementioned issue is a tailored solver for multi-index MIP problems. An entity which, if provided with a proper data structure as input, solves the problem and achieves a better performance compared to the traditional solver.
This project activity is centred around the preliminary step of the pipeline involving said ‘ad-hoc’ solver: obtaining a data structure to use as input starting from an instance of an MIP problem belonging to a known category of problems through a process of semantic mapping.

To achieve semantic mapping, the component must:
1. Analyse the instance file (.lp), which represents every variable as *x_k*
2. Identify the role of each *x_k* by observing in which constraints it appears (e.g. the variables *y_jt* are the only ones in the binary constraints)
3. Identify the value of the indexes *j* and *t* for each inferred variable
4. Produce an output file in an easy-to-handle data format

## Double query types
This component contains two methods of queries: prompted and promptless. The experimentations lead to discard the prompted approach, based on providing an accurate description of the task, as well as the LSP. Intead, the promptless attempt exploited the generalisation capabilities of the model, having it infer the task to be performed by observing a fake conversation with examples and expected results. Nonethelss, the prompted methods is still implemented, although no benchmark has been run on it since changing to the other model. If one wishes to employ the prompted version, they might have to update the files in the `prompt` folder.

## Repository structure
The repository is structured as follows:
* `main.py` summons the function contained in other files, and handles the output
* `utils.py` contains utils functions (e.g. load file, send query) summoned by other components
* `truth.py` is the ground-truth: it performs a correct mapping without the use of AI. Used to check whether the AI made mistakes.
* `mip.py` contains classes and methods used by `truth.py`. Shouldn't be touched.
* The `output` folder is where the two output files are: `truth.json`, produced by `truth.py` and `mapping.json`, produced by the LLM. Each run, they're automatically updated with the new results.
* The `instances` folder contains both the .lp files, as well as some already solved instances, used in the prompt as expected results
* The `prompt` folder contains `description.txt`, `user_prompt.txt` and `system_prompt.txt`, all used in the Prompted Query method.

## Guide to usage
To execute the program, position in the `Lot Sizing` folder and run: `python .\main.py`

Head to `main.py` if you wish to:
* Change the instance (.lp) file
* Change model, description file, prompt files or output path (global variables)
* Change between prompted and promptless query (~ line 40) 
* Change from sorted to unsorted variable order in the output files (unsorted means they'll be ordered by index)

Head to `utils.py` if you wish to:
* Edit the pre-loaded conversation for the Promptless Query method (e.g. adding another example and its expected output, switching examples, increasing context size).


