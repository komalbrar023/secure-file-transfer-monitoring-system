from flask import Flask, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONITORING_ZONE = os.path.join(BASE_DIR, "data", "monitoring_zone")
LOG_FILE = os.path.join(BASE_DIR, "logs", "audit.log")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def count_alerts():
    """Count security alerts from the audit log."""
    if not os.path.exists(LOG_FILE):
        return 0

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            return sum(1 for line in file if "ALERT" in line.upper())
    except Exception:
        return 0


def count_reports():
    """Count generated security reports."""
    if not os.path.exists(REPORTS_DIR):
        return 0

    try:
        return len([
            file for file in os.listdir(REPORTS_DIR)
            if file.endswith(".md")
        ])
    except Exception:
        return 0


def count_files():
    """Count files inside the monitoring zone."""
    if not os.path.exists(MONITORING_ZONE):
        return 0

    total = 0
    for root, dirs, files in os.walk(MONITORING_ZONE):
        total += len(files)

    return total


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        status="ACTIVE",
        monitoring_zone=MONITORING_ZONE,
        alerts=count_alerts(),
        reports=count_reports(),
        files=count_files(),
        hash_method="SHA-256",
        log_file=LOG_FILE,
        current_time=datetime.now().strftime("%d %B %Y, %H:%M:%S")
    )


if __name__ == "__main__":
    app.run(debug=True)