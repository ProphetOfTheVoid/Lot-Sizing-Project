import re
from mip import MIPModel, create_mip_from_file

def extract_prod_capacity(model: MIPModel) -> dict[str, str]:
    x_to_y = {}
    for line in model.c_prod_capacity_k:
        vars_pos = re.findall(r'\+ (x_\d+)', line)
        vars_neg = re.findall(r'- \d+ (x_\d+)', line)
        if vars_pos and vars_neg:
            x_to_y[vars_pos[0]] = vars_neg[0]
    return x_to_y

def parse_balance_constraints(lines: list[str]) -> dict:
    results = {}
    for line in lines:
        vars_pos = re.findall(r'\+ (x_\d+)', line)
        vars_neg = re.findall(r'- (x_\d+)', line)
        x_a = vars_pos[0]
        x_s = vars_pos[1] if len(vars_pos) > 1 else None  
        x_p = vars_neg[0] if vars_neg else None
        results[x_a] = {"x_s": x_s, "x_p": x_p}
    return results

def resolve_periods(x_to_y_dict, balance_results):
    mapping = {}
    
    prev_stock_to_prod = {v["x_s"]: k for k, v in balance_results.items() if v["x_s"] is not None}
    
    first_periods = [x for x, v in balance_results.items() if v["x_s"] is None]
    
    for j, x_jt_0 in enumerate(first_periods):
        t = 0  # changed from 1
        current = x_jt_0
        while current is not None:
            x_s = balance_results[current]["x_s"]
            x_p = balance_results[current]["x_p"]
            y = x_to_y_dict[current]
            
            mapping[current] = {"role": "x", "j": j, "t": t}
            if x_p:
                mapping[x_p] = {"role": "s", "j": j, "t": t}
            if x_s:
                mapping[x_s] = {"role": "s", "j": j, "t": t - 1}  # becomes -1 for first period, was 0
            mapping[y] = {"role": "y", "j": j, "t": t}
            
            current = prev_stock_to_prod.get(x_p)
            t += 1
    
    return mapping

def sort_mapping(mapping: dict) -> dict:
    return dict(sorted(mapping.items(), key=lambda item: int(item[0].split('_')[1])))

def generate_mapping_grounded(instance_file: str) -> dict:
    instance = create_mip_from_file(instance_file)

    x_to_y = extract_prod_capacity(instance)
    balance_results = parse_balance_constraints(instance.c_balance)
    mapping = resolve_periods(x_to_y, balance_results)

    return mapping