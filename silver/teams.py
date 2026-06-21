from database.connection import db_connect 
from silver.helpers import read_json_file, extract_latest_bronze_file


def extract_teams(data :dict):
    teams = []
    if "matches" not in data:
        raise ValueError("no matches in data")

    if data.get("resultSet",{}).get("count",0) <= 0:
        return teams
    
    for match in data.get("matches",[]):
        home = match.get("homeTeam")
        away = match.get("awayTeam")

        teams.append({
            "team_id": home.get("id"),
            "team_name": home.get("name"),
            "team_short_name": home.get("shortName")})
        
        teams.append({
            "team_id": away.get("id"),
            "team_name": away.get("name"),
            "team_short_name": away.get("shortName")})

            
    return teams

def load_teams_to_silverDB(teams :dict):
    try:
        connection = db_connect()
        cursor = connection.cursor()

        inserted_teams = 0

        for team in teams:
            sql = """
            INSERT INTO silver.teams (
                team_id,
                team_name,
                team_short_name
            )

            VALUES (
                %(team_id)s,
                %(team_name)s,
                %(team_short_name)s
            )

            ON CONFLICT (team_id)
            DO UPDATE SET
                team_name = EXCLUDED.team_name,
                team_short_name = EXCLUDED.team_short_name
            WHERE silver.teams.team_name <> EXCLUDED.team_name
            OR silver.teams.team_short_name <> EXCLUDED.team_short_name

            RETURNING match_id;
            """

            cursor.execute(sql, team)
            result = cursor.fetchone()
            if result:
                inserted_teams += 1

        connection.commit()
        print(f"{inserted_teams} new teams")
    
    except Exception as error:
        connection.rollback()
        print("Failed to save teams", error)

    finally:
        cursor.close()
        connection.close()

def main():
    file = extract_latest_bronze_file(Season = 2025, Competition_name = "premier_league", folder_name = "Matches")
    data = read_json_file(file)
    players = extract_teams(data)
    load_teams_to_silverDB(players)

if __name__ == "__main__":
    main()