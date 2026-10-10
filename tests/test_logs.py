"""Regression tests for the bounded LogSense finalisation milestone."""

from app.services import log_service


def test_dashboard_and_api_are_served(client):
    assert client.get("/").status_code == 200
    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
    assert "LogSense" in dashboard.text
    assert client.get("/dashboard/assets/dashboard.css").status_code == 200
    assert client.get("/dashboard/assets/dashboard.js").status_code == 200


def test_summary_initially_empty(client):
    payload = client.get("/logs/dashboard-summary").json()
    assert payload["total_logs"] == 0
    assert payload["counts"]["ERROR"] == 0
    assert payload["top_errors"] == []
    assert len(payload["errors_by_day"]) == 7
    assert payload["last_imported_at"] is None


def test_repeated_import_is_idempotent_and_preserves_real_repeats(client, monkeypatch, tmp_path):
    sample = tmp_path / "server.log"
    sample.write_text(
        "INFO Booted\nERROR Database timeout\nERROR Database timeout\n"
        "WARNING Slow request\n", encoding="utf-8",
    )
    monkeypatch.setattr(log_service, "LOG_FILE_PATH", sample)

    first = client.post("/logs/import")
    assert first.status_code == 200
    assert first.json()["imported_count"] == 4
    assert first.json()["skipped_count"] == 0

    second = client.post("/logs/import")
    assert second.json()["imported_count"] == 0
    assert second.json()["skipped_count"] == 4

    summary = client.get("/logs/dashboard-summary").json()
    assert summary["total_logs"] == 4
    assert summary["counts"]["ERROR"] == 2
    assert summary["top_errors"][0]["count"] == 2
    assert summary["last_imported_at"] is not None

    sample.write_text(sample.read_text() + "ERROR Database timeout\nINFO Ready\n", encoding="utf-8")
    third = client.post("/logs/import")
    assert third.json()["imported_count"] == 2
    assert third.json()["skipped_count"] == 4
    assert client.get("/logs/dashboard-summary").json()["total_logs"] == 6


def test_stored_log_limit_and_filter(client, monkeypatch, tmp_path):
    sample = tmp_path / "records.log"
    sample.write_text("INFO Started\nERROR Down\nWARNING Busy\n", encoding="utf-8")
    monkeypatch.setattr(log_service, "LOG_FILE_PATH", sample)
    client.post("/logs/import")

    response = client.get("/logs/stored?severity=ERROR&limit=1")
    assert response.status_code == 200
    logs = response.json()["logs"]
    assert len(logs) == 1
    assert logs[0]["severity"] == "ERROR"

    assert client.get("/logs/stored?limit=0").status_code == 422
    assert client.get("/logs/stored?severity=INVALID").status_code == 422


def test_dashboard_uses_database_not_the_sample_file(client, monkeypatch, tmp_path):
    sample = tmp_path / "records.log"
    sample.write_text("INFO One\n", encoding="utf-8")
    monkeypatch.setattr(log_service, "LOG_FILE_PATH", sample)
    client.post("/logs/import")
    sample.write_text("INFO One\nERROR Not yet imported\n", encoding="utf-8")

    summary = client.get("/logs/dashboard-summary").json()
    assert summary["total_logs"] == 1
    assert summary["counts"]["ERROR"] == 0
    assert client.get("/logs/summary").json()["total_lines"] == 2


def test_missing_cli_report_returns_404(client, monkeypatch, tmp_path):
    monkeypatch.setattr(log_service, "REPORT_FILE_PATH", tmp_path / "missing-report.txt")
    response = client.get("/logs/report")
    assert response.status_code == 404
    assert "No report generated" in response.json()["detail"]


def test_empty_report_cli_helpers():
    from analytics import calculate_percentages, analyze_error_hours
    assert calculate_percentages({"ERROR": [], "INFO": []}) == {"ERROR": 0.0, "INFO": 0.0}
    assert analyze_error_hours({"ERROR": ["no timestamp"]}) == {}
