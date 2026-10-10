"""LogSense API routes. The dashboard does not offer write operations."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.log_service import (
    clear_stored_logs,
    get_dashboard_summary,
    get_error_logs,
    get_log_summary,
    get_stored_logs,
    import_logs_to_database,
    read_analysis_report,
    get_latest_log_entries,
)

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/summary")
def log_summary():
    return get_log_summary()


@router.get("/errors")
def error_logs():
    return {"errors": get_error_logs()}


@router.get("/report")
def analysis_report():
    try:
        return {"report": read_analysis_report()}
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="No report generated yet. Run python analyzer.py first.",
        ) from exc


@router.get("/dashboard-summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)


@router.get("/stored")
def stored_logs(
    limit: int | None = Query(default=None, ge=1, le=500),
    severity: Literal["INFO", "WARNING", "ERROR", "UNKNOWN"] | None = None,
    db: Session = Depends(get_db),
):
    return {"logs": get_stored_logs(db, limit=limit, severity=severity)}


@router.get("/live")
def live_logs(limit: int = Query(default=5, ge=1, le=100)):
    return get_latest_log_entries(limit)


@router.post("/import")
def import_logs(db: Session = Depends(get_db)):
    return import_logs_to_database(db)


@router.delete("/stored")
def delete_stored_logs(db: Session = Depends(get_db)):
    return clear_stored_logs(db)
