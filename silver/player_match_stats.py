from database.connection import db_connect 
from silver.helpers import read_json_file, extract_latest_bronze_file

def extract_player_stats(data :dict):
    player_stats = {}
    if "matches" not in data:
        raise ValueError("no matches in data")

    if data.get("resultSet",{}).get("count",0) <= 0:
        return player_stats
    
    for match in data.get("matches",[]):
        match_id = match.get("id")
        status = match.get("status")

        if status == "FINISHED":
            if match.get("score",{}).get("fullTime",{}).get("home",0) == 0 and match.get("score",{}).get("fullTime",{}).get("away",0) == 0:
                    continue
            
            goals = match.get("goals",[])
            for goal in goals:
                scorer_id = goal.get("scorer", {}).get("id")
                assist_id = goal.get("assist", {}).get("id")

                if scorer_id:
                    key = (match_id,scorer_id)

                    if key not in player_stats:
                        player_stats[key] = {
                            "match_id": match_id,
                            "player_id": scorer_id,
                            "goals": 0,
                            "assists": 0}
                        
                    player_stats[key]["goals"] += 1

                if assist_id:
                    key = (match_id, assist_id)

                    if key not in player_stats:
                        player_stats[key] = {
                            "match_id": match_id,
                            "player_id": assist_id,
                            "goals": 0,
                            "assists": 0}

                    player_stats[key]["assists"] += 1
            
    return player_stats

def load_player_stats_to_silverDB(player_stats :dict):
    try:
        connection = db_connect()
        cursor = connection.cursor()

        player_stat = 0
        for stat in player_stats.values():
            sql = """
            INSERT INTO silver.player_match_stats (
                match_id,
                player_id,
                goals,
                assists
            )

            VALUES (
                %(match_id)s,
                %(player_id)s,
                %(goals)s,
                %(assists)s
            )
            """

            cursor.execute(sql, stat)
            player_stat += 1

        connection.commit()
        print(f"added {player_stat} new player stats")
    
    except Exception as error:
        connection.rollback()
        print("Failed to save stats", error)

    finally:
        cursor.close()
        connection.close()

def main():
    file = extract_latest_bronze_file(Season = 2025, Competition_name = "premier_league", folder_name = "Matches")
    data = read_json_file(file)
    players = extract_player_stats(data)
    load_player_stats_to_silverDB(players)

if __name__ == "__main__":
    main()