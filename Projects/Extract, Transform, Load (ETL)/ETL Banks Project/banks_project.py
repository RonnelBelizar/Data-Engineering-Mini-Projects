import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
from io import StringIO
import sqlite3

url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
header = {"User-Agent": "Mozilla/5.0"}

attributes = ["Name", "MC_USD_Billion"]
table_attributes = ["Name", "MC_USD_Billion",
                    "MC_GBP_Billion", "MC_EUR_Billion", "MC_INR_Billion"]

output_csv_path = "Largest_banks_data.csv"
database_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt"


def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as file:
        file.write(f"{timestamp}: {message}\n")


def extract(url):
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = str(soup.find_all("table", class_="wikitable"))
    dfs = pd.read_html(StringIO(tables))
    df = dfs[0]
    return df


def transform(df, csv_path):
    rates = pd.read_csv(csv_path, index_col="Currency")
    df = df.rename(columns={
        "Bank name": "Name", "Total assets (2025) (US$ billion)": "MC_USD_Billion"})
    for currency, rate in rates["Rate"].items():
        df[f"MC_{currency}_Billion"] = np.round(df["MC_USD_Billion"]*rate, 2)
    df = df[table_attributes]
    return df


def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)


def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)


def run_queries(query_statement, sql_connection):
    log_progress("Running Query")
    print(pd.read_sql(query_statement, sql_connection))
    log_progress("Querying Successful")

# Running ETL


log_progress("Preliminaries complete. Initiating ETL process")


try:
    extracted = extract(url)
    log_progress("Data extraction complete. Initiating Transformation process")

    transformed = transform(extracted, "exchange_rate.csv")
    log_progress("Data transformation complete. Initiating Loading process")

    load_to_csv(transformed, output_csv_path)
    log_progress("Data saved to CSV file")

    sql_conn = sqlite3.connect(database_name)
    log_progress("SQL Connection initiated")

    load_to_db(transformed, sql_conn, table_name)
    log_progress("Data loaded to Database as a table, Executing queries")

except Exception as e:
    log_progress(f"Error Found: {e}")
    print(f"Error found during ETL Process: {e}")

else:
    run_queries("SELECT * FROM Largest_banks", sql_conn)
    run_queries(
        "SELECT AVG(MC_GBP_Billion) FROM Largest_banks", sql_conn)
    run_queries("SELECT Name from Largest_banks LIMIT 5", sql_conn)

    log_progress("Process Complete")

finally:
    sql_conn.close()
    log_progress("Server Connection closed")
