import requests, pandas as pd

URL = "https://api.mla.com.au/prices/list?seriesIds=2133&timeFrame=10"
HEADERS = {"Accept": "application/json"}

def fetch() -> pd.DataFrame:
    data = requests.get(URL, headers=HEADERS, timeout=30).json()
    return pd.DataFrame(data["seriesData"])
