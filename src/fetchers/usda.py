import requests, pandas as pd

BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports/XL555/details?lastDays=10"

def fetch() -> pd.DataFrame:
    resp = requests.get(BASE, timeout=30)
    resp.raise_for_status()
    tables = resp.json()["report"].get("reportTables", [])
    if not tables:
        return pd.DataFrame()
    return pd.json_normalize(tables[0]["table"]["rows"])
