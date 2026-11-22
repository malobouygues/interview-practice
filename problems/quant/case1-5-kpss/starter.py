import warnings

import pandas as pd
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.stattools import adfuller, kpss


def stationarity_verdict(x: pd.Series, regression: str = "c", alpha: float = 0.05) -> dict:
    """ADF + KPSS with the same specification.

    Returns adf_pvalue, kpss_pvalue, adf_rejects, kpss_rejects and a verdict among
    "stationary", "unit root", "conflict", "inconclusive".
    """
    raise NotImplementedError("run both tests and combine them")
