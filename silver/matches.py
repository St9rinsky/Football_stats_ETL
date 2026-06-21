from database.connection import db_connect 
from silver.helpers import read_json_file, extract_latest_bronze_file


    
def extract_matches(data: dict):
    matches = []
    if "matches" not in data:
        raise ValueError("no matches in data")
    
    if data.get("resultSet",{}).get("count",0) <= 0:
        return matches
    
    for match in data.get("matches",[]):
        match_id = match.get("id")
        match_day = match.get("matchday")
        match_date = match.get("utcDate")

        home_team_id = match.get("homeTeam",{}).get("id")
        away_team_id = match.get("awayTeam",{}).get("id")

        status = match.get("status")

        if status == "FINISHED":
            home_goals = match.get("score",{}).get("fullTime",{}).get("home")
            away_goals = match.get("score",{}).get("fullTime",{}).get("away")
        else:
            home_goals = None
            away_goals = None

        matches.append({
            "match_id" : match_id,
            "match_day" :match_day,
            "match_date" :match_date,
            "home_team_id" :home_team_id,
            "away_team_id": away_team_id,
            "status" :status,
            "home_goals": home_goals,
            "away_goals": away_goals
        })
        
    return matches

def load_matches_to_silverDB(matches :list):
    try:
        connection = db_connect()
        cursor = connection.cursor()

        inserted_matches = 0

        for match in matches:
            sql = """
            INSERT INTO silver.matches (
                match_id,
                match_day,
                match_date,
                home_team_id,
                away_team_id,
                home_goals,
                away_goals,
                status
            )

            VALUES (
                %(match_id)s,
                %(match_day)s,
                %(match_date)s,
                %(home_team_id)s,
                %(away_team_id)s,
                %(home_goals)s,
                %(away_goals)s,
                %(status)s
            )

            ON CONFLICT (match_id)
            DO UPDATE SET
                match_date = EXCLUDED.match_date,
                status = EXCLUDED.status,
                home_goals = EXCLUDED.home_goals,
                away_goals = EXCLUDED.away_goals
            WHERE silver.matches.match_date <> EXCLUDED.match_date
            OR silver.matches.status <> EXCLUDED.status
            OR silver.matches.home_goals <> EXCLUDED.home_goals
            OR silver.matches.away_goals <> EXCLUDED.away_goals

            RETURNING match_id;
            """

            cursor.execute(sql, match)
            result = cursor.fetchone()
            if result:
                inserted_matches += 1

        connection.commit()
        print(f"{inserted_matches} new matches")
    
    except Exception as error:
        connection.rollback()
        print("Failed to save matches", error)

    finally:
        cursor.close()
        connection.close()

def main():
    file = extract_latest_bronze_file(Season = 2025, Competition_name = "premier_league", folder_name = "Matches")
    data = read_json_file(file)
    matches = extract_matches(data)
    load_matches_to_silverDB(matches)


if __name__ == "__main__":
    main()