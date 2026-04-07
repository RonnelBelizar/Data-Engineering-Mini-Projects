import pandas as pd
from sqlalchemy import create_engine
import os

csv_file = "master_data.csv"
csv_path = f"./raw_data/{csv_file}"

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME")

staging_table = "staging_master_data"


def extract(csv_path):
    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="latin1",
        na_values=["", "NULL", "null", "NaN",
                   "nan", "None", "No Record", "<NA>"]
    )
    return df


def transform(df):

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Dropping duplicates
    df = df.drop_duplicates(subset=['serial_number'], keep='first')

    # Date conversions
    date_cols = [
        "first_installation_date",
        "warranty_end_date",
        "last_maintenance_visit_date",
        "last_xpertcheck_date",
        "adf_generation_date",
        "last_database_update"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    # Numeric conversions
    df["serial_number"] = pd.to_numeric(df["serial_number"], errors="raise")
    df["no_of_modules"] = pd.to_numeric(df["no_of_modules"], errors="coerce")
    df["utilization_rate"] = pd.to_numeric(
        df["utilization_rate"], errors="coerce")
    df["total_tests"] = pd.to_numeric(df["total_tests"], errors="coerce")

    # Fix float artifacts on string fields
    float_artifact_cols = [
        "last_maintenance_sr_no",
        "last_xpertcheck_sr_no",
        "contact_number"
    ]

    for col in float_artifact_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"\.0$", "", regex=True)
                .replace("nan", None)
            )

    # Final cleanup: empty strings → NULL
    df = df.replace(r"^\s*$", None, regex=True)

    return df


def load(df):
    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}",
        future=True
    )
    df.to_sql(
        name=f"{staging_table}",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi"
    )

# ETL Process


extracted = extract(csv_path)
transformed = transform(extracted)
load(transformed)
