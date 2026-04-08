## Python ETL Scripts

This folder contains Python-based ETL scripts responsible for loading raw source data into the data warehouse.

The staging ETL script cleans, standardizes, and deduplicates raw machine master data before loading it into a staging table. The fact ETL script processes daily testing records and loads them into the fact table using chunked upsert logic to support late-arriving updates.

These scripts are designed to be idempotent and safe to re-run.