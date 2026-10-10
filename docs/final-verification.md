# Final verification checklist

## Automated (must pass before merging)

- [ ] `python -m pytest -q` — seven regression tests pass using isolated in-memory SQLite.
- [ ] Backend CI builds the Docker image and runs real tests.
- [ ] Docker CI starts FastAPI + PostgreSQL, serves `/dashboard`, imports records, and confirms the second import adds zero records.

## Manual (requires your local environment)

- [ ] Copy `.env.example` to `.env` and replace the local password.
- [ ] `docker compose up --build -d` succeeds with healthy PostgreSQL.
- [ ] `/docs`, `/dashboard`, `/logs/stored`, and `/logs/dashboard-summary` load.
- [ ] Import source logs once, then import them again; confirm no new duplicates.
- [ ] Validate the populated chart, severity bars, repeated errors and log search/filter.
- [ ] Restart Docker Compose and confirm imported records persist in the named volume.
- [ ] Capture an actual populated screenshot and add it to your README/portfolio.
- [ ] Confirm checked-in files contain no secrets; never publicly expose write/delete endpoints without authentication.

## Definition of done

Move LogSense to **Maintenance** only after automated checks and local PostgreSQL smoke tests pass and the final screenshots/docs are reviewed. This package was locally tested using SQLite; it does not by itself prove your deployment works on the real Docker/PostgreSQL stack.
