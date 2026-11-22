import numpy as np
import pandas as pd

FUNCTION = "trend_or_random_walk"


def demand():
    return pd.read_csv("data/p4_diesel_demand_monthly_synthetic.csv", parse_dates=["month"], index_col="month")["demand_kbd"]


def brent_monthly():
    prices = pd.read_csv("data/p4_crude_research_daily_synthetic.csv", parse_dates=["date"], index_col="date")
    return prices["brent"].resample("MS").mean()


MONTHS = pd.date_range("2010-01-01", periods=120, freq="MS")
WAVE = 30 * np.cos(2 * np.pi * (MONTHS.month - 1) / 12)

TESTS = [
    {"name": "Diesel demand -> detrend", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": demand()}},
    {"name": "Brent monthly average 2012-2019 -> difference", "origin": "extra",
     "args": lambda: {"y": brent_monthly()}},
    {"name": "Seasonal profile + white noise -> stationary", "origin": "extra",
     "args": lambda: {"y": pd.Series(WAVE + np.random.default_rng(7).normal(0, 10, 120), index=MONTHS)}},
    {"name": "Seasonal profile + random walk -> difference", "origin": "extra",
     "args": lambda: {"y": pd.Series(1000 + np.random.default_rng(3).normal(0, 15, 120).cumsum() + WAVE,
                                     index=MONTHS)}},
]
