CREATE SCHEMA IF NOT EXISTS silver;

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