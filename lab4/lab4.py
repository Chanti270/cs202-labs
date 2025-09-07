import subprocess
import csv
from pydriller import Repository

# 3 repositories for analysis
repos = [
    "https://github.com/django/django.git",
    "https://github.com/pallets/flask.git",
    "https://github.com/numpy/numpy.git"
]

# Limit number of commits per repo (set None for full history)
COMMIT_LIMIT = 200

# Output CSV
output_file = "final_dataset.csv"

# Write CSV header
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "repo", "old_file_path", "new_file_path",
        "commit_sha", "parent_commit_sha",
        "commit_message", "diff_myers", "diff_hist", "Discrepancy"
    ])

# Process each repo
for repo_url in repos:
    print(f"Processing repository: {repo_url}")

    commits = list(Repository(repo_url).traverse_commits())
    if COMMIT_LIMIT:
        commits = commits[:COMMIT_LIMIT]

    for idx, commit in enumerate(commits, start=1):
        print(f"  Commit {idx}/{len(commits)}: {commit.hash[:7]}")

        parent = commit.parents[0] if commit.parents else None

        try:
            for mod in commit.modified_files:   # this may throw errors
                try:
                    # Myers diff (default in PyDriller)
                    diff_myers = mod.diff or ""

                    # Histogram diff (via git command)
                    diff_hist = ""
                    if parent:
                        result = subprocess.run(
                            ["git", "diff", "--histogram", parent, commit.hash, "--", mod.new_path or mod.old_path or ""],
                            capture_output=True, text=True
                        )
                        diff_hist = result.stdout.strip()

                    # Compare diffs
                    discrepancy = "No"
                    if diff_myers.strip() != diff_hist.strip():
                        discrepancy = "Yes"

                    # Save row
                    with open(output_file, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            repo_url,
                            mod.old_path,
                            mod.new_path,
                            commit.hash,
                            parent,
                            commit.msg,
                            diff_myers,
                            diff_hist,
                            discrepancy
                        ])

                except Exception as e:
                    print(f"    ⚠️ Error processing file in commit {commit.hash}: {e}")

        except Exception as e:
            print(f"  ⚠️ Skipping commit {commit.hash} due to error: {e}")

print(f"\n✅ Analysis complete! Results saved in {output_file}")
