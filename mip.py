from dataclasses import dataclass, field
from pathlib import Path
from utils import load_file
import re

@dataclass
class LotSizingParams:
    J: int                          # numero di prodotti
    T: int                          # numero di periodi
    d: list[list[float]]            # d[j][t]  domanda
    c: list[list[float]]            # c[j][t]  costo produzione
    f: list[list[float]]            # f[j][t]  costo stock
    g: list[list[float]]            # g[j][t]  costo setup
    K: float                        # capacità produzione per prodotto
    R: float                        # capacità produzione totale
    Q: float                        # capacità stock totale

@dataclass
class MIPModel:
    params: LotSizingParams | None = None
    objective_fun: list[str]        = field(default_factory=list)
    c_balance: list[str]            = field(default_factory=list)  # (2) x_jt - s_jt + s_{j,t-1} = d_jt
    c_stock_capacity_q: list[str]   = field(default_factory=list)  # (3) sum s_jt <= Q
    c_prod_capacity_k: list[str]    = field(default_factory=list)  # (4) x_jt <= K * y_jt
    c_prod_capacity_r: list[str]    = field(default_factory=list)  # (5) sum x_jt <= R
    c_capacity: list[str]           = field(default_factory=list)  # campo generico per vincoli <= senza binarie (usato solo dal parser da file)
    c_binary: list[str]             = field(default_factory=list)  # y_jt in {0,1}

def create_mip_from_file(path: str) -> MIPModel:
    text = load_file(path)
    model = MIPModel()
 
    current_section = None
    raw_constraints = []
    done = False
 
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        low = stripped.lower()
 
        # in which section?
        if low in ("minimize", "maximize"):
            current_section = "objective"
        elif low in ("subject to"):
            current_section = "constraints"
        elif low == "binaries":
            current_section = "binaries"
        elif low == "end":
            done = True
        
        if not done:
            if current_section == "objective":
                model.objective_fun.append(stripped)
            elif current_section == "constraints":
                raw_constraints.append(stripped)
            elif current_section == "binaries":
                model.c_binary.append(stripped)
 
    binary_set = set(model.c_binary)
 
    for line in raw_constraints:
        vars_in_line = set(re.findall(r'x_\d+', line))
        has_binary = bool(vars_in_line & binary_set)
        has_continuous = bool(vars_in_line - binary_set)
 
        if ">=" in line or ("=" in line and "<" not in line):
            model.c_balance.append(line)
        elif "<=" in line and has_binary and has_continuous:
            # x_jt - K y_jt <= 0
            model.c_prod_capacity_k.append(line)
        elif "<=" in line and not has_binary:
            # (3) o (5)
            model.c_capacity.append(line)
 
    return model