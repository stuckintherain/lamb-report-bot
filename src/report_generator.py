# src/report_generator.py
from datetime import date, timedelta
from dotenv import load_dotenv
import pandas as pd
import requests
from summariser import summarise

load_dotenv()

def fetch_usda() -> pd.DataFrame:
    TXT_URL = "https://www.ams.usda.gov/mnreports/lm_xl555.txt"
    resp = requests.get(TXT_URL, timeout=15)
    resp.raise_for_status()
    df = pd.read_fwf(pd.io.common.StringIO(resp.text), skiprows=6)
    return df.dropna(how="all")

def main():
    # 1) Fetch data
    df = fetch_usda()
    print("✅ Fetched U.S. data, rows:", len(df))

    # 2) Summarise
    prompt = (
        "Write a concise weekly market report for U.S. lamb carcass prices, "
        "based on this table:\n\n" + df.head().to_string()
    )
    summary = summarise(prompt)

    # 3) Write Markdown
    today = date.today().isoformat()
    with open("weekly_report.md", "w", encoding="utf-8") as f:
        f.write(f"# Weekly U.S. Lamb Carcass Report — {today}\n\n")
        f.write(summary + "\n")

    print("✓ Report written to weekly_report.md")

if __name__ == "__main__":
    main()

