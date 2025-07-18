import requests
import pandas as pd
from datetime import date, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LMPRS_ENDPOINT = "https://mpr.datamart.ams.usda.gov/services/v1.2/reports/XL555"

def fetch() -> pd.DataFrame:
    # Figure out last Friday
    today = date.today()
    last_friday = today - timedelta(days=(today.weekday() - 4) % 7)

    params = {"lastReports": 1, "allSections": True}

    # Build a session that retries on network hiccups
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))

    try:
        resp = session.get(LMPRS_ENDPOINT, params=params, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        print(f"⚠️  USDA fetch failed: {e}")
        return pd.DataFrame()  # return empty so the rest of the script still runs

    report = resp.json().get("report", {})
    rows = []
    for section in report.get("reportSections", []):
        rows.extend(section.get("table", {}).get("rows", []))

    return pd.json_normalize(rows)
