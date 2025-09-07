import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("../lab4/final_dataset.csv")  # go up 1 folder if needed

# Filter mismatches
mismatches = df[df["Discrepancy"] == "Yes"]

# Count mismatches by file type
counts = {
    "Source Code": mismatches[mismatches["new_file_path"].str.endswith((".py", ".java", ".cpp"), na=False)].shape[0],
    "Test Files": mismatches[mismatches["new_file_path"].str.contains("test", case=False, na=False)].shape[0],
    "README": mismatches[mismatches["new_file_path"].str.contains("README", case=False, na=False)].shape[0],
    "LICENSE": mismatches[mismatches["new_file_path"].str.contains("LICENSE", case=False, na=False)].shape[0],
}

# Print counts in terminal
print("\nMismatch Counts by File Type:")
for k, v in counts.items():
    print(f"{k}: {v}")

# Create bar plot
plt.bar(counts.keys(), counts.values())
plt.title("Mismatch Counts by File Type")
plt.xlabel("File Type")
plt.ylabel("Mismatch Count")
plt.tight_layout()
plt.savefig("mismatch_plot.png")  # save plot as image
plt.show()

print("\n✅ Plot saved as mismatch_plot.png")
