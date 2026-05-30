import os
import numpy as np
import pandas as pd

print("🧮 Initializing Cohort Math Engine...")

# 1. Load our immaculate, cleaned transaction dataset
source_path = os.path.join("data", "online_retail_clean.csv")
df = pd.read_csv(source_path)

# Convert InvoiceDate back to a datetime object for date calculations
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])


# 2. Assign Transaction Month and Cohort Month
# Function to truncate dates to year-month period format (e.g., 2010-12)
def get_month(x):
    return pd.to_datetime(df["InvoiceDate"]).dt.to_period("M")


df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")

# Find the absolute first purchase month for every unique user
df["CohortMonth"] = df.groupby("CustomerID")["InvoiceMonth"].transform("min")


# 3. Calculate Cohort Index (The number of months passed since the first purchase)
def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    return year, month


invoice_year, invoice_month = get_date_int(df, "InvoiceMonth")
cohort_year, cohort_month = get_date_int(df, "CohortMonth")

# Years difference * 12 + months difference
years_diff = invoice_year - cohort_year
months_diff = invoice_month - cohort_month

# Index 0 means purchase happened in their first month, 1 means month 2, etc.
df["CohortIndex"] = years_diff * 12 + months_diff


# 4. Construct the Retention Pivot Table Matrix
# Group by original cohort cohort month and index step, counting unique customers
cohort_data = (
    df.groupby(["CohortMonth", "CohortIndex"])["CustomerID"]
    .nunique()
    .reset_index()
)

# Pivot the data into a beautiful matrix spreadsheet layout
cohort_matrix = cohort_data.pivot(
    index="CohortMonth", columns="CohortIndex", values="CustomerID"
)

print("\n📊 RAW COHORT SIZE MATRIX (HEAD):")
print(cohort_matrix.iloc[:5, :5])

# 5. Convert Absolute Customer Counts into Percentage Retention Rates
cohort_sizes = cohort_matrix.iloc[:, 0]  # First column is original cohort size
retention_matrix = cohort_matrix.divide(cohort_sizes, axis=0)
retention_matrix = (retention_matrix * 100).round(1)  # Format as percentages

print("\n📉 PERCENTAGE RETENTION MATRIX (HEAD):")
print(retention_matrix.iloc[:5, :5])

# 6. Save matrices to data folder for our upcoming data visualizations
cohort_matrix.to_csv(os.path.join("data", "cohort_counts_matrix.csv"))
retention_matrix.to_csv(os.path.join("data", "cohort_retention_matrix.csv"))
print("\n💾 Analytical matrices calculated and cached successfully in /data!")