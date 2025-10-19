import pandas as pd
import glob
from datetime import datetime
from sqlalchemy import create_engine

raw_data_dir_ = "./infectious_disease_pipeline_data/"
patients_table = "patients"
lab_results_table = "lab_results"
maintenance_logs_table = "maintenance_logs"
etl_logs = "./logs/etl_logs.txt"


def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(etl_logs, "a") as file:
        file.write(f"{timestamp}: {message}\n")


def extract_patient_info():
    files = glob.glob(f"{raw_data_dir_}*.json")
    json_files = []
    for data in files:
        df = pd.read_json(data)
        json_files.append(df)
    df_total = pd.concat(json_files, ignore_index=True)
    return df_total


def extract_lab_results():
    files = glob.glob(f"{raw_data_dir_}*.csv")
    csv_files = []
    for data in files:
        df = pd.read_csv(data)
        csv_files.append(df)
    df_total = pd.concat(csv_files, ignore_index=True)
    return df_total


def extract_device_maintenance():
    files = glob.glob(f"{raw_data_dir_}*.xlsx")
    xlsx_files = []
    for data in files:
        df = pd.read_excel(data)
        xlsx_files.append(df)
    df_total = pd.concat(xlsx_files, ignore_index=True)
    return df_total


def transform_patient_info(df):

    df["patient_id"] = df["patient_id"].astype(str).str.strip().str.upper()
    df["name"] = df["name"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df['age'] = pd.to_numeric(df['age'], errors='coerce').astype('Int64')
    df["gender"] = df["gender"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df["city"] = df["city"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df["contact"] = pd.to_numeric(
        df["contact"], errors="coerce").astype("Int64")
    df.drop_duplicates(subset=['name', 'contact'], inplace=True)

    return df


def transform_lab_results(df):
    df["patient_id"] = df["patient_id"].astype(str).str.strip().str.upper()
    df["test_type"] = df["test_type"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df["result"] = df["result"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df["ct_value"] = pd.to_numeric(df['ct_value'], errors='coerce')
    df["test_date"] = pd.to_datetime(df["test_date"], errors='coerce')
    df.drop_duplicates(subset=["patient_id", "test_type",
                       "result", "ct_value", "test_date"], inplace=True)
    return df


def transform_device_maintenance(df):
    df["device_id"] = df["device_id"].astype(str).str.strip().str.upper()
    df["service_date"] = pd.to_datetime(df["service_date"])
    df["engineer"] = df["engineer"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df["status"] = df["status"].astype(str).str.strip().replace(
        r'[^A-Za-z\s]', '', regex=True).str.title()
    df.drop_duplicates(
        subset=["device_id", "service_date", "engineer", "status"], inplace=True)
    return df


def loading_patient_info(df_patients, df_lab_results, df_device_maintenance):
    df_patients.to_sql(patients_table, engine, if_exists="append", index=False)
    df_lab_results.to_sql(lab_results_table, engine,
                          if_exists="append", index=False)
    df_device_maintenance.to_sql(
        maintenance_logs_table, engine, if_exists="append", index=False)


# running ETL

log_progress('Starting ETL Process')

try:
    # Creating SQLAlchemy Engine
    log_progress('Establishing SQLAlchemy Engine')
    engine = create_engine(
        "postgresql+psycopg2://postgres:Madron_91@localhost:5432/infectious_disease_db"
    )
except Exception as e:
    print(f'Error Occured During Engine Creation: {e}')
    log_progress(f'Error Occured During Engine Creation: {e}')
else:
    log_progress('Successfully Created SQLAlchemy Engine')

# Extraction Process

log_progress('Initializing Extract Process')

try:
    log_progress('Extracting Patient Info')
    extract_patients = extract_patient_info()
    log_progress('Successfully Extracted Patient Info')

    log_progress('Extracting Lab Results')
    extract_lab = extract_lab_results()
    log_progress('Successfully Extracted Lab Results')

    log_progress('Extracting Device Maintenance')
    extract_maintenance = extract_device_maintenance()
    log_progress('Successfully Extracted Device Maintenance')
except Exception as e:
    print(f'Error Occured During Extraction: {e}')
    log_progress(f'Error Occured During Extraction: {e}')
else:
    log_progress('Successfully Extracted Data')

# Transformation Process

log_progress('Initializing Transformation')

try:
    log_progress('Transforming Patient Info')
    transform_patients = transform_patient_info(extract_patients)
    log_progress('Successfully Transformed Patient Info')

    log_progress('Transforming Lab Results')
    transform_lab = transform_lab_results(extract_lab)
    log_progress('Successfully Transformed Lab Results')

    log_progress('Transforming Device Maintenance')
    transform_maintenance = transform_device_maintenance(extract_maintenance)
    log_progress('Successfully Transformed Device Maintenance')
except Exception as e:
    print(f'Error Occured During Transformation: {e}')
    log_progress(f'Error Occured During Transformation: {e}')
else:
    log_progress('Successfully Transformed DataFrames')

# Loading DFs to PostgreSQL

log_progress('Loading DataFrames into PostgreSQL DB')

try:
    loading_patient_info(transform_patients, transform_lab,
                         transform_maintenance)
except Exception as e:
    print(f'Error Occured During Loading: {e}')
    log_progress(f'Error Occured During Loading: {e}')
else:
    log_progress('Successfully Loaded DataFrames')

# Closing SQLAlchemy Engine

engine.dispose()
log_progress('Closed SQLAlchemy Engine')
