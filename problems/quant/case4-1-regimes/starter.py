import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


def regime_comparison(prices: pd.DataFrame, break_date: str) -> dict:
    """Spread level / volatility, short-run link and cointegration, before and after a date.

    Returns {"pre": {...}, "post": {...}, "full_eg_pvalue": float}; each period dict has
    n, mean_spread, std_spread, return_beta, return_corr, eg_pvalue.
    """
    raise NotImplementedError("split at the break date and compare")
