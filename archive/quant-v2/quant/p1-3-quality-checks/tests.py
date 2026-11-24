import pandas as pd

FUNCTION = "quality_checks"


def loaded():
    raw = pd.read_csv("data/p1_crude_prices_vendor_synthetic.csv", na_values=["HOL", "-"])
    raw.columns = ["date", "brent", "wti", "dubai", "loaded_at"]
    raw["date"] = pd.to_datetime(raw["date"], format="%d/%m/%Y")
    raw["loaded_at"] = pd.to_datetime(raw["loaded_at"])
    prices = raw.drop_duplicates().sort_values(["date", "loaded_at"])
    prices = prices.drop_duplicates(subset="date", keep="last").set_index("date")
    return prices[["brent", "wti", "dubai"]]


def small():
    index = pd.bdate_range("2020-01-01", periods=9)
    nan = float("nan")
    return pd.DataFrame({"brent": [60.0, 61.0, 60.5, 61.2, 6.12, 61.0, 61.4, 0.0, 61.1],
                         "wti": [55.0, 56.0, -1.5, 56.2, 56.0, 55.8, 56.1, 56.0, 55.9],
                         "dubai": [59.0, 59.5, 59.2, nan, 59.9, 140.0, 60.1, 60.2, 59.8]}, index=index)


TESTS = [
    {"name": "Small frame: a /10 print, a x2.3 print, a zero, a negative WTI", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"prices": small()}},
    {"name": "The loaded vendor file: one error, one genuine event", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"prices": loaded()}},
]
