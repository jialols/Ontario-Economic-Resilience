# Ontario Economic Resilience Model 🇨🇦
**A Data Pipeline & Predictive Labour Stability Index Project˙ᵕ˙**

## ٩(ˊᗜˋ*)و ♡ 
## Project Overview
This project models the long‑term stability of Ontario’s labour market using Statistics Canada Labour Force Survey (LFS) datasets. It introduces a custom **Labour Stability Index (LSI)** to quantify regional economic resilience by capturing how employment, unemployment, and labour force participation interact during economic shocks.

---

## ദ്ദി(｡•̀ ᗜ<) 
## The Model: Labour Stability Index (LSI)
Unlike simple unemployment metrics, the LSI evaluates the "anchoring" of a workforce. A resilient economy is one where participation remains high even when employment fluctuates.

Following this equation:

$$LSI = \left( \frac{\text{Employment Rate}}{\text{Unemployment Rate} + 0.1} \right) \times \frac{\text{Participation Rate}}{100}$$

- **Employment Rate:** Proxy for current economic output.  
- **Participation Rate:** Captures attachment and “buy‑in” to the labour market.  
- **Unemployment Rate:** Captures immediate labour market stress.  

The raw LSI is then min–max scaled to a **Resilience Score (0–100)** for easier comparison across years and age groups.

---

## (˶• ᴗ •˵) 
## Tech Stack & Architecture
- **Data Engineering:** `Python` (Pandas, NumPy) for cleaning messy Statistics Canada CSV formats.
- **Relational Modelling:** `SQL` (PostgreSQL) for structured storage and complex trend querying.
- **Business Logic:** `Java` for a strictly-typed, high-performance calculation engine.
- **Visualization:** `Matplotlib` & `Seaborn` for time-series trend analysis.

---

## (ง ˃ ᗜ ˂)ว  .ˊˎ-
## Repository Structure
*   `ontario_resilience_analysis.py`: Main Python pipeline for data ingestion, cleaning, and normalization.
*   `ResilienceCalculator.java`: Java-based engine for core index calculations.
*   `schema.sql`: Database schema and analytical queries for warehouse modelling.
*   `data/raw/`: Original Statistics Canada LFS datasets.
*   `data/processed/`: Normalized datasets used for final modelling.
*   `resilience_trend_chart.png`: Visual output of Ontario’s economic health from 1976–2025.

---

## ¡¡¡( •̀ ᴗ •́ )و!!!
## Key Findings (Ontario 1976–2025)
*   **Historical Peak:** Ontario reached maximum resilience in the late 1980s due to record-high participation and low relative unemployment.
*   **The 2020 Shock:** The Resilience Score dropped to a historical low of **1.77**, indicating a total breakdown in labour market stability during the pandemic.
*   **Current Outlook:** As of 2025, the index sits at **25.3**, suggesting that while employment remains moderate, the labour market is currently more "fragile" than it was during the 2022-2023 recovery peak.
<img width="806" height="500" alt="image" src="https://github.com/user-attachments/assets/4348e3a9-3a85-4f98-9637-f0d24aa179f7" />


---

## ദ്ദി ≧؂ ⠈≦)
## How to Run
1. **Python:** Run `python scripts/ontario_resilience_analysis.py` to generate the processed CSVs and plots.
2. **Java:** Compile and run `javac src/java/ResilienceCalculator.java && java ResilienceCalculator` to test specific data points.
3. **SQL:** Execute `sql/schema.sql` in your preferred RDBMS to initialize the data warehouse.

---
**Author:** Jia Naidu
**Field:** Honours Mathematics/Business Administration | University of Waterloo
