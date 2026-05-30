import os
import pandas as pd

print("🚀 Starting Data Ingestion Pipeline...")

# Active repository mirror for the Online Retail Dataset
url = "https://raw.githubusercontent.com/shricharan-ks/Retail-datasets/master/Online%20Retail.csv"

print("📥 Streaming over 500,000 rows of transactions...")
df = pd.read_csv(url, encoding="ISO-8859-1")

# Save directly to our data directory
target_path = os.path.join("data", "online_retail.csv")
df.to_csv(target_path, index=False)

print("\n🎉 SUCCESS!")
print(f"📊 Matrix Dimensions: {df.shape[0]:,} rows x {df.shape[1]} columns")