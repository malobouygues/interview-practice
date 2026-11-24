import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


def describe_period(log_brent: pd.Series, log_wti: pd.Series) -> dict:
    spread = log_brent - log_wti                       # WTI discount to Brent, in log points
    brent_returns = log_brent.diff().dropna()
    wti_returns = log_wti.diff().dropna()
    short_run = sm.OLS(wti_returns, sm.add_constant(brent_returns)).fit()

    return {
        "n": int(len(log_brent)),
        "mean_spread": float(spread.mean()),
        "std_spread": float(spread.std()),
        "return_beta": float(short_run.params.iloc[1]),
        "return_corr": float(brent_returns.corr(wti_returns)),
        "eg_pvalue": float(coint(log_wti, log_brent)[1]),
    }


def regime_comparison(prices: pd.DataFrame, break_date: str) -> dict:
    log_brent = np.log(prices["brent"])
    log_wti = np.log(prices["wti"])
    before = prices.index < pd.Timestamp(break_date)

    return {
        "pre": describe_period(log_brent[before], log_wti[before]),
        "post": describe_period(log_brent[~before], log_wti[~before]),
        "full_eg_pvalue": float(coint(log_wti, log_brent)[1]),
    }
