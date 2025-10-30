import pandas as pd
import glob
from sqlalchemy import create_engine


def extract_patients():
    patients_dir = glob.glob("./raw_files/*patients*.xlsx")
    if not patients_dir:
        raise FileNotFoundError("No patient.xlsx file found")
    patients = []
    for data in patients_dir:
        df = pd.read_excel(data)
        patients.append(df)
    df_total = pd.concat(patients, ignore_index=True)
    return df_total


def extract_medtechs():
    medtechs_dir = glob.glob("./raw_files/*medtechs*.xlsx")
    if not medtechs_dir:
        raise FileNotFoundError("No medtechs.xlsx file found")
    medtechs = []
    for data in medtechs_dir:
        df = pd.read_excel(data)
        medtechs.append(df)
    df_total = pd.concat(medtechs, ignore_index=True)
    return df_total


def extract_test_records():
    test_records_dir = glob.glob("./raw_files/*test_records*.xlsx")
    if not test_records_dir:
        raise FileNotFoundError("No test_records.xlsx file found")
    test_records = []
    for data in test_records_dir:
        df = pd.read_excel(data)
        test_records.append(df)
    df_total = pd.concat(test_records, ignore_index=True)
    return df_total


def transform_patients(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["patient_id", "first_name", "last_name"])
    df["first_name"] = df["first_name"].astype(str).str.strip().str.title()
    df["last_name"] = df["last_name"].astype(str).str.strip().str.title()
    df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
    df["gender"] = df["gender"].astype(str).str.strip().str.upper()
    df["contact_number"] = df["contact_number"].astype(
        str).str.replace(r"\.0$", "", regex=True).str.strip()
    return df


def transform_medtechs(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["medtech_id", "first_name", "last_name"])
    df["first_name"] = df["first_name"].astype(str).str.strip().str.title()
    df["last_name"] = df["last_name"].astype(str).str.strip().str.title()
    df["license_number"] = df["license_number"].astype(str).str.strip()
    return df


def transform_test_records(df):
    df = df.copy()
    df = df.drop_duplicates(
        subset=["test_id", "test_date", "test_type", "status"])
    df["test_date"] = pd.to_datetime(df["test_date"], errors="coerce")
    df["sample_type"] = df["sample_type"].astype(str).str.strip().str.title()
    df["test_type"] = df["test_type"].astype(str).str.strip().str.upper()
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df["result"] = df["result"].astype(str).str.strip().str.title()
    df["time_completed"] = pd.to_datetime(
        df["time_completed"], errors="coerce")
    return df


def load_patients(df, engine):
    df.to_sql("patients", engine, if_exists="append", index=False)


def load_medtechs(df, engine):
    df.to_sql("medtechs", engine, if_exists="append", index=False)


def load_test_records(df, engine):
    df.to_sql("test_records", engine, if_exists="append", index=False)


# ETL

# Load Engine

engine = create_engine(
    "mysql+pymysql://Ronnel:1234@localhost:3306/genexpert_lis")

# Extraction
patients_df = extract_patients()
medtechs_df = extract_medtechs()
test_records_df = extract_test_records()

# Transformation
transformed_patients = transform_patients(patients_df)
transformed_medtechs = transform_medtechs(medtechs_df)
transformed_test_records = transform_test_records(test_records_df)

# Loading
load_patients(transformed_patients, engine)
load_medtechs(transformed_medtechs, engine)
load_test_records(transformed_test_records, engine)

# Engine Closing
connection = engine.connect()
connection.close()
