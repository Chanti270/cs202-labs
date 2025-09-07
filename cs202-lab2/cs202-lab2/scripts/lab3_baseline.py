import pandas as pd, os, collections, pathlib

IN = "data/file_level.csv"
OUT = "reports/lab3_baseline.md"
pathlib.Path("reports").mkdir(parents=True, exist_ok=True)

df = pd.read_csv(IN)

# Basic counts
n_files = len(df)
n_commits = df["commit"].nunique() if "commit" in df.columns else df["hash"].nunique() if "hash" in df.columns else None
avg_files_per_commit = (n_files / n_commits) if n_commits else None

# File extension distribution
ext = df["file"].astype(str).str.extract(r"(\.[A-Za-z0-9_]+)$")
ext_counts = ext[0].value_counts().head(10)

# Fix-type distribution (best-effort: try to find an LLM fix-type column)
fix_col = None
for c in df.columns:
    lc = c.lower().replace(" ", "")
    if lc in {"llminference(fixtype)","fixtype","llm_inference","llm_fix_type","fix_type"}:
        fix_col = c
        break
fix_counts = None
if fix_col:
    fix_counts = df[fix_col].astype(str).value_counts().head(10)
else:
    # fallback: simple heuristic using developer message keywords
    dev = df.get("developer_msg", pd.Series([""]*len(df))).astype(str).str.lower()
    tmp = pd.Series(["bugfix" if any(k in s for k in ["fix","bug","patch","regression","hotfix"]) else "other"
                     for s in dev])
    fix_counts = tmp.value_counts()

# Write report
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Lab 3 — Baseline Descriptive Statistics\n\n")
    f.write(f"- Total unique commits: **{n_commits}**\n")
    f.write(f"- Total file-level rows: **{n_files}**\n")
    if avg_files_per_commit is not None:
        f.write(f"- Avg. files per commit: **{avg_files_per_commit:.2f}**\n\n")
    f.write("## Top file extensions\n")
    f.write(ext_counts.to_frame("count").to_markdown() + "\n\n")
    f.write("## Fix-type distribution (LLM if present, else heuristic)\n")
    f.write(fix_counts.to_frame("count").to_markdown() + "\n")

print(f"✅ Baseline written to {OUT}")
