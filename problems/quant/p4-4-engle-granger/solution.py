import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import coint


def relationship_by_period(prices, break_date="2016-01-01"):
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])
    prices = prices.set_index("date")
    logs = np.log(prices[["brent", "wti"]])
    # changes BEFORE splitting: the change across the break date belongs to the second period,
    # so the pooled and the separate regressions of the Chow test use exactly the same days
    logs["d_brent"] = logs["brent"].diff()
    logs["d_wti"] = logs["wti"].diff()

    periods = {"full sample": logs,
               "before " + break_date: logs[logs.index < break_date],
               "from " + break_date: logs[logs.index >= break_date]}

    rows = []
    ssr = {}
    for name, part in periods.items():
        # long run: Engle-Granger on log levels (economic link: transport and quality arbitrage)
        eg_stat, eg_p, eg_critical = coint(part["wti"], part["brent"])
        long_run = sm.OLS(part["wti"], sm.add_constant(part["brent"])).fit()
        # short run: daily pass-through of Brent returns to WTI returns
        changes = part.dropna()
        short_run = sm.OLS(changes["d_wti"], sm.add_constant(changes["d_brent"])).fit()
        ssr[name] = short_run.ssr
        spread = prices.loc[part.index, "brent"] - prices.loc[part.index, "wti"]
        rows.append({"period": name, "n_days": len(part),
                     "eg_stat": eg_stat, "eg_p": eg_p, "long_run_beta": long_run.params["brent"],
                     "mean_spread_usd": spread.mean(),
                     "pass_through": short_run.params["d_brent"], "pass_through_se": short_run.bse["d_brent"]})
    table = pd.DataFrame(rows).set_index("period")

    # Chow test at the known date, on the short-run regression (k = 2 coefficients)
    k = 2
    n = len(logs) - 1
    pooled = ssr["full sample"]
    separate = ssr["before " + break_date] + ssr["from " + break_date]
    chow_f = ((pooled - separate) / k) / (separate / (n - 2 * k))
    chow_p = stats.f.sf(chow_f, k, n - 2 * k)
    return {"periods": table, "chow_f": chow_f, "chow_p": chow_p}
