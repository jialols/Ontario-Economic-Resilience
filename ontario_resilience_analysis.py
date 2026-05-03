import argparse
import os
from typing import List

import numpy as np
import pandas as pd


def process_ontario_data(raw_folder: str = "data/raw",
                         output_folder: str = "data/processed",
                         output_filename: str = "ontario_resilience_summary.csv") -> str:
    """
    ETL Pipeline for Ontario Labour Force Survey (LFS) data.

    Enhancements:
    - Uses NumPy for clipping, vectorized math, and missing-value handling.
    - More robust metric detection.
    - Faster pivoting and dtype optimization.
    - Cleaner logging and error handling.
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

        # Read metadata lines
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        if len(lines) < 11:
            print(f"[WARN] Skipping {filename}: insufficient metadata.")
            continue

        # Extract metric name from StatsCan metadata
        try:
            metric = lines[9].split(",")[2].replace('"', "").strip()
        except Exception:
            print(f"[WARN] Could not parse metric from {filename}. Skipping.")
            continue

        # Load data (skip metadata header)
        df = pd.read_csv(path, skiprows=10)

        # Standardize column names
        df = df.rename(columns={
            "Gender 6 7": "Gender",
            "Age group": "AgeGroup"
        })

        if "Gender" not in df.columns or "AgeGroup" not in df.columns:
            print(f"[WARN] Missing required columns in {filename}. Skipping.")
            continue

        # Identify year columns
        year_cols = [col for col in df.columns if str(col).isdigit()]
        if not year_cols:
            print(f"[WARN] No year columns found in {filename}. Skipping.")
            continue

        # Melt wide → long
        df_long = df.melt(
            id_vars=["Gender", "AgeGroup"],
            value_vars=year_cols,
            var_name="Year",
            value_name="Value"
        )
        df_long["Metric"] = metric
        all_data.append(df_long)

    if not all_data:
        raise RuntimeError("No valid CSVs found in raw data folder.")

    print("[INFO] Combining datasets...")
    combined = pd.concat(all_data, ignore_index=True)

    # Convert to numeric using NumPy for speed
    combined["Value"] = pd.to_numeric(combined["Value"], errors="coerce")
    combined = combined.dropna(subset=["Value"])

    # Filter for total gender
    combined = combined[combined["Gender"].str.contains("Total", case=False, na=False)]

    print("[INFO] Pivoting metrics...")
    pivot_df = combined.pivot_table(
        index=["AgeGroup", "Year"],
        columns="Metric",
        values="Value",
        aggfunc="mean"
    ).reset_index()

    # Rename metrics (adjust to your actual StatsCan labels)
    pivot_df = pivot_df.rename(columns={
        "Employment rate": "Employment_Rate",
        "Participation rate": "Participation_Rate",
        "Unemployment rate": "Unemployment_Rate"
    })

    required = {"Employment_Rate", "Participation_Rate", "Unemployment_Rate"}
    missing = required - set(pivot_df.columns)
    if missing:
        raise RuntimeError(f"Missing required metrics: {missing}")

    pivot_df["Year"] = pivot_df["Year"].astype(int)

    print("[INFO] Calculating LSI using NumPy...")
    emp = pivot_df["Employment_Rate"].to_numpy()
    unemp = pivot_df["Unemployment_Rate"].to_numpy()
    part = pivot_df["Participation_Rate"].to_numpy()

    # Avoid division by zero using NumPy
    epsilon = 0.1
    lsi = (emp / (unemp + epsilon)) * (part / 100.0)

    # Clip negative or extreme values (robustness)
    lsi = np.clip(lsi, 0, None)

    pivot_df["LSI"] = lsi

    print("[INFO] Normalizing LSI to 0–100 scale...")
    lsi_min, lsi_max = np.nanmin(lsi), np.nanmax(lsi)

    if lsi_max == lsi_min:
        pivot_df["Resilience_Score"] = 50.0
    else:
        pivot_df["Resilience_Score"] = ((lsi - lsi_min) / (lsi_max - lsi_min)) * 100

    # Final ordering
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
    parser = argparse.ArgumentParser(description="Ontario Economic Resilience ETL Pipeline")
    parser.add_argument("--raw_dir", default="data/raw")
    parser.add_argument("--output_dir", default="data/processed")
    parser.add_argument("--output_filename", default="ontario_resilience_summary.csv")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_ontario_data(
        raw_folder=args.raw_dir,
        output_folder=args.output_dir,
        output_filename=args.output_filename
    )
