# LogSense dashboard

## Purpose

The new `/dashboard` is a **small read-only** analytics UI. It displays:

- Total imported records and counts for ERROR, WARNING and INFO
- Severity distribution
- Errors grouped over the past seven days **by UTC import date**
- Five most repeated full ERROR messages
- The latest 100 stored records with local search and a severity filter
- Empty, loading, and API error states

No React build or external charting library is needed. Assets ship under `app/dashboard/` and are served directly by FastAPI, keeping the frontend deliberately small.

## Local use

1. Create your `.env` by copying `.env.example`, change the password, and run `docker compose up --build -d`.
2. Open http://localhost:8000/dashboard.
3. Initially the dashboard may be empty. Run `curl -X POST http://localhost:8000/logs/import`.
4. Use **Refresh data**; search/filter the recent log table.
5. Confirm that a second import returns `imported_count: 0` and a nonzero `skipped_count`.

Note: `/logs/summary` reads the sample file and **does not** represent imported records; `/logs/dashboard-summary` is the dashboard's DB-backed source.

## Evidence

The bundled preview screenshot (`screenshots/logsense-dashboard-preview.png`) was rendered from a local SQLite test API response. After running the Docker/PostgreSQL verification, capture a final working screenshot at `screenshots/logsense-dashboard.png` and ensure it corresponds to a running, populated dashboard. A local SQLite-backed screenshot is suitable for showing UI layout, but the Docker/PostgreSQL flow should be verified separately for the portfolio's deployment claim.
