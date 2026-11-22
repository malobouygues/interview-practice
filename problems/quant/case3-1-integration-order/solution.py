import warnings

import pandas as pd
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.stattools import adfuller, kpss


def _verdict(x, alpha=0.05):
    adf_rejects = adfuller(x, regression="c", autolag="AIC")[1] < alpha
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InterpolationWarning)
        kpss_rejects = kpss(x, regression="c", nlags="auto")[1] < alpha
    return {(True, False): "stationary", (False, True): "unit root",
            (True, True): "conflict", (False, False): "inconclusive"}[(adf_rejects, kpss_rejects)]


def integration_order(x: pd.Series, max_order: int = 2) -> dict:
    x = x.dropna()
    verdicts = []
    for d in range(max_order + 1):
        v = _verdict(x)
        verdicts.append(v)
        if v == "stationary":
            return {"order": d, "verdicts": verdicts}   # I(d): stationary after d differences
        x = x.diff().dropna()
    return {"order": None, "verdicts": verdicts}         # not settled within max_order differences
