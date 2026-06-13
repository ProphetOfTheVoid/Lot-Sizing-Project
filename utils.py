from pathlib import Path
import ollama, re, json


# UTILS FUNCTIONS
def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_description(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".txt":
        return load_text_file(path)
    else:
        raise ValueError(f"File format not supported: {ext}")

def load_mip_model(path: str) -> str:
    supported = {".jl", ".mod", ".lp", ".txt"}
    ext = Path(path).suffix.lower()
    if ext not in supported:
        raise ValueError(f"File format not supported: {ext}")
    return load_text_file(path)

def load_prompt(prompt_path: str, instance: str) -> str:
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{instance}", instance)

def query_llm(system_prompt: str, user_prompt: str, model: str, instance: str) -> str:
    ref1_lp = load_text_file("small1.lp")
    ref1_json = load_text_file("small1_mapped.json")
    ref2_lp = load_text_file("medium_4p5t.lp")
    ref2_json = load_text_file("4p5t_mapped.json")
    ref3_lp = load_text_file("medium_4p6t.lp")
    ref3_json = load_text_file("4p6t_mapped.json")

    p = "Exactly. That's the output I expected. Now, do the same on the following file. Before producing the output, reason step by step:\n 1. first identify which variables are binary\n 2.trace the balance constraints to determine how many products and periods there are\n 3.assign role, j and t to each variable"
    response = ollama.chat(
        model=model,
        
        messages=[
            #{"role": "system", "content": system_prompt},
            #{"role": "user", "content": user_prompt}

            {"role": "user", "content": "Do NOT solve the optimization problem. Do NOT write code. Your ONLY task is to execute a semantic mapping on the new file, specifying the type, period and product for every variableb in the .lp file.\n\nHere is an example of a .lp file: \n\n" + ref1_lp},
            {"role": "assistant", "content": ref1_json},
            {"role": "user", "content": "Good. That's a correct mapping. Do it again on this slightly bigger instance: \n\n" + ref2_lp},
            {"role": "assistant", "content": ref2_json},
            {"role": "user", "content": "Perfect. Now, try with a bigger instace: \n\n" + ref3_lp},
            {"role": "assistant", "content": ref3_json},
            {"role": "user", "content": p + "Here is the file:\n\n" + instance}
        ],
        format="json"
    )
    return response["message"]["content"]