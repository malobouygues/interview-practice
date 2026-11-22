import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint


def engle_granger(y: pd.Series, x: pd.Series) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    yy, xx = data.iloc[:, 0], data.iloc[:, 1]

    # Step 1: long-run (cointegrating) regression in levels
    step1 = sm.OLS(yy, sm.add_constant(xx)).fit()
    resid = step1.resid                                   # deviation from the long-run relation

    # Step 2: unit-root test on the residuals (mean zero by construction -> no constant)
    adf_stat, naive_p = adfuller(resid, regression="n", autolag="AIC")[:2]

    # Same statistic, but judged against Engle-Granger critical values (beta was estimated)
    _stat, eg_p, crit = coint(yy, xx, trend="c", autolag="aic")
    return {
        "alpha": float(step1.params.iloc[0]),
        "beta": float(step1.params.iloc[1]),
        "adf_stat": float(adf_stat),
        "naive_pvalue": float(naive_p),       # WRONG reference distribution, too optimistic
        "eg_pvalue": float(eg_p),             # correct p-value for an estimated residual
        "eg_crit_5pct": float(crit[1]),
        "cointegrated": bool(eg_p < 0.05),
    }
