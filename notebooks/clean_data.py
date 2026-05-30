import os
import pandas as pd

print("⚙️ Initializing Core Data Cleaning Pipeline...")

# 1. Load our locally cached raw transaction dataset
source_path = os.path.join("data", "online_retail.csv")
df_raw = pd.read_csv(source_path, encoding="ISO-8859-1")

print(f"• Baseline Data Loaded: {df_raw.shape[0]:,} records.")

# 2. Audit Missing Fields
print("\n🔍 Auditing Data Matrix Gaps...")
print(df_raw.isnull().sum())

# 3. Execute Deep Corporate Cleaning Steps
df_clean = df_raw.copy()

# A. Drop records lacking a CustomerID (cohort tracking requires individual identification)
df_clean = df_clean.dropna(subset=["CustomerID"])
df_clean["CustomerID"] = df_clean["CustomerID"].astype(int).astype(str)

# B. Standardize date timelines to true datetime objects
df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"])

# C. Strip trailing whitespace from descriptions
df_clean["Description"] = df_clean["Description"].str.strip()

# D. Remove retail cancellations (Quantity <= 0) and zero/negative pricing anomalies
df_clean = df_clean[(df_clean["Quantity"] > 0) & (df_clean["UnitPrice"] > 0)]

# E. Feature Engineering: Create the explicit revenue generation metric
df_clean["TotalSpent"] = df_clean["Quantity"] * df_clean["UnitPrice"]

print("\n✨ PIPELINE CLEANING RESULTS:")
print(f"• Pristine Records Retained: {df_clean.shape[0]:,}")
print(f"• Rows Purged (Noise/Anomalies): {df_raw.shape[0] - df_clean.shape[0]:,}")

# 4. Save the immaculate dataset for our mathematical cohort analysis
target_path = os.path.join("data", "online_retail_clean.csv")
df_clean.to_csv(target_path, index=False)
print(f"\n💾 Pristine dataset cached safely at: {target_path}")