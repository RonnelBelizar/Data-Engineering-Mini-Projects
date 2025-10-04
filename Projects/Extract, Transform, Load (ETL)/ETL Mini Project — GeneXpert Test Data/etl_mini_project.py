import glob
import pandas as pd
from datetime import datetime
import os

etl_log = "etl_log.txt"
transformed_data_file = "clean_genexpert_data.csv"


def extract_xlsx(xlsx):
    extracted_xlsx = pd.read_excel(xlsx)
    file_name = os.path.splitext(os.path.basename(xlsx))[0]
    extracted_xlsx["Source_File"] = file_name
    logging(f"Extracted {file_name}.xlsx file")
    return extracted_xlsx


def extract_csv(csv):
    extracted_csv = pd.read_csv(csv)
    file_name = os.path.splitext(os.path.basename(csv))[0]
    extracted_csv["Source_File"] = file_name
    logging(f"Extracted {file_name}.csv file")
    return extracted_csv


def extract_json(json_file):
    extracted_json_file = pd.read_json(json_file)
    file_name = os.path.splitext(os.path.basename(json_file))[0]
    extracted_json_file["Source_File"] = file_name
    logging(f"Extracted {file_name}.json file")
    return extracted_json_file


def extract_and_combine_dataframes():

    look_xlsx = glob.glob(r"raw_data\*genexpert_data*.xlsx*")
    look_csv = glob.glob(r"raw_data\*genexpert_data*.csv*")
    look_json = glob.glob(r"raw_data\*genexpert_data*.json*")

    final_dfs = []
    for xlsx in look_xlsx:
        extracted_xlsx = extract_xlsx(xlsx)
        final_dfs.append(extracted_xlsx)
    for csv in look_csv:
        extracted_csv = extract_csv(csv)
        final_dfs.append(extracted_csv)
    for json_file in look_json:
        extracted_json = extract_json(json_file)
        final_dfs.append(extracted_json)

    combined_data = pd.concat(final_dfs, ignore_index=True)
    logging(f"Extracted XLSX/CSV/JSON files")
    return combined_data


def transform(combined_files):

    combined_files.columns = combined_files.columns.str.strip(
    ).str.lower().str.replace("_", " ")
    logging("Standardized Column Names")
    combined_files = combined_files.drop_duplicates(
        subset=["patient code", "test type", "result"])

    logging("Dropping duplicates based on 'patient code', 'test type', 'result'")
    combined_files["result"] = combined_files["result"].replace(
        [5007, 4017, 2008, "5007", "4017", "2008"], "Error")

    logging("Replaced error codes as 'Error'")
    combined_files["date tested"] = pd.to_datetime(
        combined_files["date tested"])

    logging("Coverted 'date tested' to datetime format")
    combined_files.sort_values(by="date tested", ascending=False, inplace=True)
    logging("Sorted data by date")
    return combined_files


def loading(transformed):

    transformed.to_csv(transformed_data_file, index=False)


def logging(message):

    timestamp_format = '[%Y-%m-%d %H:%M:%S]'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(etl_log, "a") as f:
        f.write(f"{timestamp} INFO: {message}\n")


# -------------------------------------------------

logging("ETL Started...")

logging("Data Extraction started")
extracted_data = extract_and_combine_dataframes()
logging("Data Extraction completed")

logging("Data Transformation started")
transformed_data = transform(extracted_data)
logging("Data Transformation completed")

logging("Saving Transformed Data")
loading(transformed_data)
logging("Saving Successful")

with open(etl_log, "r") as file:
    count_log_rows = len(file.readlines())

logging("Logging Completed...")
with open(etl_log, "a") as file:
    file.write(f"\nTotal Logs: {count_log_rows}\n")
