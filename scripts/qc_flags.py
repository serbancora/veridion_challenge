import pandas as pd
from pathlib import Path

# Load files
resolved = pd.read_csv("../output/resolved_matches.csv")
raw = pd.read_csv("../data/presales_data_sample.csv")

# Join resolved data with full company info
merged = resolved.merge(raw, on="input_row_key", how="left")

# Only keep rows with a selected match
matched = merged[merged["selected_veridion_id"].notnull()].copy()

# Initialize QC flag column
def flag_qc_issues(row):
    issues = []
    if pd.isna(row['website_domain']):
        issues.append("missing website")
    if pd.isna(row['revenue']) or row['revenue'] == 0:
        issues.append("missing or 0 revenue")
    if pd.isna(row['employee_count']) or row['employee_count'] == 0:
        issues.append("missing or 0 employees")
    if pd.isna(row['main_sector']):
        issues.append("missing sector")
    if row['employee_count'] and row['employee_count'] > 100000:
        issues.append("implausibly high employee count")
    if pd.isna(row['primary_email']) and pd.isna(row['primary_phone']):
        issues.append("no contact info")
    if pd.isna(row['main_latitude']) or pd.isna(row['main_longitude']):
        issues.append("missing geolocation")
    return "; ".join(issues) if issues else None

matched["qc_flags"] = matched.apply(flag_qc_issues, axis=1)

# Filter only flagged rows
flagged = matched[matched["qc_flags"].notnull()][[
    "input_row_key", "selected_veridion_id", "company_name", 
    "website_domain", "revenue", "employee_count", "main_sector", "qc_flags"
]]

# Save to CSV
qc_path = Path("../output/qc_flags.csv")
flagged.to_csv(qc_path, index=False)

print(f"QC check complete. Found {len(flagged)} flagged entries.")
print("Output saved to:", qc_path)
