# API Examples

Example requests for interacting with the LogSense API.

> **Note**
>
> These examples assume the FastAPI application is running locally at:
>
> ```
> http://127.0.0.1:8002
> ```

---

# Import Logs

Imports log entries into PostgreSQL.

## Request

```bash
curl -X POST http://127.0.0.1:8002/logs/import
```

---

# View Stored Logs

Returns all stored log entries.

## Request

```bash
curl http://127.0.0.1:8002/logs/stored
```

---

# View Log Summary

Returns a summary of log severities.

## Request

```bash
curl http://127.0.0.1:8002/logs/summary
```

---

# View Error Logs

Returns only ERROR log entries.

## Request

```bash
curl http://127.0.0.1:8002/logs/errors
```

---

# Generate Analysis Report

Generates an analysis report from the stored logs.

## Request

```bash
curl http://127.0.0.1:8002/logs/report
```

---

# View Live Logs

Returns the latest entries from the monitored log file.

## Request

```bash
curl http://127.0.0.1:8002/logs/live
```

---

# Clear Stored Logs

Deletes all stored log entries from PostgreSQL.

> Intended for development and testing.

## Request

```bash
curl -X DELETE http://127.0.0.1:8002/logs/stored
```