import argparse
import os
from typing import List

import pandas as pd


def process_ontario_data(raw_folder: str = "data/raw",
                         output_folder: str = "data/processed",
                         output_filename: str = "ontario_resilience_summary.csv") -> str:
    """
    ETL Pipeline: Cleans Statistics Canada LFS CSVs and calculates the Labour Stability Index (LSI)
    and a normalized Resilience Score.

    Steps:
        1. Extract: Read all CSVs in `raw_folder`, handle StatsCan metadata, and standardize columns.
        2. Transform: Reshape to long format, pivot metrics, compute LSI and Resilience Score.
        3. Load: Save a clean, analysis-ready CSV to `output_folder`.

    Parameters
    ----------
    raw_folder : str
        Directory containing raw StatsCan CSV files.
    output_folder : str
        Directory where the processed CSV will be written.
    output_filename : str
        Name of the output CSV file.

    Returns
    -------
    str
        Full path to the processed CSV file.
    """
    if not os.path.isdir(raw_folder):
        raise FileNotFoundError(f"Raw data folder not found: {raw_folder}")

    os.makedirs(output_folder, exist_ok=True)

    all_data: List[pd.DataFrame] = []

    print(f"[INFO] Reading raw files from: {raw_folder}")
    for filename in os.listdir(raw_folder):
        if not filename.lower().endswith(".csv"):
            continue

        path = os.path.join(raw_folder, filename)
        print(f"[INFO] Processing file: {path}")

        # Read all lines to inspect metadata/header
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        if len(lines) < 11:
            print(f"[WARN] Skipping {filename}: not enough lines to contain metadata + data.")
            continue

        # Example: metric name is often in a metadata line (e.g., line 10, index 9)
        # Adjust this if your StatsCan format differs.
        try:
            metric = lines[9].split(",")[2].replace('"', "").strip()
        except IndexError:
            print(f"[WARN] Could not parse metric from metadata in {filename}. Skipping.")
            continue

        # Load data skipping metadata header (first 10 lines)
        df = pd.read_csv(path, skiprows=10)

        # Standardize column names (adjust to match your actual StatsCan headers)
        rename_map = {
            "Gender 6 7": "Gender",
            "Age group": "AgeGroup",
        }
        df = df.rename(columns=rename_map)

        if "Gender" not in df.columns or "AgeGroup" not in df.columns:
            print(f"[WARN] Required columns missing in {filename}. Skipping.")
            continue

        # Identify year columns (StatsCan often uses year as column names)
        year_cols = [col for col in df.columns if str(col).isdigit()]
        if not year_cols:
            print(f"[WARN] No year columns detected in {filename}. Skipping.")
            continue

        # Melt wide format (years as columns) into long format (Year, Value)
        df_long = df.melt(
            id_vars=["Gender", "AgeGroup"],
            value_vars=year_cols,
            var_name="Year",
            value_name="Value",
        )
        df_long["Metric"] = metric
        all_data.append(df_long)

    if not all_data:
        raise RuntimeError("No valid data frames were created from raw CSVs.")

    print("[INFO] Combining and pivoting metrics...")
    combined = pd.concat(all_data, ignore_index=True)

    # Convert Value to numeric and drop non-numeric entries
    combined["Value"] = pd.to_numeric(combined["Value"], errors="coerce")
    combined = combined.dropna(subset=["Value"])

    # Filter for total gender (adjust string to match your actual data)
    mask_total_gender = combined["Gender"].str.contains("Total", case=False, na=False)
    combined = combined[mask_total_gender]

    # Pivot metrics into separate columns
    pivot_df = combined.pivot_table(
        index=["AgeGroup", "Year"],
        columns="Metric",
        values="Value",
        aggfunc="mean",  # in case of duplicates
    ).reset_index()

    # Rename columns for clarity; adjust keys to match actual metric names in your files
    # Example mapping: {"Employment rate": "Employment_Rate", ...}
    rename_metrics = {
        "Employment rate": "Employment_Rate",
        "Participation rate": "Participation_Rate",
        "Unemployment rate": "Unemployment_Rate",
    }
    pivot_df = pivot_df.rename(columns=rename_metrics)

    required_cols = {"Employment_Rate", "Participation_Rate", "Unemployment_Rate"}
    missing = required_cols - set(pivot_df.columns)
    if missing:
        raise RuntimeError(f"Missing required metric columns after pivot: {missing}")

    pivot_df["Year"] = pivot_df["Year"].astype(int)

    print("[INFO] Calculating Labour Stability Index (LSI)...")
    # LSI formula: (Emp / (Unemp + 0.1)) * (Part / 100)
    epsilon = 0.1
    pivot_df["LSI"] = (
        pivot_df["Employment_Rate"] /
        (pivot_df["Unemployment_Rate"] + epsilon)
    ) * (pivot_df["Participation_Rate"] / 100.0)

    print("[INFO] Normalizing LSI to Resilience Score (0–100)...")
    lsi_min = pivot_df["LSI"].min()
    lsi_max = pivot_df["LSI"].max()
    if lsi_max == lsi_min:
        # Avoid division by zero; if all values are equal, set score to 50
        pivot_df["Resilience_Score"] = 50.0
    else:
        pivot_df["Resilience_Score"] = (
            (pivot_df["LSI"] - lsi_min) / (lsi_max - lsi_min)
        ) * 100.0

    # Reorder columns for readability
    final_df = pivot_df[
        ["AgeGroup", "Year",
         "Employment_Rate", "Participation_Rate", "Unemployment_Rate",
         "LSI", "Resilience_Score"]
    ].sort_values(["AgeGroup", "Year"])

    output_path = os.path.join(output_folder, output_filename)
    final_df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Processed data saved to: {output_path}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ontario Economic Resilience ETL Pipeline"
    )
    parser.add_argument(
        "--raw_dir",
        default="data/raw",
        help="Directory containing raw StatsCan CSV files (default: data/raw)",
    )
    parser.add_argument(
        "--output_dir",
        default="data/processed",
        help="Directory to write processed CSV files (default: data/processed)",
    )
    parser.add_argument(
        "--output_filename",
        default="ontario_resilience_summary.csv",
        help="Name of the processed output CSV file (default: ontario_resilience_summary.csv)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_ontario_data(
        raw_folder=args.raw_dir,
        output_folder=args.output_dir,
        output_filename=args.output_filename,
    )
if __name__ == "__main__":
    process_ontario_data()
