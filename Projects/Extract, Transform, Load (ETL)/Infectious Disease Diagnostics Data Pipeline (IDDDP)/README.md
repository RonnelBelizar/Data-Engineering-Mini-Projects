# 🧬 Infectious Disease ETL Pipeline

This project demonstrates a simple **ETL (Extract, Transform, Load)** process built in **Python** to handle **mock healthcare data** — including patient details, lab results, and device maintenance logs — and store them in a **PostgreSQL** database.

---

## 🧠 What This Project Does

- Extracts data from multiple local files (`.json`, `.csv`, `.xlsx`)
- Cleans and standardizes the data using **pandas**
- Loads the processed data into PostgreSQL tables using **SQLAlchemy**
- Generates logs to track each ETL stage

---

## 🛠️ Tech Stack

- **Python**
  - pandas  
  - SQLAlchemy  
  - psycopg2  
  - glob
- **PostgreSQL** (local database)

---

## 🗂️ Project Structure

infectious_disease_pipeline/  
├── etl_scripts/                         → Python: etl_pipeline_script.py and SQL: sql_script.sql
├── infectious_disease_pipeline_data/    → mock raw data files (.json, .csv, .xlsx)  
├── logs/                                → contains `etl_logs.txt`  
├── notebooks/                           → Jupyter notebooks for documentation and testing  
├── screenshots/                         → PostgreSQL table screenshots  
└── README.md                            → this file  

---

## ▶️ How It Works

1. **Extract** – Reads raw files from the local folder  
2. **Transform** – Cleans text fields, converts formats, removes duplicates  
3. **Load** – Inserts the cleaned data into PostgreSQL tables  

Logs are automatically recorded under `./logs/etl_logs.txt`.

---

## 💡 Summary

A straightforward ETL pipeline for cleaning and loading mock healthcare data.  
Built to demonstrate **data processing and database integration** skills using Python and SQL.

---

**Author:** Ronnel Belizar  
Biomedical Engineer | Aspiring Data Engineer
