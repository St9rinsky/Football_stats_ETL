import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

COMPETITION_CODE = "PL"
COMPETITION_NAME = "premier_league"
SEASON = 2025

def save_json_to_bronze(data: json, dataset_name: str, competition_name: str, season: int):
    """
    Saving the Json into the correct folder\n
    Saving the Json folder with the proper name\n
    """

    date = datetime.now().strftime("%Y-%m-%d")

    folder_path = (f"data/bronze/{competition_name}/{season}/{dataset_name}")
    
    file_name = (f"{date}_{competition_name}_{dataset_name}.json")

    file_path = f"{folder_path}/{file_name}"

    os.makedirs(folder_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved bronze {dataset_name} file: {file_path}\n")

def fetch_from_api(endpoint: str, params=None):
    """
    Fetches data from the football api\n
    Takes a url endpoint and a parameter\n\n

    RETURNS: a JSON data object\n
    RAISES: http error if occurs

    """

    headers = {"X-Auth-Token": API_KEY}
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers, params=params)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    response.raise_for_status()
    return response.json()

#http://api.football-data.org/v4/competitions/2003/matches?matchday=1"
def extract_all_matches():
    data = fetch_from_api(
        endpoint=f"competitions/{COMPETITION_CODE}/matches",
        params={"season": SEASON}
        )

    save_json_to_bronze(data, "Matches", COMPETITION_NAME, SEASON)

def extract_match_data(status :str, dataset_name :str):
    date = datetime.now()
    date_from = date.strftime("%Y-%m-%d")
    date_to = date + timedelta(days = 7)

    data = fetch_from_api(
        endpoint=f"competitions/{COMPETITION_CODE}/matches",
        params={"dateFrom":date_from,"dateTo":date_to.strftime("%Y-%m-%d"),"status":status}
        )
    
    save_json_to_bronze(data, dataset_name,COMPETITION_NAME,SEASON)

# http://api.football-data.org/v4/competitions/PL/standings
def extract_standings():
    data = fetch_from_api( endpoint=f"competitions/{COMPETITION_CODE}/standings")

    save_json_to_bronze(data, "Standings", COMPETITION_NAME, SEASON)


if __name__ == "__main__":
    extract_all_matches()
    extract_match_data("SCHEDULED", "Fixtures")
    extract_match_data("FINISHED", "Results")
    extract_standings()