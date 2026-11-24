import numpy as np
import pandas as pd

prices = pd.read_csv("data/p3_wti_daily_synthetic.csv", parse_dates=["date"], index_col="date")


def leaky_features(prices):
    price = prices["wti_usd_bbl"]
    returns = np.log(price).diff()
    features = pd.DataFrame(index=prices.index)
    features["ma_5_centered"] = price.rolling(5, center=True).mean()           # uses t+1 and t+2
    features["zscore_full_sample"] = (returns - returns.mean()) / returns.std()  # mean/std of all years
    features["share_of_max"] = price / price.max()                              # max of the whole sample
    features["return_tomorrow"] = returns.shift(-1)                             # tomorrow's return
    features["return_lag1"] = returns.shift(1)                                  # fine
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


for name, builder in [("leaky", leaky_features), ("fixed", fixed_features)]:
    print(name, "->", truncation_test(builder, prices, "2017-12-29"))
