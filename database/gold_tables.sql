CREATE TABLE gold.standings_snapshot (
    snapshot_date DATE,
    team_id INT,
    played INT,
    wins INT,
    draws INT,
    losses INT,
    goals_for INT,
    goals_against INT,
    points INT,

    PRIMARY kEY (snapshot_date, team_id)

);