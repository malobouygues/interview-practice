import pandas as pd

crude = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
print(crude.describe())

for a, b in [("brent", "wti"), ("brent", "coffee"), ("wti", "coffee")]:
    report = correlation_report(crude, a, b)
    print(f"{a:6s} / {b:6s}", {k: round(v, 3) for k, v in report.items()})
