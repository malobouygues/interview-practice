import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def trend_or_random_walk(y: pd.Series) -> dict:
    y = y.dropna()
    t = np.arange(len(y))

    # 1. linear trend fitted on the raw series (complete years: the seasons average out)
    slope, intercept = np.polyfit(t, y.to_numpy(dtype=float), 1)
    trend = intercept + slope * t

    # 2. deterministic seasonal profile = average deviation from trend, by calendar month
    profile = (y - trend).groupby(y.index.month).mean()
    deseasonalised = y - profile.reindex(y.index.month).to_numpy()

    # 3. ADF on the deseasonalised series, without and with a deterministic trend
    p_c = adfuller(deseasonalised, regression="c", autolag="AIC")[1]
    p_ct = adfuller(deseasonalised, regression="ct", autolag="AIC")[1]

    # 4. the two candidate remedies, compared on dispersion
    std_detrended = float((deseasonalised - trend).std())
    std_differenced = float(deseasonalised.diff().std())

    if p_c < 0.05:
        decision = "stationary"     # nothing to remove beyond the seasonal profile
    elif p_ct < 0.05:
        decision = "detrend"        # trend-stationary: shocks fade, remove the line
    else:
        decision = "difference"     # stochastic trend: shocks are permanent
    return {
        "trend_per_year": float(slope * 12),
        "seasonal_amplitude": float(profile.max() - profile.min()),
        "adf_p_c": float(p_c),
        "adf_p_ct": float(p_ct),
        "std_detrended": std_detrended,
        "std_differenced": std_differenced,
        "decision": decision,
    }
