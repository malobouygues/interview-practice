import warnings

import pandas as pd
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.stattools import adfuller, kpss

VERDICTS = {
    (True, False): "stationary",    # ADF rejects a unit root, KPSS does not reject stationarity
    (False, True): "unit root",     # ADF cannot reject a unit root, KPSS rejects stationarity
    (True, True): "conflict",       # both reject: trend misspecified, break, changing variance, long memory
    (False, False): "inconclusive", # neither rejects: not enough information (short sample, low power)
}


def stationarity_verdict(x: pd.Series, regression: str = "c", alpha: float = 0.05) -> dict:
    x = x.dropna()
    adf_p = adfuller(x, regression=regression, autolag="AIC")[1]
    with warnings.catch_warnings():
        # statsmodels only tabulates KPSS p-values between 0.01 and 0.10 and warns outside
        warnings.simplefilter("ignore", InterpolationWarning)
        kpss_p = kpss(x, regression=regression, nlags="auto")[1]
    adf_rejects, kpss_rejects = bool(adf_p < alpha), bool(kpss_p < alpha)
    return {
        "adf_pvalue": float(adf_p),
        "kpss_pvalue": float(kpss_p),
        "adf_rejects": adf_rejects,
        "kpss_rejects": kpss_rejects,
        "verdict": VERDICTS[(adf_rejects, kpss_rejects)],
    }
