CREATE MATERIALIZED VIEW gold.current_standings AS
WITH team_results AS (

    SELECT
        home_team_id AS team_id,
        home_goals AS goals_for,
        away_goals AS goals_against,

        CASE 
            WHEN home_goals > away_goals THEN 1
            ELSE 0
        END AS wins,

        CASE 
            WHEN home_goals = away_goals THEN 1
            ELSE 0
        END AS draws,

        CASE 
            WHEN home_goals < away_goals THEN 1
            ELSE 0
        END AS losses,

        CASE
            WHEN home_goals > away_goals THEN 3
            WHEN home_goals = away_goals THEN 1
            ELSE 0
        END AS points

    FROM silver.matches
    WHERE status = 'FINISHED'


    UNION ALL

    SELECT
        away_team_id AS team_id,
        away_goals AS goals_for,
        home_goals AS goals_against,

        CASE 
            WHEN away_goals > home_goals THEN 1
            ELSE 0
        END AS wins,

        CASE 
            WHEN away_goals = home_goals THEN 1
            ELSE 0
        END AS draws,

        CASE 
            WHEN away_goals < home_goals THEN 1
            ELSE 0
        END AS losses,

        CASE
            WHEN away_goals > home_goals THEN 3
            WHEN away_goals = home_goals THEN 1
            ELSE 0
        END AS points

    FROM silver.matches
    WHERE status = 'FINISHED'
)
SELECT
    team_id,

    COUNT(*) AS played,

    SUM(wins) AS wins,
    SUM(draws) AS draws,
    SUM(losses) AS losses,

    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,

    SUM(points) AS points

FROM team_results
GROUP BY team_id;