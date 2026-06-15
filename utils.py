from pathlib import Path
import ollama


def load_file(path: str) -> str:
    supported = {".jl", ".lp", ".txt", ".json"}
    extension = Path(path).suffix.lower()

    if extension not in supported:
        raise ValueError(f"\nFile format not supported: {extension}")
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

# The prompt contains a placeholder {instance} in place of the actual instance to save up space
# This function replaces the placeholder with the actual instance
def setup_prompt(prompt_path: str, instance: str) -> str:
    template = load_file(prompt_path)
    return template.replace("{instance}", instance)

# Old approach: prompt contains all info and guidelines
def prompted_query_llm(description: str, system_prompt: str, user_prompt: str, model: str, instance: str) -> str:
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": description + "\n" + system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        format="json"
    )
    return response["message"]["content"]

# New approach. No prompt: let the LLM infere the task from the fake conversation
def promptless_query_llm(model: str, instance: str) -> str:

    # CHANGE HERE AS NEEDED
    ref1_lp = load_file("instances/3p5t_first.lp")
    ref1_json = load_file("instances/3p5t_first_mapped.json")
    ref2_lp = load_file("instances/4p5t.lp")
    ref2_json = load_file("instances/4p5t_mapped.json")
    ref3_lp = load_file("instances/4p6t.lp")
    ref3_json = load_file("instances/4p6t_mapped.json")

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
            {"role": "user", "content": "Exactly. That's the output I expected. Here, try with this instance now:\n\n" + instance}
        ],
        options={
            "num_ctx": 32768  # 32768 or 16384
        },
        format="json"


    )
    return response["message"]["content"]