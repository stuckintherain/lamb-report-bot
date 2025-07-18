import requests
import pandas as pd
from datetime import date, timedelta

# LMPR “Weekly Lamb Carcass Report” slug = XL555
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.2/reports/XL555"

def fetch() -> pd.DataFrame:
    # Calculate last Friday (ensures we always grab the latest full week)
    today = date.today()
    days_since_friday = (today.weekday() - 4) % 7
    last_friday = today - timedelta(days=days_since_friday)

    params = {
        "lastReports": 1,      # just the most recent report
        "allSections": True    # include every section’s table
    }

    # Simple GET—LMPR is open and JSON‑only, no key needed  
    resp = requests.get(BASE, params=params, timeout=30)
    resp.raise_for_status()
    report = resp.json().get("report", {})

    # Combine all rows from each section
    rows = []
    for section in report.get("reportSections", []):
        table = section.get("table", {})
        rows.extend(table.get("rows", []))

    # Flatten to DataFrame
    return pd.json_normalize(rows)
