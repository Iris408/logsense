"""Small analytical helpers for the standalone LogSense CLI report."""

from collections import Counter


def calculate_percentages(log_data):
    total_logs = sum(len(logs) for logs in log_data.values())
    return {
        level: (len(logs) / total_logs * 100 if total_logs else 0.0)
        for level, logs in log_data.items()
    }


def analyze_error_hours(log_data):
    hour_counts = Counter()
    for log in log_data.get("ERROR", []):
        if "[" in log and "]" in log:
            timestamp = log.split("]", 1)[0].replace("[", "", 1)
            # When an ISO-like event timestamp exists, aggregate its hour.
            if "T" in timestamp:
                hour = timestamp.split("T", 1)[1].split(":", 1)[0]
            else:
                parts = timestamp.split(" ")
                hour = parts[-1].split(":", 1)[0] if ":" in parts[-1] else None
            if hour and hour.isdigit() and 0 <= int(hour) <= 23:
                hour_counts[hour.zfill(2)] += 1
    return hour_counts
