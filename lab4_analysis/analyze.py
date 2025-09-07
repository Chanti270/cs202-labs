import matplotlib.pyplot as plt
import numpy as np

# Example data
categories = ['README', 'Test Suites', 'Source Files', 'License']
expected_counts = [10, 12, 12, 1]   # expected or ideal counts
actual_counts   = [9, 10, 12, 0]    # what is actually present

# Bar graph for mismatches
x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, expected_counts, width, label='Expected', color='skyblue')
ax.bar(x + width/2, actual_counts, width, label='Actual', color='salmon')

# Labels and title
ax.set_ylabel('Counts')
ax.set_title('Mismatch between README, Test Suites, Source Files, and License')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# Annotate mismatches
for i in range(len(categories)):
    mismatch = expected_counts[i] - actual_counts[i]
    if mismatch != 0:
        ax.text(i, max(expected_counts[i], actual_counts[i]) + 0.2,
                f'Mismatch: {mismatch}', ha='center', color='black')

plt.tight_layout()
plt.show()
