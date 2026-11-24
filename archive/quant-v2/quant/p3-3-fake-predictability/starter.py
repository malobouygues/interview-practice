import numpy as np
import pandas as pd


def predictive_correlation(prices: pd.DataFrame, stocks: pd.DataFrame, align_on: str) -> dict:
    """{"n": ..., "corr": corr(latest known stock change, next 5-day WTI log return)}."""
    raise NotImplementedError("signal, outcome, as-of join on the chosen key")
