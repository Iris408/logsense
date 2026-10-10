# LogSense finalisation notes

## Why a small dashboard?

The backend already implements log importing and reporting. A small, read-only web view proves that the API can power an accessible operational interface without turning LogSense into another standalone frontend product. The frontend uses native HTML/CSS/JavaScript rather than a second deployment or framework toolchain.

## Key decisions

1. **Preserve the current PostgreSQL table.** Existing data should remain compatible; avoid expanding scope with migrations.
2. **Deduplicate counts, not unique message strings.** The same error may legitimately occur multiple times in one file. A naive uniqueness check would erase meaningful frequency data.
3. **Separate file summaries from stored-record summaries.** The dashboard's metrics must reflect actual imported records, not unsaved sample changes.
4. **Be transparent about timestamps.** The demo's source lines have no real event timestamps, so the trend chart is about import activity.
5. **Automate meaningful checks.** Existing CI could pass with no `tests/` directory. The finalisation adds regression tests and requires them to run, plus a Docker Compose smoke test.

## Out of scope / future work

Concurrently safe ingestion, rotation-aware source tracking, multi-tenant permissions, cloud delivery, durable migration strategy, backups and operational recovery belong to a larger ingestion platform. LogSense remains a bounded portfolio demonstration with possible expansion into Kansoku Cloud.
