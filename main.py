import json, time
from utils import load_file, setup_prompt, promptless_query_llm, prompted_query_llm
from truth import generate_mapping_grounded, sort_mapping


# GLOBAL VARIABLES
MODEL = "gemma4:latest"
DESCRIPTION_FILE = "prompt/description.txt"
INSTANCE_FILE = "instances/3p10t.lp"
SYS_PROMPT_FILE = "prompt/system_prompt.txt"
USR_PROMPT_FILE = "prompt/user_prompt.txt"
OUTPUT_PATH = "output/mapping.json"
TRUTH_PATH = "output/truth.json"

#-----------------------------------------

#-----------------------------------------
def main():
    # Summonign functions that prepare everything
    instance = load_file(INSTANCE_FILE)
    description = load_file(DESCRIPTION_FILE)
    sys_prompt = load_file(SYS_PROMPT_FILE)
    usr_prompt = setup_prompt(USR_PROMPT_FILE, instance)

    print(f"Starting mapping for instance file: {INSTANCE_FILE}\n")

    # Invoking the non-AI mapper
    o_def = generate_mapping_grounded(INSTANCE_FILE)
    with open(TRUTH_PATH, "w", encoding="utf-8") as f:
        json.dump(sort_mapping(o_def), f, indent=2)
        #json.dump(o_def, f, indent=2)
    
    print(f"Mapping ground-truth completed")
    start = time.time()

    
    # Invoking the LLM to query the mapping
    #output = prompted_query_llm(description, sys_prompt, usr_prompt, MODEL, instance)
    output = promptless_query_llm(MODEL, instance)
    
    #print("=== RAW OUTPUT ===")
    #print(output)
    #print("=== END RAW ===")
    
    parsed = json.loads(output)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sort_mapping(parsed), f, indent=2)    
    

    end = time.time()
    print(f"Mapping AI completed and stored in {OUTPUT_PATH}")
    print(f"Elasped time for LLM query: {(end-start)/60} minutes")

if __name__=="__main__":
    main()