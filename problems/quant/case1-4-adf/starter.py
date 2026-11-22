import pandas as pd
from statsmodels.tsa.stattools import adfuller


def adf_report(x: pd.Series, regression: str = "c") -> dict:
    """ADF test summary: stat, pvalue, lags, nobs, crit_5pct, reject_unit_root."""
    raise NotImplementedError("run adfuller and report")
