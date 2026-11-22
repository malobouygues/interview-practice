import pandas as pd

raw = pd.read_csv("data/p1_crude_prices_vendor_synthetic.csv")   # no options on purpose
print(raw.head())
print(raw.info())

report = profile_raw_file(raw)
for key, value in report.items():
    print(f"{key:22s} {value}")
