import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

print("🎨 Initializing RFM Visualization Engine...")

# 1. Load our customer segment database
source_path = os.path.join("data", "customer_rfm_segments.csv")
rfm = pd.read_csv(source_path)

# 2. Calculate the volume per segment
segment_counts = rfm["General_Segment"].value_counts().reset_index()
segment_counts.columns = ["Customer Segment", "Total Customers"]

# 3. Initialize professional plotting canvas
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")

# Create a clean horizontal bar chart for high readability
ax = sns.barplot(
    x="Total Customers",
    y="Customer Segment",
    data=segment_counts,
    palette="viridis",
    hue="Customer Segment",
    legend=False,
)

# 4. Add corporate labels and data values onto the bars
for index, value in enumerate(segment_counts["Total Customers"]):
    ax.text(value + 15, index, f"{value:,}", va="center", fontweight="bold")

plt.title(
    "Enterprise Customer Segmentation Distribution (RFM Model)",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.xlabel("Total Customer Count", fontsize=12, fontweight="bold")
plt.ylabel("Strategic Behavioral Segment", fontsize=12, fontweight="bold")

plt.xlim(0, max(segment_counts["Total Customers"]) * 1.15)
plt.tight_layout()

# 5. Save the final visual asset
output_path = os.path.join("templates", "customer_rfm_distribution.png")
plt.savefig(output_path, dpi=300)

print("\n🎉 SUCCESS!")
print(f"🖼️ Executive distribution chart saved at: {output_path}")
