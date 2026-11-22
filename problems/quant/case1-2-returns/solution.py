import numpy as np
import pandas as pd


def make_returns(prices: pd.Series) -> pd.DataFrame:
    if (prices.dropna() <= 0).any():
        # log(p) is undefined for p <= 0: a spread or a negative print needs diff(), not log returns
        raise ValueError("log returns need strictly positive prices; use diff() for this series")
    return pd.DataFrame({
        "price": prices,
        "diff": prices.diff(),                 # change in price units (EUR/MWh)
        "pct_change": prices.pct_change(),     # simple return: readable, not additive over time
        "log_return": np.log(prices).diff(),   # additive over time: sum = log(P_end / P_start)
    }, index=prices.index)
