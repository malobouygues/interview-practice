import numpy as np
import pandas as pd

FUNCTION = "trend_or_random_walk"


def demand():
    return pd.read_csv("data/diesel_demand_monthly_synthetic.csv",
                       parse_dates=["month"], index_col="month")["demand_kbd"]


def ttf_monthly():
    ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
    return ttf.resample("MS").mean()


MONTHS = pd.date_range("2010-01-01", periods=120, freq="MS")
WAVE = 30 * np.cos(2 * np.pi * (MONTHS.month - 1) / 12)


TESTS = [
    {"name": "Diesel demand -> detrend (trend-stationary)", "origin": "extra", "check_no_mutation": True,
     "args": lambda: {"y": demand()}},
    {"name": "TTF monthly average -> difference (stochastic trend)", "origin": "extra",
     "args": lambda: {"y": ttf_monthly()}},
    {"name": "Seasonal profile + white noise -> stationary", "origin": "extra",
     "args": lambda: {"y": pd.Series(WAVE + np.random.default_rng(7).normal(0, 10, 120), index=MONTHS)}},
    {"name": "Seasonal profile + random walk -> difference", "origin": "extra",
     "args": lambda: {"y": pd.Series(1000 + np.random.default_rng(3).normal(0, 15, 120).cumsum() + WAVE,
                                     index=MONTHS)}},
]
