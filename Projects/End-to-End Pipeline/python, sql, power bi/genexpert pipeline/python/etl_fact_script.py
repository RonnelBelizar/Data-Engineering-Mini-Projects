import os
import pandas as pd
from sqlalchemy import create_engine, text

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME")

fact_table = "fact_machine_daily_tests"

csv_file = "fact_machine_tests_2025.csv"
csv_path = f"./raw_data/{csv_file}"


UPSERT_SQL = text("""
INSERT INTO fact_machine_daily_tests (
    date_id,
    machine_id,
    facility_id,
    engineer_id,
    tests_mtb,
    tests_hiv,
    tests_ct_ng,
    tests_sars_cov,
    total_tests,
    theoretical_capacity,
    utilization_rate
)
VALUES (
    :date_id,
    :machine_id,
    :facility_id,
    :engineer_id,
    :tests_mtb,
    :tests_hiv,
    :tests_ct_ng,
    :tests_sars_cov,
    :total_tests,
    :theoretical_capacity,
    :utilization_rate
)
ON DUPLICATE KEY UPDATE
    engineer_id = VALUES(engineer_id),
    tests_mtb = VALUES(tests_mtb),
    tests_hiv = VALUES(tests_hiv),
    tests_ct_ng = VALUES(tests_ct_ng),
    tests_sars_cov = VALUES(tests_sars_cov),
    total_tests = VALUES(total_tests),
    theoretical_capacity = VALUES(theoretical_capacity),
    utilization_rate = VALUES(utilization_rate);
""")


def extract(csv_path):
    df = pd.read_csv(
        csv_path,
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
    # Dropping duplicates (Keeping the last because in our dataset, correction happens on the latest input)
    df = df.drop_duplicates(
        subset=['date_id', 'machine_id', 'facility_id'], keep='last')

    # Numeric conversions

    df = df.apply(pd.to_numeric, errors="raise")

    return df


def load(df, chunk_size=10_000):
    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}",
        future=True
    )

    total_rows = len(df)
    print(f"Loading {total_rows:,} fact rows...")

    with engine.begin() as conn:
        for start in range(0, total_rows, chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            records = chunk.to_dict(orient="records")

            conn.execute(UPSERT_SQL, records)
            print(f"Upserted rows {start:,} → {start + len(chunk):,}")

    print("Fact load completed.")

# ETL Process


extracted = extract(csv_path)
transformed = transform(extracted)
load(transformed)
