import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_ecm(y: pd.Series, x: pd.Series) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]

    # Step 1: long-run relation y = a + beta * x; its residual is the deviation from equilibrium
    long_run = sm.OLS(data["y"], sm.add_constant(data["x"])).fit()
    deviation = long_run.resid

    # Step 2: dy_t = c + alpha * deviation_{t-1} + gamma * dx_t + e_t
    ecm_data = pd.DataFrame(index=data.index)
    ecm_data["dy"] = data["y"].diff()
    ecm_data["deviation_lag"] = deviation.shift(1)      # YESTERDAY's gap explains today's change
    ecm_data["dx"] = data["x"].diff()
    ecm_data = ecm_data.dropna()

    ecm = sm.OLS(ecm_data["dy"], sm.add_constant(ecm_data[["deviation_lag", "dx"]])).fit()
    alpha = float(ecm.params["deviation_lag"])

    # half-life of a deviation: (1 + alpha)^k = 0.5, only meaningful for -1 < alpha < 0
    half_life = None
    if -1 < alpha < 0:
        half_life = float(np.log(0.5) / np.log(1 + alpha))

    return {
        "beta_long_run": float(long_run.params["x"]),
        "alpha": alpha,
        "alpha_tstat": float(ecm.tvalues["deviation_lag"]),
        "gamma": float(ecm.params["dx"]),
        "half_life": half_life,
        "n": int(ecm.nobs),
    }
