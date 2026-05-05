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


def insert_result(cursor, match):
    competition = match.get("competition", {})
    season = match.get("season", {})
    home_team = match.get("homeTeam", {})
    away_team = match.get("awayTeam", {})
    score = match.get("score", {})
    full_time = score.get("fullTime", {})

    sql = """
        INSERT INTO silver.results (
            match_id,
            competition_code,
            competition_name,
            season,
            match_date,
            status,
            home_team_id,
            home_team_name,
            away_team_id,
            away_team_name,
            home_score,
            away_score,
            winner,
            last_updated
        )
        VALUES (
            %(match_id)s,
            %(competition_code)s,
            %(competition_name)s,
            %(season)s,
            %(match_date)s,
            %(status)s,
            %(home_team_id)s,
            %(home_team_name)s,
            %(away_team_id)s,
            %(away_team_name)s,
            %(home_score)s,
            %(away_score)s,
            %(winner)s,
            %(last_updated)s
        )
        ON CONFLICT (match_id)
        DO UPDATE SET
            status = EXCLUDED.status,
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            winner = EXCLUDED.winner,
            last_updated = EXCLUDED.last_updated,
            loaded_at = CURRENT_TIMESTAMP;
    """

    values = {
        "match_id": match.get("id"),
        "competition_code": competition.get("code"),
        "competition_name": competition.get("name"),
        "season": season.get("startDate", "")[:4] if season.get("startDate") else None,
        "match_date": match.get("utcDate"),
        "status": match.get("status"),
        "home_team_id": home_team.get("id"),
        "home_team_name": home_team.get("name"),
        "away_team_id": away_team.get("id"),
        "away_team_name": away_team.get("name"),
        "home_score": full_time.get("home"),
        "away_score": full_time.get("away"),
        "winner": score.get("winner"),
        "last_updated": match.get("lastUpdated")
    }

    cursor.execute(sql, values)


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