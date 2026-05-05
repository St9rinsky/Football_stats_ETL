import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

COMPETITION_CODE = "PL"
COMPETITION_NAME = "premier_league"
SEASON = 2025

def save_json_to_bronze(data, dataset_name, competition_name, season):
    now = datetime.now()
    year = now.year
    week = now.isocalendar().week
    date = now.strftime("%Y-%m-%d")

    folder_path = (
        f"data/bronze/football_api/"
        f"competition={competition_name}/"
        f"season={season}/"
        f"year={year}/"
        f"week={week}/"
        f"{dataset_name}"
    )
    
    file_name = (
        f"{competition_name}_{dataset_name}_"
        f"{season}_season_week_{week}_{date}.json"
    )

    file_path = f"{folder_path}/{file_name}"

    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved bronze file: {file_path}\n")



def fetch_from_api(endpoint, params=None):
    headers = {
        "X-Auth-Token": API_KEY
    }

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, headers=headers, params=params)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    response.raise_for_status()
    return response.json()


def extract_results():
    data = fetch_from_api(
        endpoint=f"competitions/{COMPETITION_CODE}/matches",
        params={
            "season": SEASON
        }
    )

    save_json_to_bronze(data, "results", COMPETITION_NAME, SEASON)


def extract_standings():
    data = fetch_from_api(
        endpoint=f"competitions/{COMPETITION_CODE}/standings"
    )

    save_json_to_bronze(data, "standings", COMPETITION_NAME, SEASON)


if __name__ == "__main__":
    extract_results()
    extract_standings()