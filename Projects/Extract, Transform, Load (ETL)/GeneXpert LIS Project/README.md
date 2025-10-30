# GeneXpert LIS Project

**Overview:**  
This project implements a laboratory information system (LIS) for GeneXpert test management. It consolidates patient, medtech, and test record data from multiple Excel files into a structured MySQL database. Data is cleaned, standardized, and ready for reporting and analytics, with relationships maintained for integrity.  

**Tech Stack:**  
- **Python** – for ETL (Extract, Transform, Load) using `pandas` and `glob`.  
- **SQLAlchemy** – to connect and load data into MySQL.  
- **MySQL** – relational database with tables, constraints, and views.  
- **Excel** – source files and export format for analytics.  

**STAR Summary:**  

- **Situation:** Laboratory data was scattered across multiple unstandardized Excel files.  
- **Task:** Consolidate, clean, and store data in a structured, queryable system.  
- **Action:** Wrote Python ETL scripts, created MySQL tables and relationships, and built a SQL view for analytics.  
- **Result:** Clean, standardized dataset with traceable IDs, ready for reporting, analytics, and multi-lab integration.
