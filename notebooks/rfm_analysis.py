import os
import datetime as dt
import pandas as pd
import numpy as np

print("📊 Initializing Advanced RFM & Churn Modeling Engine...")

# 1. Load our immaculate cleaned dataset
source_path = os.path.join("data", "online_retail_clean.csv")
df = pd.read_csv(source_path)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 2. Establish a snapshot date (pretend we are analyzing the data the day after the last transaction)
snapshot_date = df["InvoiceDate"].max() + dt.timedelta(days=1)
print(f"• System Snapshot Date for Recency Calculations: {snapshot_date.date()}")

# 3. Aggregate transaction data per Customer ID
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days, # Days since last order (Recency)
    "InvoiceNo": "nunique",                                  # Unique orders placed (Frequency)
    "TotalSpent": "sum"                                      # Total capital spent (Monetary)
})

# Rename attributes for clean database management
rfm.rename(columns={
    "InvoiceDate": "Recency",
    "InvoiceNo": "Frequency",
    "TotalSpent": "Monetary"
}, inplace=True)

# 4. Statistical Scoring via Quintiles (Cut data into 5 equal 20% slices)
# For Recency, a smaller number is better (recent), so labels count down from 5 to 1
r_labels = range(5, 0, -1)
# For Frequency & Monetary, bigger numbers are better, so labels count up from 1 to 5
f_labels = range(1, 6)
m_labels = range(1, 6)

rfm["R"] = pd.qcut(rfm["Recency"], q=5, labels=r_labels)
rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=f_labels)
rfm["M"] = pd.qcut(rfm["Monetary"], q=5, labels=m_labels)

# Concatenate scores into a unique algorithmic string (e.g., '555' or '111')
rfm["RFM_Segment"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)
rfm["RFM_Score"] = rfm[["R", "F", "M"]].sum(axis=1)

# 5. Algorithmic Corporate Segmentation Mapping
def segment_me(df):
    score = df["RFM_Score"]
    segment = "Standard Client"
    
    if score >= 14:
        segment = "Champions (Core Value)"
    elif (score >= 11) and (score < 14):
        segment = "Loyal & High-Value"
    elif (score >= 8) and (score < 11):
        segment = "Custom Retention Needed"
    elif (score >= 5) and (score < 8):
        segment = "At-Risk / Slipping"
    else:
        segment = "High Churn / Lost Segment"
        
    return segment

rfm["General_Segment"] = rfm.apply(segment_me, axis=1)

print("\n📈 RFM SEGMENTATION MATRIX COMPLETED (PREVIEW):")
print(rfm[["Recency", "Frequency", "Monetary", "RFM_Segment", "General_Segment"]].head())

print("\n🏢 CORPORATE CLIENT GROUP DISTRIBUTION:")
print(rfm["General_Segment"].value_value_counts() if hasattr(rfm["General_Segment"], 'value_value_counts') else rfm["General_Segment"].value_counts())

# 6. Cache the output matrix safely
output_path = os.path.join("data", "customer_rfm_segments.csv")
rfm.to_csv(output_path)
print(f"\n💾 Strategic segment maps saved locally at: {output_path}")