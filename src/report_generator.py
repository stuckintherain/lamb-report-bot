import datetime as dt, pathlib, pandas as pd
from jinja2 import Template

from fetchers import usda, mla, blnz
from summariser import summarise

BASE = pathlib.Path(__file__).parent

def main():
    today = dt.date.today().strftime("%d %b %Y")

    us = usda.fetch()
    au = mla.fetch()
    nz = blnz.fetch()

    us_txt = summarise(f"Summarise latest U.S. lamb prices (table):\\n{us.head().to_markdown()}")
    au_txt = summarise(f"Summarise latest AU ESTLI prices (table):\\n{au.head().to_markdown()}")
    nz_txt = summarise(f"Summarise latest NZ slaughter figures (table):\\n{nz.to_markdown()}")
    cross  = summarise("Given the AU & NZ trends above and a strong USD, what may happen to U.S. import lamb prices in the next month?")

    template = Template((BASE / "template.md.j2").read_text())
    markdown = template.render(
        date=today,
        us_section=us_txt,
        au_section=au_txt,
        nz_section=nz_txt,
        outlook_section="(Add longer-range forecasts here later)",
        cross_section=cross,
    )

    (BASE.parent / "weekly_report.md").write_text(markdown)
    print("✓ Report ready: weekly_report.md")

if __name__ == "__main__":
    main()
