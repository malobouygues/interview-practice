import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


def _block(log_brent, log_wti):
    spread = log_brent - log_wti                      # WTI discount to Brent, in log points
    rb, rw = log_brent.diff().dropna(), log_wti.diff().dropna()
    fit = sm.OLS(rw, sm.add_constant(rb)).fit()       # short-run link, on returns
    return {
        "n": int(len(log_brent)),
        "mean_spread": float(spread.mean()),
        "std_spread": float(spread.std()),
        "return_beta": float(fit.params.iloc[1]),
        "return_corr": float(rb.corr(rw)),
        "eg_pvalue": float(coint(log_wti, log_brent)[1]),
    }


def regime_comparison(prices: pd.DataFrame, break_date: str) -> dict:
    lb, lw = np.log(prices["brent"]), np.log(prices["wti"])
    before = prices.index < pd.Timestamp(break_date)
    return {
        "pre": _block(lb[before], lw[before]),
        "post": _block(lb[~before], lw[~before]),
        "full_eg_pvalue": float(coint(lw, lb)[1]),
    }
