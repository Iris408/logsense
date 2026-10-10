# LogSense maintenance policy

**Lifecycle:** Maintenance  
**Entered maintenance:** 10 October 2026  
**Release evidence:** [Final verification](final-verification.md) · [Finalisation PR #1](https://github.com/Iris408/logsense/pull/1)

## Completed scope

- FastAPI REST API and PostgreSQL/SQLAlchemy persistence
- Sequential repeat-import protection for the configured sample file
- Read-only HTML/CSS/JavaScript analytics dashboard
- Severity counts, recurring errors, seven-day UTC **import-date** summary, recent record search and filter
- CLI/file analysis and reporting tools
- Docker Compose for a local, persistent PostgreSQL-backed demo
- Seven automated regression tests plus Backend CI and Docker CI smoke tests
- Architecture, API and dashboard documentation

## What maintenance includes

- Fix verified defects without expanding product scope.
- Keep Python, FastAPI, PostgreSQL container and dependencies reasonably up to date.
- Review dependency/security advisories and keep GitHub Actions green.
- Maintain setup documentation and capture improved screenshots when the UI changes.
- Run tests and Docker smoke checks after changes affecting ingestion, persistence or dashboards.

## Checks before merging a maintenance PR

```bash
python3 -m pytest -q
# From a local environment with .env configured:
docker compose up --build -d
curl --fail http://localhost:8002/
curl --fail http://localhost:8002/dashboard
docker compose down
```

The GitHub branch protection rules should require Backend CI and Docker CI when available. Never use `docker compose down -v` if you intend to preserve existing database content.

## Explicit limitations

This is a **trusted-local portfolio application**, not a production log platform. There is no authentication or multi-tenant isolation. Write/delete endpoints must not be exposed on the public internet. A Docker named volume provides persistence but not backup/recovery. Ingestion is not concurrency-safe or rotation-aware. The seven-day chart represents UTC **import dates**, not original event timestamps.

## Future architecture: Kansoku Cloud

Distributed ingestion, OpenTelemetry/OTLP, ClickHouse, queues/workers, AWS, Terraform, scaling, recovery and cloud operations are deliberately separate from LogSense maintenance.