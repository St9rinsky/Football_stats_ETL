import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime
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


def insert_standing_snapshot(cursor, standing_row, competition, season_year, snapshot_date, snapshot_week):
    team = standing_row.get("team", {})

    sql = """
        INSERT INTO silver.standings_snapshot (
            competition_code,
            competition_name,
            season,
            snapshot_date,
            snapshot_week,
            position,
            team_id,
            team_name,
            played_games,
            won,
            draw,
            lost,
            points,
            goals_for,
            goals_against,
            goal_difference
        )
        VALUES (
            %(competition_code)s,
            %(competition_name)s,
            %(season)s,
            %(snapshot_date)s,
            %(snapshot_week)s,
            %(position)s,
            %(team_id)s,
            %(team_name)s,
            %(played_games)s,
            %(won)s,
            %(draw)s,
            %(lost)s,
            %(points)s,
            %(goals_for)s,
            %(goals_against)s,
            %(goal_difference)s
        )
        ON CONFLICT (competition_code, season, snapshot_week, team_id)
        DO NOTHING;
    """

    values = {
        "competition_code": competition.get("code"),
        "competition_name": competition.get("name"),
        "season": season_year,
        "snapshot_date": snapshot_date,
        "snapshot_week": snapshot_week,
        "position": standing_row.get("position"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "played_games": standing_row.get("playedGames"),
        "won": standing_row.get("won"),
        "draw": standing_row.get("draw"),
        "lost": standing_row.get("lost"),
        "points": standing_row.get("points"),
        "goals_for": standing_row.get("goalsFor"),
        "goals_against": standing_row.get("goalsAgainst"),
        "goal_difference": standing_row.get("goalDifference")
    }

    cursor.execute(sql, values)


def load_standings_to_silver(file_path):
    data = load_json_file(file_path)

    if "standings" not in data:
        raise ValueError("This is not a standings file. Expected key 'standings'.")

    competition = data.get("competition", {})
    season = data.get("season", {})
    season_year = season.get("startDate", "")[:4] if season.get("startDate") else None

    today = datetime.now()
    snapshot_date = today.date()
    snapshot_week = today.isocalendar().week

    connection = get_db_connection()
    cursor = connection.cursor()

    loaded_rows = 0

    try:
        for standing_group in data["standings"]:
            if standing_group.get("type") == "TOTAL":
                for row in standing_group.get("table", []):
                    insert_standing_snapshot(
                        cursor,
                        row,
                        competition,
                        season_year,
                        snapshot_date,
                        snapshot_week
                    )
                    loaded_rows += 1

        connection.commit()
        print(f"Loaded {loaded_rows} standings rows into silver.standings_snapshot")

    except Exception as error:
        connection.rollback()
        print("Failed to load standings:", error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    latest_file = get_latest_bronze_file("standings")
    load_standings_to_silver(latest_file)