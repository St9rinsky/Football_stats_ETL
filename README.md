# Football_stats_ETL

                    ┌────────────────────┐
                    │   Football API      │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Weekly Batch Job    │
                    │ (Scheduled ETL)     │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────────────┐                 ┌──────────────────────┐
│ Fixtures / Results    │                 │ League Standings     │
│ Incremental Extract   │                 │ Full Snapshot Extract│
└─────────┬────────────┘                 └─────────┬────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐                 ┌──────────────────────┐
│ BRONZE LAYER          │                 │ BRONZE LAYER          │
│ Raw JSON (append)     │                 │ Raw JSON (append)     │
│ matches_*.json        │                 │ standings_*.json      │
└─────────┬────────────┘                 └─────────┬────────────┘
          │                                        │
          ▼                                        ▼
┌──────────────────────┐                 ┌──────────────────────┐
│ SILVER LAYER          │                 │ SILVER LAYER          │
│ Clean Matches Table   │                 │ Standings Snapshot    │
│ (Upsert by match_id)  │                 │ (Insert per week)     │
└─────────┬────────────┘                 └─────────┬────────────┘
          │                                        │
          └──────────────┬─────────────────────────┘
                         ▼
              ┌──────────────────────┐
              │ GOLD LAYER            │
              │ Analytics Tables      │
              │ - team_form           │
              │ - league_progression  │
              │ - top_scorers         │
              └─────────┬────────────┘
                        │
                        ▼
              ┌──────────────────────┐
              │ Dashboard / Queries  │
              └──────────────────────┘