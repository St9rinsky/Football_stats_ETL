from datetime import datetime, timedelta
from helpers import save_json_to_bronze, fetch_from_api


def extract_matches(Season :int , Competition_code :str):
    """
    Extracts match data for the next upcoming 7 days and previous 7 days
    """
    date = datetime.now()
    strfdate_from = (date - timedelta(days = 7)).strftime("%Y-%m-%d")
    strfdate_to = (date + timedelta(days = 7)).strftime("%Y-%m-%d")

    return fetch_from_api(
            endpoint = f"competitions/{Competition_code}/matches",
            params = {"season": Season,"dateFrom":strfdate_from,"dateTo":strfdate_to }
            )
    
def main():
    match_data = extract_matches(Season = 2025, Competition_code = "PL")
    save_json_to_bronze(data = match_data,season = 2025, competition_name = "Premier_league", dataset_name = "Matches")

if __name__ == "__main__":
    main()
