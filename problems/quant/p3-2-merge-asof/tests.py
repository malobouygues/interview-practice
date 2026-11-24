import pandas as pd

FUNCTION = "align_stocks"


def stocks():
    s = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
    s["week_ending"] = pd.to_datetime(s["week_ending"])
    release = pd.to_datetime(s["release_date"] + " " + s["release_time_et"])
    s["available_at"] = release.dt.tz_localize("America/New_York").dt.tz_convert("UTC")
    s = s.sort_values("week_ending")
    s["surprise_mbbl"] = s["crude_stocks_mbbl"].diff() - s["consensus_change_mbbl"]
    return s


def hand_made():
    prices = pd.DataFrame({"date": ["2022-06-21", "2022-06-22", "2022-06-28", "2022-06-29", "2022-07-12"],
                           "wti_settle_usd_bbl": [110.0, 106.2, 111.8, 109.8, 95.8]})
    s = pd.DataFrame({"week_ending": pd.to_datetime(["2022-06-10", "2022-06-17"]),
                      "available_at": pd.to_datetime(["2022-06-15 14:30", "2022-06-29 14:30"]).tz_localize("UTC"),
                      "crude_stocks_mbbl": [418.7, 415.6], "surprise_mbbl": [1.2, -2.6]})
    return {"prices": prices, "stocks": s}


TESTS = [
    {"name": "Hand-made: a late release, the same-day release before the settlement, a report too old",
     "origin": "extra", "args": hand_made},
    {"name": "Daily WTI and weekly stocks 2019-2024", "origin": "extra",
     "args": lambda: {"prices": pd.read_csv("data/p3_wti_daily_synthetic.csv"), "stocks": stocks()}},
]
