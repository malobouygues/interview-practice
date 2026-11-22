import pandas as pd
from statsmodels.tsa.stattools import adfuller


def adf_report(x: pd.Series, regression: str = "c") -> dict:
    # H0: unit root (non-stationary).  H1: stationary around 0 ('n'), a level ('c') or a trend ('ct').
    # autolag="AIC": the number of lagged differences is chosen to clean the residuals
    stat, pvalue, lags, nobs, critical_values, icbest = adfuller(x.dropna(), regression=regression, autolag="AIC")

    return {
        "stat": float(stat),
        "pvalue": float(pvalue),
        "lags": int(lags),
        "nobs": int(nobs),
        "crit_5pct": float(critical_values["5%"]),     # reject H0 at 5 % when stat < crit_5pct
        "reject_unit_root": bool(pvalue < 0.05),
    }
