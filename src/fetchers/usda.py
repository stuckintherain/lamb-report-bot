import requests, pandas as pd

BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports/XL555/details?lastDays=10"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LambBot/1.0; +https://github.com/stuckintherain/lamb-report-bot)"
}

def fetch() -> pd.DataFrame:
    resp = requests.get(BASE, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    tables = resp.json()["report"].get("reportTables", [])
    if not tables:
        return pd.DataFrame()
    return pd.json_normalize(tables[0]["table"]["rows"])
