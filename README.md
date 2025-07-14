# Veridion Challenge #5 – PoC Simulation

## Problem Statement
A large manufacturing company's supplier database is outdated and messy. The goal is to clean and resolve this supplier data using Veridion's company match candidates, and prepare it for downstream analysis like spend tracking and sustainability scoring.

## What I Did

### Entity Resolution
Used Python and pandas along with the `rapidfuzz` library to:
- Group supplier entries by `input_row_key`
- Compute fuzzy match scores between `input_company_name` and candidate `company_name` using `fuzz.token_sort_ratio`
- Select the best candidate if the fuzzy match score was >= 85
- Leave unmatched entries blank (if no candidate passed threshold)
- Record the fuzzy score as a reason for transparency
- Exported results to `/output/resolved_matches.csv`

### Data Quality Control
Created `/output/qc_flags.csv` by:
- Merging resolved matches with full company metadata
- Flagging issues such as:
  -  Missing or 0 revenue
  -  Missing or 0 employees
  -  Missing website
  -  Missing business sector
  -  Implausibly large employee counts (> 100,000)
- These QC insights simulate what a presales team would provide to help a client trust the data output.

## Folder Structure

veridion_challenge/
    data/
        presales_data_sample.csv
    output/
        resolved_matches.csv
        qc_flags.csv
    scripts/
        entity_resolution.py
        qc_flags.py
    README.md

## Summary Results

- Total supplier queries processed: 592
- Confident matches found: 174 (fuzzy score ≥ 85)
- Entries flagged in QC: 590
- Most common data issues:
  - `revenue` missing or 0
  - `employee_count` missing or 0
  - `website_domain` missing
  - `main_sector` missing

## Tools Used

- Python 3.13
- pandas
- rapidfuzz
- pathlib

## Final Thoughts

This simulation reflects how I would approach a real-world Proof of Concept (PoC):

- Prioritized precision over blind matching to avoid false positives
- Delivered matches that are explainable, auditable, and easy to validate
- Flagged key data health issues so the client knows what’s missing and why it matters

If this were a live project, recommended next steps would include:
- Enriching metadata using website domains or email for better confidence scoring
- Normalizing multilingual or region-specific company names
- Creating visual QC dashboards in Power BI or Streamlit to assist client review

