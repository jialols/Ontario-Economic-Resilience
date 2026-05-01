import pandas as pd
import numpy as np

def clean_stats_can(file_path):
    """ Cleans the unique header/footer format of StatsCan CSVs."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    metric = lines[9].split(',')[2].replace('"', '').strip()
    df = pd.read_csv(file_path, skiprows=10)
    df = df.rename(columns={'Gender 6 7': 'Gender', 'Age group': 'AgeGroup'})
    
    # Pivot from Wide to Long format
    year_cols = [col for col in df.columns if col.isdigit()]
    df_melted = df.melt(id_vars=['Gender', 'AgeGroup'], value_vars=year_cols, 
                        var_name='Year', value_name='Value')
    
    df_melted['Metric'] = metric
    df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
    return df_melted.dropna(subset=['Value'])

# 1. Load Data
files = ["1410032701-eng.csv", "1410032701-eng (1).csv", "1410032701-eng (2).csv"]
raw_data = pd.concat([clean_stats_can(f) for f in files])

# 2. Build Model DataFrame
model_df = raw_data[raw_data['Gender'] == 'Total - Gender'].pivot_table(
    index=['AgeGroup', 'Year'], 
    columns='Metric', 
    values='Value'
).reset_index()

# Rename columns variable for easier coding
model_df.columns = ['AgeGroup', 'Year', 'Emp_Rate', 'Part_Rate', 'Unemp_Rate']

# 3. Calculate Resilience Index
# Formula: (Employment / Unemployment) * Participation
model_df['LSI'] = (model_df['Emp_Rate'] / (model_df['Unemp_Rate'] + 0.1)) * (model_df['Part_Rate'] / 100)

# Normalize 0-100
model_df['Resilience_Score'] = (model_df['LSI'] - model_df['LSI'].min()) / (model_df['LSI'].max() - model_df['LSI'].min()) * 100

# 4. Export Results
model_df.to_csv("economic_resilience_results.csv", index=False)
print("Model created successfully. Top resilient years in Ontario:")
print(model_df.sort_values(by='Resilience_Score', ascending=False).head(5))
