import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def get_latest_bronze_file(dataset_name):
    bronze_path = Path("data/bronze/football_api")

    files = list(bronze_path.rglob(f"{dataset_name}/*.json"))

    if not files:
        raise FileNotFoundError(f"No bronze files found for dataset: {dataset_name}")

    return max(files, key=lambda file: file.stat().st_mtime)


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# keep your insert_result() exactly a


def load_results_to_silver(file_path):
    data = load_json_file(file_path)

    if "matches" not in data:
        raise ValueError("This is not a results file. Expected key 'matches'.")

    print("Loading file:", file_path)
    print("Number of matches:", len(data["matches"]))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        for match in data["matches"]:
            insert_result(cursor, match)

        connection.commit()
        print(f"Loaded {len(data['matches'])} matches into silver.results")

    except Exception as error:
        connection.rollback()
        print("Failed to load results:", error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    latest_file = get_latest_bronze_file("results")
    load_results_to_silver(latest_file)