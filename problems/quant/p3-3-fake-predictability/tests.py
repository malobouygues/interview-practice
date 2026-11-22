import pandas as pd

FUNCTION = "predictive_correlation"


def stocks():
    s = pd.read_csv("data/p3_us_crude_stocks_weekly_synthetic.csv")
    s["week_ending"] = pd.to_datetime(s["week_ending"])
    s["release_date"] = pd.to_datetime(s["release_date"])
    s["available_at"] = s["release_date"] + pd.to_timedelta(s["release_time_et"] + ":00")
    s["ingested_at"] = pd.to_datetime(s["ingested_at"])
    return s


def prices():
    return pd.read_csv("data/p3_wti_daily_synthetic.csv")


TESTS = [
    {"name": "Aligned on week_ending (look-ahead): a negative 'signal'", "origin": "extra",
     "check_no_mutation": True, "args": lambda: {"prices": prices(), "stocks": stocks(), "align_on": "week_ending"}},
    {"name": "Aligned on available_at: nothing left", "origin": "extra",
     "args": lambda: {"prices": prices(), "stocks": stocks(), "align_on": "available_at"}},
    {"name": "Aligned on ingested_at (backfilled history)", "origin": "extra",
     "args": lambda: {"prices": prices(), "stocks": stocks(), "align_on": "ingested_at"}},
]
