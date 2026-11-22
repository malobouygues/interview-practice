import numpy as np
import pandas as pd


def make_returns(prices: pd.Series) -> pd.DataFrame:
    # returns are measured between consecutive OBSERVED prices: a holiday is not a zero return
    prices = prices.dropna()

    # a log return needs strictly positive prices: refuse a series that has any price <= 0
    if (prices <= 0).any():
        raise ValueError("log returns need strictly positive prices: use diff() for this series")

    table = pd.DataFrame(index=prices.index)
    table["price"] = prices
    table["diff"] = prices.diff()                    # change in USD/bbl
    table["pct_change"] = prices.pct_change()        # simple return: readable, not additive over time
    table["log_return"] = np.log(prices).diff()      # additive over time
    return table
