import numpy as np
import pandas as pd

FUNCTION = "truncation_test"


def prices():
    return pd.read_csv("data/p3_wti_daily_synthetic.csv", parse_dates=["date"], index_col="date")


def leaky_features(prices):
    price = prices["wti_usd_bbl"]
    returns = np.log(price).diff()
    features = pd.DataFrame(index=prices.index)
    features["ma_5_centered"] = price.rolling(5, center=True).mean()
    features["zscore_full_sample"] = (returns - returns.mean()) / returns.std()
    features["share_of_max"] = price / price.max()
    features["return_tomorrow"] = returns.shift(-1)
    features["return_lag1"] = returns.shift(1)
    return features


def fixed_features(prices):
    price = prices["wti_usd_bbl"]
    returns = np.log(price).diff()
    features = pd.DataFrame(index=prices.index)
    features["ma_5_past"] = price.rolling(5).mean().shift(1)
    past_mean = returns.expanding(60).mean().shift(1)
    past_std = returns.expanding(60).std().shift(1)
    features["zscore_past"] = (returns - past_mean) / past_std
    features["share_of_running_max"] = price.shift(1) / price.shift(1).cummax()
    features["return_lag1"] = returns.shift(1)
    return features


TESTS = [
    {"name": "Leaky builder, cutoff 2017-12-29 (before the 2018 high)", "origin": "extra",
     "args": lambda: {"build_features": leaky_features, "prices": prices(), "cutoff": "2017-12-29"},
     "expected": ["ma_5_centered", "zscore_full_sample", "share_of_max", "return_tomorrow"]},
    {"name": "Leaky builder, cutoff 2019-06-28 (after the high: share_of_max no longer moves)", "origin": "extra",
     "args": lambda: {"build_features": leaky_features, "prices": prices(), "cutoff": "2019-06-28"},
     "expected": ["ma_5_centered", "zscore_full_sample", "return_tomorrow"]},
    {"name": "Corrected builder: nothing changes", "origin": "extra",
     "args": lambda: {"build_features": fixed_features, "prices": prices(), "cutoff": "2017-12-29"},
     "expected": []},
]
