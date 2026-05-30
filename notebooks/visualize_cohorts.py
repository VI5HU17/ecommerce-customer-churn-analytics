import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

print("🎨 Initializing Cohort Visualization Engine...")

# 1. Load our calculated percentage retention matrix
source_path = os.path.join("data", "cohort_retention_matrix.csv")
retention_matrix = pd.read_csv(source_path, index_col="CohortMonth")

# 2. Set up the corporate plotting canvas
plt.figure(figsize=(16, 10))
plt.title(
    "E-Commerce Customer Retention Rates (%) - Monthly Cohorts",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

# 3. Generate a professional color-coded heatmap
# fmt='.1f' ensures numbers display cleanly to 1 decimal place
sns.heatmap(
    data=retention_matrix,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar_kws={"label": "Retention Rate (%)"},
)

# 4. Clean up labels for executive presentation
plt.ylabel("Cohort Start Month", fontsize=12, fontweight="bold")
plt.xlabel("Months Passed (Cohort Index)", fontsize=12, fontweight="bold")

# Adjust layout so labels don't get clipped
plt.tight_layout()

# 5. Save the visual asset directly into our repository
output_path = os.path.join("templates", "cohort_retention_heatmap.png")
plt.savefig(output_path, dpi=300)

print("\n🎉 SUCCESS!")
print(f"🖼️ Publication-grade heatmap saved locally at: {output_path}")