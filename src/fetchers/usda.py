import requests
import pandas as pd

BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports/XL555/details?lastDays=10"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://mpr.datamart.ams.usda.gov/",
    "Origin": "https://mpr.datamart.ams.usda.gov",
}

def fetch() -> pd.DataFrame:
    resp = requests.get(BASE, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    tables = resp.json()["report"].get("reportTables", [])
    if not tables:
        return pd.DataFrame()
    return pd.json_normalize(tables[0]["table"]["rows"])
