import pandas as pd

FUNCTION = "add_availability"


def raw():
    return pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")


def hand():
    return pd.DataFrame({"week_ending": ["2019-01-11", "2019-01-18"],
                         "release_date": ["2019-01-16", "2019-01-24"],
                         "release_time_et": ["10:30", "10:30"],
                         "crude_stocks_mbbl": [437.1, 445.0],
                         "ingested_at": ["2019-01-16 16:05", "2019-02-20 09:00"]})


def hand_expected():
    return pd.DataFrame({"week_ending": pd.to_datetime(["2019-01-11", "2019-01-18"]),
                         "crude_stocks_mbbl": [437.1, 445.0],
                         "release_date": pd.to_datetime(["2019-01-16", "2019-01-24"]),
                         "available_at": pd.to_datetime(["2019-01-16 10:30", "2019-01-24 10:30"]),
                         "ingested_at": pd.to_datetime(["2019-01-16 16:05", "2019-02-20 09:00"]),
                         "publication_lag_days": [5, 6],
                         "backfilled": [False, True]})


TESTS = [
    {"name": "Two weeks: a normal release, a holiday-delayed release loaded late", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"stocks": hand()}, "expected": hand_expected},
    {"name": "Weekly US crude stocks 2016-2019", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"stocks": raw()}},
]
