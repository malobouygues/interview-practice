import pandas as pd

FUNCTION = "realtime_growth"


def vintages():
    return pd.read_csv("data/p3_us_oil_demand_vintages_synthetic.csv")


TESTS = [
    {"name": "Three month-ends in 2016", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"vintages": vintages(), "decision_dates": ["2016-03-31", "2016-06-30", "2016-09-30"]}},
    {"name": "Every month-end 2016-2019", "origin": "extra",
     "args": lambda: {"vintages": vintages(),
                      "decision_dates": list(pd.date_range("2016-03-31", "2019-12-31", freq="ME"))}},
]
