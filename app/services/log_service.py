"""LogSense log ingestion and read-only reporting services."""

from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.log_model import LogEntry

LOG_FILE_PATH = Path("sample_logs/server.log")
REPORT_FILE_PATH = Path("analysis_report.txt")
SEVERITIES = ("INFO", "WARNING", "ERROR", "UNKNOWN")


def read_log_file():
    if not LOG_FILE_PATH.exists():
        raise FileNotFoundError(f"Log file not found: {LOG_FILE_PATH}")
    return LOG_FILE_PATH.read_text(encoding="utf-8").splitlines()


def read_analysis_report():
    if not REPORT_FILE_PATH.exists():
        raise FileNotFoundError(f"Report file not found: {REPORT_FILE_PATH}")
    return REPORT_FILE_PATH.read_text(encoding="utf-8")


def get_log_severity(line: str) -> str:
    """Classify the current single-file demo's plain-text log records."""
    import re
    match = re.search(r"\b(ERROR|WARNING|INFO)\b", line)
    return match.group(1) if match else "UNKNOWN"


def get_log_summary():
    """Legacy sample-file summary. The dashboard uses database aggregates instead."""
    lines = read_log_file()
    counts = Counter(get_log_severity(line) for line in lines if line.strip())
    return {
        "total_lines": len(lines),
        "info_count": counts["INFO"],
        "warning_count": counts["WARNING"],
        "error_count": counts["ERROR"],
    }


def get_error_logs():
    return [line.strip() for line in read_log_file()
            if get_log_severity(line) == "ERROR"]


def import_logs_to_database(db: Session):
    """Idempotently import the currently configured single source file.

    Compare each message's occurrence number in the source against the number
    already stored. Legitimate repeated lines within the file are preserved,
    while importing the same snapshot twice adds no extra rows. This is a
    bounded, sequential single-source strategy, not a concurrent ingestion
    mechanism or multi-file event identity scheme.
    """
    existing_counts = Counter({
        (severity, message): count
        for severity, message, count in db.query(
            LogEntry.severity, LogEntry.message, func.count(LogEntry.id)
        ).group_by(LogEntry.severity, LogEntry.message).all()
    })
    occurrences_in_file = Counter()
    added = 0
    skipped = 0

    for line in read_log_file():
        clean_line = line.strip()
        if not clean_line:
            continue
        severity = get_log_severity(clean_line)
        key = (severity, clean_line)
        occurrences_in_file[key] += 1
        if occurrences_in_file[key] <= existing_counts[key]:
            skipped += 1
            continue
        db.add(LogEntry(timestamp=None, severity=severity, message=clean_line))
        added += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Log import complete",
        "imported_count": added,
        "skipped_count": skipped,
    }


def get_stored_logs(db: Session, limit=None, severity=None):
    query = db.query(LogEntry)
    if severity:
        query = query.filter(LogEntry.severity == severity)
    query = query.order_by(LogEntry.created_at.desc(), LogEntry.id.desc())
    if limit is not None:
        query = query.limit(limit)
    return [{
        "id": log.id,
        "timestamp": log.timestamp,
        "severity": log.severity,
        "message": log.message,
        "created_at": log.created_at,
    } for log in query.all()]


def get_dashboard_summary(db: Session):
    """Aggregate imported database records (never the sample file)."""
    levels = {severity: 0 for severity in SEVERITIES}
    for severity, count in db.query(
        LogEntry.severity, func.count(LogEntry.id)
    ).group_by(LogEntry.severity).all():
        levels[severity] = count

    most_common_errors = db.query(
        LogEntry.message, func.count(LogEntry.id).label("count")
    ).filter(LogEntry.severity == "ERROR").group_by(
        LogEntry.message
    ).order_by(func.count(LogEntry.id).desc(), LogEntry.message).limit(5).all()

    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=6)
    error_days = Counter()
    for (created_at,) in db.query(LogEntry.created_at).filter(
        LogEntry.severity == "ERROR",
        LogEntry.created_at >= datetime.combine(start, datetime.min.time()),
    ).all():
        error_days[created_at.date().isoformat()] += 1

    last_ingested_at = db.query(func.max(LogEntry.created_at)).scalar()
    return {
        "total_logs": sum(levels.values()),
        "counts": levels,
        "top_errors": [
            {"message": message, "count": count}
            for message, count in most_common_errors
        ],
        "errors_by_day": [{
            "date": (start + timedelta(days=offset)).isoformat(),
            "count": error_days[(start + timedelta(days=offset)).isoformat()],
        } for offset in range(7)],
        "last_imported_at": last_ingested_at,
    }


def clear_stored_logs(db: Session):
    deleted_count = db.query(LogEntry).delete()
    db.commit()
    return {"message": "Stored logs cleared successfully", "deleted_count": deleted_count}


def get_latest_log_entries(limit: int = 5):
    lines = [line.strip() for line in read_log_file() if line.strip()]
    latest_lines = lines[-limit:]
    return {
        "latest_logs": [{
            "severity": get_log_severity(line), "message": line,
        } for line in latest_lines],
        "total_returned": len(latest_lines),
    }
