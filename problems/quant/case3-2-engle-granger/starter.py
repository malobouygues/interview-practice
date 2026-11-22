import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint


def engle_granger(y: pd.Series, x: pd.Series) -> dict:
    """Engle-Granger by hand.

    Keys: alpha, beta, adf_stat, naive_pvalue, eg_pvalue, eg_crit_5pct, cointegrated.
    """
    raise NotImplementedError("step 1: OLS in levels; step 2: unit-root test on the residuals")
