INSERT INTO gold.standings_snapshot
(
    snapshot_date,
    team_id,
    played,
    wins,
    draws,
    losses,
    goals_for,
    goals_against,
    points
)

SELECT
    CURRENT_DATE,
    team_id,
    played,
    wins,
    draws,
    losses,
    goals_for,
    goals_against,
    points

FROM gold.current_standings;