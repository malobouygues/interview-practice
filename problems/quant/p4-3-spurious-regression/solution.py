import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint


def spurious_check(prices):
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])
    logs = np.log(prices.set_index("date")[["brent", "wti", "coffee"]])
    changes = logs.diff().dropna()

    rows = []
    for partner in ["coffee", "brent"]:
        # levels: log WTI on log partner
        levels = sm.OLS(logs["wti"], sm.add_constant(logs[partner])).fit()
        # the residual of a levels regression tested with ORDINARY ADF p-values (the classic mistake)...
        naive_p = adfuller(levels.resid, regression="c", autolag="AIC")[1]
        # ...and with the Engle-Granger critical values that account for the estimated coefficient
        eg_stat, eg_p, eg_critical = coint(logs["wti"], logs[partner])
        rows.append({"pair": "wti ~ " + partner, "form": "log levels",
                     "coef": levels.params[partner], "t": levels.tvalues[partner], "r2": levels.rsquared,
                     "durbin_watson": sm.stats.durbin_watson(levels.resid),
                     "residual_adf_p_naive": naive_p, "engle_granger_p": eg_p})

        # daily changes: the same question on stationary data
        diffs = sm.OLS(changes["wti"], sm.add_constant(changes[partner])).fit()
        rows.append({"pair": "wti ~ " + partner, "form": "log changes",
                     "coef": diffs.params[partner], "t": diffs.tvalues[partner], "r2": diffs.rsquared,
                     "durbin_watson": sm.stats.durbin_watson(diffs.resid),
                     "residual_adf_p_naive": np.nan, "engle_granger_p": np.nan})
    return pd.DataFrame(rows)
