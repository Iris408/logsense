# LogSense architecture

## Scope

LogSense is a **single-file log analysis portfolio project**, not a distributed ingestion service. The API is implemented in FastAPI. PostgreSQL holds imported log records. A small HTML/CSS/JavaScript dashboard is served by the same API, requiring no separate frontend deployment.

```text
sample_logs/server.log
        │ POST /logs/import (explicit, local demo)
        ▼
FastAPI ── log service ── SQLAlchemy ── PostgreSQL
   │                               ▲
   ├─ GET /logs/dashboard-summary ─┤
   ├─ GET /logs/stored ────────────┘
   └─ GET /dashboard + bundled static assets
                    │
                    ▼
              Read-only web UI
```

## Dashboard data

- `/logs/dashboard-summary` aggregates **database** records by severity, repeated error message, and import date.
- `/logs/stored?limit=100` supplies the most recent imported records for the dashboard's client-side search and filters.
- `/logs/summary`, `/logs/errors`, and `/logs/live` remain legacy **sample-file** endpoints to preserve existing API behaviour; they do not represent the database dashboard.
- The sample log has no true event timestamps. The dashboard explicitly labels its time chart and record dates by **import time, UTC**, not the original event time.

## Import idempotency

`POST /logs/import` counts occurrences of each `(severity, full message)` in the single configured log file and imports only occurrences not already present in the database. That means a repeated error genuinely appearing three times in the source is stored three times, but importing the same snapshot again adds none. Appending more matching records can add the new occurrences without re-importing the earlier ones.

This strategy is intentionally limited. It does **not** distinguish two independent source files with the same messages, track rotations/rewrites, or guarantee idempotency under simultaneous import requests. Those require durable source identity and unique record keys at the database layer; that belongs to any future Kansoku Cloud ingestion project, not this maintenance release.

## Data model

The existing `log_entries` table is unchanged to preserve compatibility with existing PostgreSQL data. It includes `id`, `timestamp` (nullable source field), `severity`, `message`, and `created_at` (UTC import time by convention). The finalisation does not introduce migrations.

## Security and deployment constraints

- The dashboard is read-only. API write endpoints (`POST /logs/import`, `DELETE /logs/stored`) remain available for **trusted local use**, not an internet-facing service.
- Docker Compose binds the API to `127.0.0.1`, avoids publishing the PostgreSQL port, and requires an environment-defined database password.
- `.env` is ignored by Git and should never contain checked-in credentials. The checked-in `.env.example` contains an illustrative replacement value only.
- There is **no user authentication or RBAC**. Do not deploy publicly without auth, rate limits, source validation, and removing or protecting destructive routes.
- Database persistence is provided by a Docker named volume, **not a backup system**. This demo must not be presented as recovery-ready production infrastructure.

## Intentional non-goals

ClickHouse, OTLP/OpenTelemetry ingest, queues, cloud deployment, Terraform, Kubernetes, multi-source ingestion and distributed workers are all future Kansoku Cloud concerns.
