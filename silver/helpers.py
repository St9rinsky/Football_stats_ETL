import os
import json
import glob
from pathlib import Path


def extract_latest_bronze_file(Season: int, Competition_name: str, folder_name: str):
    bronze_path = Path(f"data/bronze/{Competition_name}/{Season}")
    files = glob.glob(f"{bronze_path}/{folder_name}/*.json")

    if not files:
        raise FileNotFoundError(f"No bronze files found for dataset: {folder_name}")

    return max(files)

def read_json_file(file_path):
    with open(file_path, "r", encoding = "utf-8") as file:
        return json.load(file)