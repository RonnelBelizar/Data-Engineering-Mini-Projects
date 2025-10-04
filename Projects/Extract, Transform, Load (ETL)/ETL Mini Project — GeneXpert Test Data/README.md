# ETL Mini Project: GeneXpert Data Pipeline

## Project Overview
This project simulates a real-world ETL (Extract, Transform, Load) process for GeneXpert machine test data. It extracts data from multiple file types, cleans and transforms it, and saves a final cleaned dataset.

## Features
- **Extract** data from CSV, XLSX, and JSON files.  
- **Transform** data by:
  - Standardizing column names  
  - Dropping duplicate rows  
  - Replacing error codes `[5007, 4017, 2008]` with `"Error"`  
  - Converting date columns to datetime format  
  - Sorting data by test date  
- **Load** cleaned data into a CSV file.  
- **Logging** all ETL steps with timestamps.

## File Structure

ETL Mini Project — GeneXpert Test Data/
├── raw_data/ # Folder containing raw CSV/XLSX/JSON files
├── clean_genexpert_data.csv # Final cleaned dataset
├── etl_log.txt # ETL process log
├── healthcare_etl.ipynb # Jupyter Notebook
└── healthcare_etl.py # Main ETL script

## How to Run
1. Place raw CSV, XLSX, or JSON files in the `raw_data` folder.  
2. Run the ETL script:
```bash
python etl_mini_project.py
```
3. Check clean_genexpert_data.csv for the cleaned data.
4. Check etl_log.txt for the ETL process log.

## Notes

- Duplicate rows are removed based on "patient code", "test type", and "result".
- Error codes are replaced with "Error" to standardize invalid results.
- This project demonstrates a beginner-friendly simulation of a healthcare ETL workflow.