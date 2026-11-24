import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint


def engle_granger(y: pd.Series, x: pd.Series) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]

    # Step 1: long-run (cointegrating) regression in levels
    step1 = sm.OLS(data["y"], sm.add_constant(data["x"])).fit()
    residuals = step1.resid                              # deviation from the long-run relation

    # Step 2: unit-root test on the residuals (mean zero by construction -> no constant)
    adf_stat, naive_pvalue = adfuller(residuals, regression="n", autolag="AIC")[:2]

    # the same statistic judged against Engle-Granger critical values (beta was estimated)
    eg_stat, eg_pvalue, critical_values = coint(data["y"], data["x"], trend="c", autolag="aic")

    return {
        "alpha": float(step1.params["const"]),
        "beta": float(step1.params["x"]),
        "adf_stat": float(adf_stat),
        "naive_pvalue": float(naive_pvalue),             # WRONG reference distribution, too optimistic
        "eg_pvalue": float(eg_pvalue),                   # correct p-value for an estimated residual
        "eg_crit_5pct": float(critical_values[1]),
        "cointegrated": bool(eg_pvalue < 0.05),
    }
