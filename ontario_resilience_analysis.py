import pandas as pd
import os

def process_ontario_data(raw_folder="data/raw", output_folder="data/processed"):
    """
    ETL Pipeline: Cleans StatsCan CSVs and calculates the Resilience Index.
    """
    all_data = []
    
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 1. Extraction: Load and clean metadata from each file
    print("Reading raw files...")
    for filename in os.listdir(raw_folder):
        if filename.endswith(".csv"):
            path = os.path.join(raw_folder, filename)
            # Encoding utf-8-sig handles the byte order mark often found in StatsCan files
            with open(path, "r", encoding="utf-8-sig") as f:
                lines = f.readlines()
            
            # Detect Metric Name (e.g., Employment rate) from the header
            metric = lines[9].split(",")[2].replace('"', '').strip()
            
            # Load data skipping the metadata header
            df = pd.read_csv(path, skiprows=10)
            df = df.rename(columns={"Gender 6 7": "Gender", "Age group": "AgeGroup"})
            
            # Melt Wide format (years as columns) to Long format (Year column)
            year_cols = [col for col in df.columns if col.isdigit()]
            df_long = df.melt(id_vars=["Gender", "AgeGroup"], value_vars=year_cols, 
                              var_name="Year", value_name="Value")
            df_long["Metric"] = metric
            all_data.append(df_long)

    # 2. Transformation: Combine and Pivot
    print("Combining and pivoting metrics...")
    combined = pd.concat(all_data)
    combined["Value"] = pd.to_numeric(combined["Value"], errors="coerce")
    combined = combined.dropna(subset=["Value"])

    # Filter for Total Gender and Pivot metrics into separate columns
    final_df = combined[combined["Gender"] == "Total - Gender"].pivot_table(
        index=["AgeGroup", "Year"], 
        columns="Metric", 
        values="Value"
    ).reset_index()

    # Rename columns for clarity
    final_df.columns = ["AgeGroup", "Year", "Employment_Rate", "Participation_Rate", "Unemployment_Rate"]
    final_df["Year"] = final_df["Year"].astype(int)

    # 3. Feature Engineering: Resilience Calculation
    print("Calculating Labor Stability Index (LSI)...")
    # Formula: (Emp / (Unemp + 0.1)) * (Part / 100)
    final_df["LSI"] = (final_df["Employment_Rate"] / (final_df["Unemployment_Rate"] + 0.1)) * (final_df["Participation_Rate"] / 100)

    # Min-Max Normalization (0 to 100)
    lsi_min = final_df["LSI"].min()
    lsi_max = final_df["LSI"].max()
    final_df["Resilience_Score"] = ((final_df["LSI"] - lsi_min) / (lsi_max - lsi_min)) * 100

    # 4. Loading: Save the Processed Data
    output_path = os.path.join(output_folder, "ontario_resilience_summary.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Success! Processed data saved to: {output_path}")

if __name__ == "__main__":
    process_ontario_data()
