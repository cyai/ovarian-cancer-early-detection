import os
import json
import pandas as pd
from datetime import datetime


def load_json_file(json_path):
    """Load a JSON file and return its data."""
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


def normalize_json(data, record_path=None):
    """
    Normalize a list of JSON records to a DataFrame.
    Use record_path if the JSON structure is nested.
    """
    return pd.json_normalize(data, record_path=record_path)


def preprocess_clinical(clinical_data):
    """Convert clinical data to a DataFrame and parse dates."""
    df = pd.json_normalize(clinical_data)
    # Convert string datetime columns to actual datetime objects (if present)
    for col in df.columns:
        if "datetime" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def preprocess_biospecimen(biospecimen_data):
    """Convert biospecimen data to a DataFrame and flatten nested structures."""
    df = pd.json_normalize(
        biospecimen_data,
        record_path=["samples"],
        meta=["case_id", "submitter_id", ["project", "project_id"]],
        meta_prefix="meta_",
        errors="ignore",
    )
    # Rename meta_case_id back to case_id
    df.rename(columns={"meta_case_id": "case_id"}, inplace=True)
    # You might also want to further expand nested lists (like 'portions') here.
    return df

def get_imaging_file_mapping(root_dir):
    """
    Walk the imaging directory and return a DataFrame with case-level file mapping.
    Assumes the folder structure is: <root_dir>/<case_id>/...
    """
    records = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(".png"):
                full_path = os.path.join(dirpath, file)
                # Assuming structure: converted/TCGA-OV/<case_id>/...
                parts = os.path.normpath(full_path).split(os.sep)
                # For example, if your folder tree is:
                # ["converted", "TCGA-OV", "TCGA-09-0364", ...]
                # then parts[2] is the case folder.
                if len(parts) >= 3:
                    case_id = parts[2]
                else:
                    case_id = None
                records.append({"case_id": case_id, "image_path": full_path})
    return pd.DataFrame(records)


def main():
    # File paths (adjust as needed)
    clinical_file = "clinical.project-tcga-ov.2025-03-06.json"
    biospecimen_file = "biospecimen.project-tcga-ov.2025-03-06.json"
    imaging_root = os.path.join("converted", "TCGA-OV")

    # Load JSON files
    clinical_data = load_json_file(clinical_file)
    biospecimen_data = load_json_file(biospecimen_file)

    # Preprocess clinical and biospecimen data
    clinical_df = preprocess_clinical(clinical_data)
    biospecimen_df = preprocess_biospecimen(biospecimen_data)

    # Get image file mapping from the converted directory
    imaging_df = get_imaging_file_mapping(imaging_root)

    # Merge clinical and biospecimen on "case_id" or "submitter_id" if available.
    # Here we merge on "case_id". Note that clinical_df and biospecimen_df may have different levels of granularity.
    integrated_df = pd.merge(
        clinical_df,
        biospecimen_df,
        on="case_id",
        how="outer",
        suffixes=("_clin", "_bio"),
    )
    integrated_df = pd.merge(integrated_df, imaging_df, on="case_id", how="outer")

    # Optional: Sort or drop duplicates if needed.
    integrated_df = integrated_df.sort_values(by="case_id")

    # Save integrated data to CSV
    output_csv = "integrated_data.csv"
    integrated_df.to_csv(output_csv, index=False)
    print(f"Integrated data saved to {output_csv}")


if __name__ == "__main__":
    main()
