import json, re
from utils import load_description, load_mip_model, load_text_file, load_prompt, query_llm
from truth import generate_mapping_grounded


# GLOBAL VARIABLES
MODEL = "mistral-small:22b"
DESCRIPTION_FILE = "description.txt"
INSTANCE_FILE = "medium_4p5t.lp"
SYS_PROMPT_FILE = "system_prompt.txt"
USR_PROMPT_FILE = "user_prompt.txt"
OUTPUT_PATH = "mapping.json"

#-----------------------------------------

#-----------------------------------------
def main():
    instance = load_mip_model(INSTANCE_FILE)
    sys_prompt = load_text_file(SYS_PROMPT_FILE)
    usr_prompt = load_prompt(USR_PROMPT_FILE, instance)

    o_def = generate_mapping_grounded(INSTANCE_FILE)
    with open("truth.json", "w", encoding="utf-8") as f:
        json.dump(o_def, f, indent=2)    
    
    print(f"Mapping ground-truth completed")


    output = query_llm(sys_prompt, usr_prompt, MODEL, instance)
    print("=== RAW OUTPUT ===")
    print(output)
    print("=== END RAW ===")
    parsed = json.loads(output)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)    

    print(f"Mapping AI completed")

if __name__=="__main__":
    main()