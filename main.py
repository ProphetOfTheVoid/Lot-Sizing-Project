import json
from utils import load_file, setup_prompt, promptless_query_llm, prompted_query_llm
from truth import generate_mapping_grounded, sort_mapping


# GLOBAL VARIABLES
MODEL = "mistral-small:22b"
DESCRIPTION_FILE = "description.txt"
INSTANCE_FILE = "instances/4p5t.lp"
SYS_PROMPT_FILE = "system_prompt.txt"
USR_PROMPT_FILE = "user_prompt.txt"
OUTPUT_PATH = "mapping.json"

#-----------------------------------------

#-----------------------------------------
def main():
    # Summonign functions that prepare everything
    instance = load_file(INSTANCE_FILE)
    description = load_file(DESCRIPTION_FILE)
    sys_prompt = load_file(SYS_PROMPT_FILE)
    usr_prompt = setup_prompt(USR_PROMPT_FILE, instance)

    print(f"Starting mapping for instance file: {INSTANCE_FILE}")

    # Invoking the non-AI mapper
    o_def = generate_mapping_grounded(INSTANCE_FILE)
    with open("truth.json", "w", encoding="utf-8") as f:
        json.dump(sort_mapping(o_def), f, indent=2)
    
    print(f"Mapping ground-truth completed")

    # Invoking the LLM to query the mapping
    #output = prompted_query_llm(description, sys_prompt, usr_prompt, MODEL, instance)
    output = promptless_query_llm(MODEL, instance)
    
    #print("=== RAW OUTPUT ===")
    #print(output)
    #print("=== END RAW ===")
    
    parsed = json.loads(output)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sort_mapping(parsed), f, indent=2)    

    print(f"Mapping AI completed and stored in {OUTPUT_PATH}")

if __name__=="__main__":
    main()