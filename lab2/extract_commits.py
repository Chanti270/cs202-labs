from pydriller import Repository
import pandas as pd

commits_data = []
for commit in Repository('.').traverse_commits():
    if any(word in commit.msg.lower() for word in ['fix', 'bug', 'error', 'issue']):
        commits_data.append([
            commit.hash, 
            commit.msg, 
            [p.hash for p in commit.parents], 
            commit.merge, 
            [mod.filename for mod in commit.modified_files]
        ])

df = pd.DataFrame(commits_data, columns=["Hash","Message","ParentHashes","IsMerge","ModifiedFiles"])
df.to_csv("bug_fix_commits.csv", index=False)
print("✅ Extracted commits saved to bug_fix_commits.csv")
