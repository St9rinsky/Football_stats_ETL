CREATE TABLE IF NOT EXISTS silver.teams (

    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    team_short_name VARCHAR(100) NOT NULL

);

CREATE TABLE IF NOT EXISTS silver.matches (

    match_id INTEGER PRIMARY KEY,
    match_day INTEGER,
    match_date TIMESTAMP,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_goals INTEGER,
    away_goals INTEGER,
    status VARCHAR(20),

    FOREIGN KEY(home_team_id)
    REFERENCES silver.teams(team_id),

    FOREIGN KEY(away_team_id)
    REFERENCES silver.teams(team_id)

);


CREATE TABLE IF NOT EXISTS silver.players (

    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(100),
    team_id INTEGER,

    FOREIGN KEY(team_id)
    REFERENCES silver.teams(team_id)

);


CREATE TABLE IF NOT EXISTS silver.player_match_stats (

    match_id INTEGER,
    player_id INTEGER,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,

    PRIMARY KEY(match_id, player_id)

);

