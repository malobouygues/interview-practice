import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, adfuller


def stationarity_table(prices, demand):
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])
    log_brent = np.log(prices.set_index("date")["brent"])
    brent_returns = log_brent.diff().dropna()

    demand = demand.copy()
    demand["month"] = pd.to_datetime(demand["month"])
    level = demand.set_index("month")["demand_kbd"]

    # remove a deterministic trend and a fixed monthly pattern with one OLS (trend + 11 month dummies)
    design = pd.get_dummies(level.index.month, prefix="m", drop_first=True, dtype=float)
    design.index = level.index
    design["trend"] = np.arange(len(level), dtype=float)
    detrended = sm.OLS(level, sm.add_constant(design)).fit().resid

    # each candidate: (series, transformation, deterministic terms justified by the picture, lag for the ACF)
    candidates = [
        ("brent", "log level", log_brent, "c", 20),
        ("brent", "log level", log_brent, "ct", 20),
        ("brent", "log return", brent_returns, "n", 20),
        ("diesel demand", "level", level, "c", 12),
        ("diesel demand", "level", level, "ct", 12),
        ("diesel demand", "first difference", level.diff().dropna(), "c", 12),
        ("diesel demand", "seasonal difference (12)", level.diff(12).dropna(), "c", 12),
        ("diesel demand", "detrended and deseasonalised", detrended, "n", 12),
    ]

    rows = []
    for name, transformation, series, regression, long_lag in candidates:
        statistic, p_value, lags_used, n_obs, critical, icbest = adfuller(series, regression=regression, autolag="AIC")
        correlations = acf(series, nlags=long_lag)
        rows.append({"series": name, "transformation": transformation, "regression": regression,
                     "adf_stat": statistic, "p_value": p_value, "lags_used": lags_used, "n_obs": n_obs,
                     "acf_1": correlations[1], "acf_long": correlations[long_lag], "long_lag": long_lag})
    return pd.DataFrame(rows)
