-- Active: 1782061921007@@127.0.0.1@5432@Football_stats
CREATE MATERIALIZED VIEW gold.current_standings AS
WITH team_results AS (

    SELECT
        t.team_name AS team_name,
        m.home_goals AS goals_for,
        m.away_goals AS goals_against,

        CASE 
            WHEN m.home_goals > m.away_goals THEN 1
            ELSE 0
        END AS wins,

        CASE 
            WHEN m.home_goals = m.away_goals THEN 1
            ELSE 0
        END AS draws,

        CASE 
            WHEN m.home_goals < m.away_goals THEN 1
            ELSE 0
        END AS losses,

        CASE
            WHEN m.home_goals > m.away_goals THEN 3
            WHEN m.home_goals = m.away_goals THEN 1
            ELSE 0
        END AS points

    FROM silver.matches m
    INNER JOIN silver.teams t 
    ON m.home_team_id = t.team_id
    WHERE status = 'FINISHED'


    UNION ALL

    SELECT
        t.team_name AS team_name,
        m.away_goals AS goals_for,
        m.home_goals AS goals_against,

        CASE 
            WHEN m.away_goals > m.home_goals THEN 1
            ELSE 0
        END AS wins,

        CASE 
            WHEN m.away_goals = m.home_goals THEN 1
            ELSE 0
        END AS draws,

        CASE 
            WHEN m.away_goals < m.home_goals THEN 1
            ELSE 0
        END AS losses,

        CASE
            WHEN m.away_goals > m.home_goals THEN 3
            WHEN m.away_goals = m.home_goals THEN 1
            ELSE 0
        END AS points

    FROM silver.matches m
    INNER JOIN silver.teams t 
    ON m.away_team_id = t.team_id
    WHERE status = 'FINISHED'
)
SELECT
    team_name,

    COUNT(*) AS played,

    SUM(wins) AS wins,
    SUM(draws) AS draws,
    SUM(losses) AS losses,

    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,

    SUM(points) AS points

FROM team_results
GROUP BY team_name;