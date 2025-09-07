import argparse, pandas as pd
from pydriller import Repository
from tqdm import tqdm

BUGFIX_KEYWORDS = ["fix", "bug", "error", "issue", "patch", "hotfix", "regression"]

def is_bugfix(msg: str) -> bool:
    return any(kw in msg.lower() for kw in BUGFIX_KEYWORDS)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-commits", type=int, default=500)
    args = ap.parse_args()

    rows = []
    for i, commit in enumerate(tqdm(Repository(args.repo).traverse_commits())):
        if i >= args.max_commits:
            break
        rows.append({
            "hash": commit.hash,
            "msg": commit.msg,
            "is_bugfix": is_bugfix(commit.msg),
            "n_files": len(commit.modified_files)
        })
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f"✅ Saved {len(rows)} commits to {args.out}")

if __name__ == "__main__":
    main()

