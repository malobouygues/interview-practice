import pandas as pd

FUNCTION = "align_stocks"


def stocks():
    s = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
    s["week_ending"] = pd.to_datetime(s["week_ending"])
    s["available_at"] = pd.to_datetime(s["release_date"]) + pd.to_timedelta(s["release_time_et"] + ":00")
    return s


def hand():
    prices = pd.DataFrame({"date": ["2019-01-15", "2019-01-16", "2019-01-17", "2019-01-30"],
                           "wti_usd_bbl": [52.1, 52.3, 51.9, 54.0]})
    stocks = pd.DataFrame({"week_ending": pd.to_datetime(["2019-01-04", "2019-01-11"]),
                           "available_at": pd.to_datetime(["2019-01-09 10:30", "2019-01-16 10:30"]),
                           "crude_stocks_mbbl": [439.7, 437.1]})
    return {"prices": prices, "stocks": stocks}


def hand_expected():
    nat = pd.NaT
    return pd.DataFrame({"date": pd.to_datetime(["2019-01-15", "2019-01-16", "2019-01-17", "2019-01-30"]),
                         "wti_usd_bbl": [52.1, 52.3, 51.9, 54.0],
                         "week_ending": pd.to_datetime(["2019-01-04", "2019-01-11", "2019-01-11", nat]),
                         "available_at": pd.to_datetime(["2019-01-09 10:30", "2019-01-16 10:30", "2019-01-16 10:30", nat]),
                         "crude_stocks_mbbl": [439.7, 437.1, 437.1, float("nan")],
                         "age_days": [11.0, 5.0, 6.0, float("nan")]})


TESTS = [
    {"name": "Hand-made: before / after a 10:30 release, and a report too old (tolerance)", "origin": "extra",
     "args": hand, "expected": hand_expected},
    {"name": "Daily WTI and weekly stocks 2016-2019", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p3_wti_daily_synthetic.csv"), "stocks": stocks()}},
]
