import pandas as pd, math, pathlib
from radon.metrics import mi_visit
from radon.complexity import cc_visit
from radon.raw import analyze

IN = "data/file_level.csv"
OUT = "data/lab3_metrics.csv"
pathlib.Path("data").mkdir(parents=True, exist_ok=True)

def safe(s): 
    if isinstance(s, float) and math.isnan(s): return ""
    return "" if s is None else str(s)

def mi(code):
    code = safe(code)
    if not code.strip(): return float("nan")
    try: return float(mi_visit(code, False))
    except: return float("nan")

def cc_avg(code):
    code = safe(code)
    if not code.strip(): return float("nan")
    try:
        blocks = cc_visit(code)
        if not blocks: return 0.0
        return sum(b.complexity for b in blocks) / len(blocks)
    except: return float("nan")

def sloc(code):
    code = safe(code)
    if not code.strip(): return 0
    try: return analyze(code).sloc
    except: return 0

df = pd.read_csv(IN)
df["MI_Before"]  = df["old_code"].apply(mi)
df["MI_After"]   = df["new_code"].apply(mi)
df["CC_Before"]  = df["old_code"].apply(cc_avg)
df["CC_After"]   = df["new_code"].apply(cc_avg)
df["LOC_Before"] = df["old_code"].apply(sloc)
df["LOC_After"]  = df["new_code"].apply(sloc)

df["MI_Change"]  = df["MI_After"] - df["MI_Before"]
df["CC_Change"]  = df["CC_After"] - df["CC_Before"]
df["LOC_Change"] = df["LOC_After"] - df["LOC_Before"]

df.to_csv(OUT, index=False)
print(f"✅ Structural metrics saved to {OUT}")
