import pandas as pd

url = "https://www.ams.usda.gov/mnreports/lm_xl555.txt"

df = pd.read_csv(url, delimiter="|", skip_blank_lines=True, engine="python")
print(df.head())
