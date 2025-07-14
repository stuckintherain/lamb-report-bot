import pandas as pd

CSV = "https://beeflambnz.com/sites/default/files/lamb-slaughter-progress.csv"

def fetch() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    return df.tail(4)
