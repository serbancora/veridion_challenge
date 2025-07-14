import pandas as pd
from pathlib import Path
from rapidfuzz import fuzz

# Load data
df = pd.read_csv("../data/presales_data_sample.csv")
grouped = df.groupby("input_row_key")

# Match logic
def pick_best_match(group):
    input_name = group['input_company_name'].iloc[0].lower()
    best_score = 0
    best_row = None

    for _, row in group.iterrows():
        candidate_name = row['company_name'].lower()
        score = fuzz.token_sort_ratio(input_name, candidate_name)
        if score > best_score:
            best_score = score
            best_row = row

    if best_score >= 85:  # Score threshold for confident match
        return best_row['veridion_id'], f"fuzzy match score: {round(best_score, 2)}"
    return None, "no confident match"

results = []

for row_key, group in grouped:
    match_id, reason = pick_best_match(group)
    results.append({
        "input_row_key": row_key,
        "selected_veridion_id": match_id,
        "match_reason": reason
    })

# Convert results to DataFrame and save to CSV
output_df = pd.DataFrame(results)
output_path = Path("../output/resolved_matches.csv")
output_df.to_csv(output_path, index=False) 

print("Matching complete. Output saved to:", output_path)
