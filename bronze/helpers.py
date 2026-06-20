import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

def fetch_from_api(endpoint: str, params = None):
    """
    Fetches data from the football api\n
    Takes a url endpoint and a parameter\n\n

    RETURNS: a JSON data object\n
    RAISES: http error if occurs

    """
    load_dotenv()

    API_KEY = os.getenv("FOOTBALL_API_KEY")
    BASE_URL = BASE_URL = "https://api.football-data.org/v4"
    headers = {"X-Auth-Token": API_KEY, "X-Unfold-Goals": "true"}
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers = headers, params = params)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    response.raise_for_status()
    return response.json()


def save_json_to_bronze(data: json, dataset_name: str, competition_name: str, season: int):
    """
    Saving the Json into the correct folder\n
    Saving the Json folder with the proper name\n
    """

    date = datetime.now().strftime("%Y-%m-%d")
    folder_path = (f"data/bronze/{competition_name}/{season}/{dataset_name}")
    file_name = (f"{date}_{competition_name}_{dataset_name}.json")
    file_path = f"{folder_path}/{file_name}"

    os.makedirs(folder_path, exist_ok = True)

    with open(file_path, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved bronze {dataset_name} file: {file_name} into {folder_path}\n")


