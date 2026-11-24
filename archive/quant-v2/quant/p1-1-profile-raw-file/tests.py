import pandas as pd

FUNCTION = "profile_raw_file"


def raw_file():
    return pd.read_csv("data/p1_crude_prices_vendor_synthetic.csv")


def small_file():
    return pd.DataFrame({
        "Date": ["02/01/2020", "03/01/2020", "03/01/2020", "06/01/2020", "06/01/2020", "05/01/2020"],
        "Brent (USD/bbl)": ["66.25", "68.60", "68.60", "HOL", "68.91", "68.10"],
        "WTI (USD/bbl)": ["61.18", "-", "-", "63.27", "63.27", "62.70"],
        "Dubai (USD/bbl)": ["65.10", "67.02", "67.02", "67.30", "67.30", "66.80"],
        "loaded_at": ["2020-02-03 06:00", "2020-02-03 06:00", "2020-02-03 06:00",
                      "2020-02-03 06:00", "2020-02-12 06:00", "2020-02-03 06:00"]})


TESTS = [
    {"name": "Small file: one identical row, one correction, codes, unsorted", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"raw": small_file()}},
    {"name": "The vendor file", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"raw": raw_file()}},
]
