import pandas as pd

FUNCTION = "load_crude_prices"

SMALL = """Date,Brent (USD/bbl),WTI (USD/bbl),Dubai (USD/bbl),loaded_at
02/01/2020,66.25,61.18,65.10,2020-02-03 06:00
06/01/2020,68.91,62.00,67.30,2020-02-03 06:00
03/01/2020,68.60,-,67.02,2020-02-03 06:00
03/01/2020,68.60,-,67.02,2020-02-03 06:00
06/01/2020,68.91,63.27,67.30,2020-02-12 06:00
01/01/2020,HOL,HOL,HOL,2020-02-03 06:00
"""


def small_path():
    with open("data/small_vendor.csv", "w") as f:
        f.write(SMALL)
    return {"path": "data/small_vendor.csv"}


def small_expected():
    index = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-06"])
    index.name = "date"
    nan = float("nan")
    return pd.DataFrame({"brent": [nan, 66.25, 68.60, 68.91],
                         "wti": [nan, 61.18, nan, 63.27],
                         "dubai": [nan, 65.10, 67.02, 67.30]}, index=index)


TESTS = [
    {"name": "Small file: codes, identical row, correction (latest load wins), order", "origin": "extra",
     "args": small_path, "expected": small_expected},
    {"name": "The vendor file", "origin": "extra",
     "args": lambda: {"path": "data/p1_crude_prices_vendor_synthetic.csv"}},
]
