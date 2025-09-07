import argparse, pandas as pd
from pydriller import Repository

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--commits", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    commits = pd.read_csv(args.commits)
    hashes = set(commits["hash"])

    rows = []
    for commit in Repository(args.repo).traverse_commits():
        if commit.hash not in hashes:
            continue
        for f in commit.modified_files:
            rows.append({
                "commit": commit.hash,
                "file": f.filename,
                "old_code": f.source_code_before,
                "new_code": f.source_code,
                "developer_msg": commit.msg,
                "rectified_msg": "Refined: " + commit.msg.capitalize()
            })

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print(f"✅ Saved {len(rows)} file-level changes to {args.out}")

if __name__ == "__main__":
    main()
