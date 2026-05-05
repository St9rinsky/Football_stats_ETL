CREATE SCHEMA IF NOT EXISTS silver;


CREATE TABLE IF NOT EXISTS silver.fixtures (
    match_id INT PRIMARY KEY,
    competition_code VARCHAR(10),
    competition_name VARCHAR(100),
    season INT,
    match_date TIMESTAMP,
    status VARCHAR(50),
    home_team_id INT,
    home_team_name VARCHAR(100),
    away_team_id INT,
    away_team_name VARCHAR(100),
    last_updated TIMESTAMP,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.results (
    match_id INT PRIMARY KEY,

    competition_code VARCHAR(10),
    competition_name VARCHAR(100),
    season INT,

    match_date TIMESTAMP,
    status VARCHAR(50),

    home_team_id INT,
    home_team_name VARCHAR(100),
    away_team_id INT,
    away_team_name VARCHAR(100),

    home_score INT,
    away_score INT,
    winner VARCHAR(20),

    last_updated TIMESTAMP,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.standings_snapshot (
    snapshot_id SERIAL PRIMARY KEY,

    competition_code VARCHAR(10),
    competition_name VARCHAR(100),
    season INT,

    snapshot_date DATE,
    snapshot_week INT,

    position INT,
    team_id INT,
    team_name VARCHAR(100),

    played_games INT,
    won INT,
    draw INT,
    lost INT,
    points INT,
    goals_for INT,
    goals_against INT,
    goal_difference INT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (competition_code, season, snapshot_week, team_id)
);