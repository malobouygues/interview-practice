import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


def regime_comparison(prices: pd.DataFrame, break_date: str) -> dict:
    """{"pre": {...}, "post": {...}, "full_eg_pvalue": float}; each period: n, mean_spread,
    std_spread, return_beta, return_corr, eg_pvalue."""
    raise NotImplementedError("split at the break date and compare")
