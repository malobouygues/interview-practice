import pandas as pd

FUNCTION = "monthly_spreads_sql"


def clean():
    return pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")


def small():
    index = pd.to_datetime(["2020-01-30", "2020-01-31", "2020-02-03", "2020-02-04"])
    nan = float("nan")
    return pd.DataFrame({"brent": [60.0, 62.0, 55.0, 54.0],
                         "wti": [56.0, 57.0, nan, 50.0],
                         "dubai": [59.0, 61.0, 54.0, 53.5]}, index=index)


TESTS = [
    {"name": "Small frame: a missing WTI day is excluded", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": small()},
     "expected": lambda: pd.DataFrame({"month": ["2020-01", "2020-02"], "brent_wti": [4.5, 4.0],
                                       "brent_dubai": [1.0, 0.5], "n_days": [2, 1]})},
    {"name": "Clean crude prices 2019-2021", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"prices": clean()}},
]
