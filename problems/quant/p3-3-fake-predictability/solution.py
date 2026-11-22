import numpy as np
import pandas as pd


def predictive_correlation(prices: pd.DataFrame, stocks: pd.DataFrame, align_on: str) -> dict:
    # signal: the weekly change in US crude stocks (million barrels)
    stocks = stocks.sort_values("week_ending").copy()
    stocks["stock_change"] = stocks["crude_stocks_mbbl"].diff()
    stocks = stocks.dropna(subset=["stock_change"])

    # outcome: WTI log return over the NEXT 5 trading days, starting at the settlement of day t
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])
    prices = prices.sort_values("date")
    prices["decision_time"] = prices["date"] + pd.Timedelta(hours=14, minutes=30)
    log_price = np.log(prices["wti_usd_bbl"])
    prices["next_5d_return"] = log_price.shift(-5) - log_price      # the future on purpose: it is the outcome

    # attach to each day the latest stock change "known" at the decision time, according to align_on
    signal = stocks[[align_on, "stock_change"]].sort_values(align_on)
    data = pd.merge_asof(prices, signal, left_on="decision_time", right_on=align_on, direction="backward")
    data = data.dropna(subset=["stock_change", "next_5d_return"])

    return {"n": int(len(data)), "corr": float(data["stock_change"].corr(data["next_5d_return"]))}
