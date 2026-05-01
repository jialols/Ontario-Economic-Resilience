# Ontario Economic Resilience Model 🇨🇦
**A Data Pipeline & Predictive Indexing Project ˙ᵕ˙**

# Ontario-Economic-Resilience
An end-to-end pipeline to model Ontario economic resilience uses data from Statistics Canada

## ٩(ˊᗜˋ*)و ♡ 
## Project Overview
This project analyzes the long-term stability of the Ontario labour market using Statistics Canada datasets. It introduces the **Labour Stability Index (LSI)**, which is a custom metric designed to measure regional economic health by evaluating how employment levels and labour force participation interact during economic shocks.

By integrating **Python** for data engineering, **SQL** for relational modelling, and **Java** for logic processing, this repository demonstrates a full-stack approach to data analysis.

---

## ദ്ദി(｡•̀ ᗜ<) 
## The Model: Labour Stability Index (LSI)
Unlike simple unemployment metrics, the LSI evaluates the "anchoring" of a workforce. A resilient economy is one where participation remains high even when employment fluctuates.

Following this equation:

$$LSI = \left( \frac{\text{Employment Rate}}{\text{Unemployment Rate} + 0.1} \right) \times \frac{\text{Participation Rate}}{100}$$

*   **Employment Rate:** Measures current economic output.
*   **Participation Rate:** Measures labour force attachment and psychological "buy-in" to the economy.
*   **Unemployment Rate:** Measures immediate labour market stress.

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

---

## ദ്ദി ≧؂ ⠈≦)
## How to Run
1. **Python:** Run `python scripts/ontario_resilience_analysis.py` to generate the processed CSVs and plots.
2. **Java:** Compile and run `javac src/java/ResilienceCalculator.java && java ResilienceCalculator` to test specific data points.
3. **SQL:** Execute `sql/schema.sql` in your preferred RDBMS to initialize the data warehouse.

---
**Author:** Jia Naidu
**Field:** Honours Mathematics/Business Administration | University of Waterloo
