import pandas as pd

FUNCTION = "as_of"


def vintages():
    return pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv")


def hand():
    return pd.DataFrame({"obs_month": ["2020-01", "2020-01", "2020-02", "2020-01", "2020-02"],
                         "vintage_date": ["2020-03-31", "2020-04-30", "2020-04-30", "2021-08-31", "2021-08-31"],
                         "demand_kbd": [100.0, 104.0, 98.0, 106.0, 101.0]})


def hand_expected():
    index = pd.to_datetime(["2020-01-01", "2020-02-01"])
    index.name = "obs_month"
    return pd.Series([104.0, 98.0], index=index, name="demand_kbd")


TESTS = [
    {"name": "Hand-made: as of 2020-05-15 (second estimate of Jan, first of Feb)", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"vintages": hand(), "as_of_date": "2020-05-15"},
     "expected": hand_expected},
    {"name": "As of 2016-06-15", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"vintages": vintages(), "as_of_date": "2016-06-15"}},
    {"name": "As of 2017-09-15 (after an annual revision)", "origin": "extra",
     "args": lambda: {"vintages": vintages(), "as_of_date": "2017-09-15"}},
    {"name": "Today: the latest revised history", "origin": "extra",
     "args": lambda: {"vintages": vintages(), "as_of_date": "2030-01-01"}},
]
