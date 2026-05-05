# Football_stats_ETL
“The pipeline uses different loading strategies depending on the data type. Fixtures and results are loaded incrementally using match IDs and updated timestamps, while league standings are captured as full weekly snapshots because table positions and points are state-based and change over time.”
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

[ SOURCE ]
     ↓
[ EXTRACT ]
     ↓
[ BRONZE (RAW) ]
     ↓
[ TRANSFORM ]
     ↓
[ SILVER (CLEAN) ]
     ↓
[ GOLD (ANALYTICS) ]