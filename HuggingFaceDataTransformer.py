import pandas as pd
import json
import os

# Load JSON
with open("final.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # Load as a dictionary

master_dir = 'HuggingFace'

# Ensure the output directory exists
os.makedirs(master_dir, exist_ok=True)

# Convert each section to a separate Parquet file
for section in data:
    # Replace spaces with underscores for file compatibility
    safe_section_name = section.replace(" ", "_").lower().strip()

    # Convert to DataFrame
    df = pd.DataFrame(data[section])

    # Ensure the output directory exists
    os.makedirs(f"{master_dir}/{safe_section_name}", exist_ok=True)

    # Save to Parquet
    df.to_parquet(f"{master_dir}/{safe_section_name}/test-00000-to-00001.parquet", engine="pyarrow")

    print(f"Saved {master_dir}/{safe_section_name}/test-00000-to-00001.parquet")
