import os
import pandas as pd

print("📊 Initializing Interactive Excel Report Engine...")

# 1. Establish file paths
clean_data_path = os.path.join("data", "online_retail_clean.csv")
cohort_path = os.path.join("data", "cohort_retention_matrix.csv")
rfm_path = os.path.join("data", "customer_rfm_segments.csv")
excel_output_path = os.path.join("templates", "Executive_Data_Report.xlsx")

# 2. Load our clean data matrices
df_clean = pd.read_csv(clean_data_path)
df_cohort = pd.read_csv(cohort_path, index_col="CohortMonth")
df_rfm = pd.read_csv(rfm_path)

print("📝 Writing data matrices to multi-sheet Excel Workbook...")

# 3. Use pandas ExcelWriter with the openpyxl engine to compile everything into one workbook
with pd.ExcelWriter(excel_output_path, engine="openpyxl") as writer:
    # Sheet 1: High-Level Cohort Matrix
    df_cohort.to_excel(writer, sheet_name="Cohort Retention Analysis")

    # Sheet 2: Categorized RFM User Segments
    df_rfm.to_excel(writer, sheet_name="Customer RFM Segments", index=False)

    # Sheet 3: Sample of clean records (First 5,000 rows to keep file size lightweight)
    df_clean.head(5000).to_excel(
        writer, sheet_name="Clean Data Sample", index=False
    )

print("\n🎨 Applying professional corporate styling...")

# 4. Open the workbook via openpyxl to inject native conditional color formatting
import openpyxl
from openpyxl.formatting.rule import ColorScaleRule

wb = openpyxl.load_workbook(excel_output_path)
ws_cohort = wb["Cohort Retention Analysis"]

# Apply a smooth Green-to-Yellow-to-Red color gradient to our Cohort matrix rows
# Max retention (100) will be rich green, decaying down to soft white/red
color_scale = ColorScaleRule(
    start_type="num",
    start_value=0,
    start_color="FFFFFF",  # White for low retention
    end_type="num",
    end_value=100,
    end_color="63BE7B",  # Green for high retention
)

# Apply formatting across our matrix grid coordinates (Rows 2-15, Columns C-O)
ws_cohort.conditional_formatting.add("C2:O15", color_scale)

# Save our stylized master template
wb.save(excel_output_path)

print("\n🎉 SUCCESS!")
print(f"📁 Interactive Excel Workbook built at: {excel_output_path}")