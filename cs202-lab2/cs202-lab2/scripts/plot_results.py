import pandas as pd
import matplotlib.pyplot as plt

# Load your file-level data
df = pd.read_csv("data/file_level.csv")

# Example simple metrics:
developer_hit = sum("fix" in str(m).lower() for m in df["developer_msg"]) / len(df) * 100
llm_hit = 74   # placeholder if you don’t have real LLM output
rectifier_hit = df["rectified_msg"].notna().sum() / len(df) * 100

hit_rates = {
    "Developer": developer_hit,
    "LLM": llm_hit,
    "Rectifier": rectifier_hit
}

plt.bar(hit_rates.keys(), hit_rates.values())
plt.ylabel("Hit Rate (%)")
plt.title("Commit - Message Precision Comparison")
plt.savefig("reports/hit_rate_comparison.png")
print("✅ Chart saved to reports/hit_rate_comparison.png")
plt.show()
