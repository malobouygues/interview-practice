import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_ecm(y: pd.Series, x: pd.Series) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]

    # Step 1: long-run relation y = a + beta * x; its residual is the error-correction term
    longrun = sm.OLS(data["y"], sm.add_constant(data["x"])).fit()
    ect = longrun.resid

    # Step 2: dy_t = c + alpha * ect_{t-1} + gamma * dx_t + e_t
    frame = pd.DataFrame({"dy": data["y"].diff(), "ect_lag": ect.shift(1),
                          "dx": data["x"].diff()}).dropna()
    ecm = sm.OLS(frame["dy"], sm.add_constant(frame[["ect_lag", "dx"]])).fit()
    alpha = float(ecm.params["ect_lag"])
    half_life = float(np.log(0.5) / np.log(1 + alpha)) if -1 < alpha < 0 else None
    return {
        "beta_long_run": float(longrun.params.iloc[1]),
        "alpha": alpha,                                  # speed of adjustment (< 0 expected)
        "alpha_tstat": float(ecm.tvalues["ect_lag"]),
        "gamma": float(ecm.params["dx"]),                # short-run pass-through
        "half_life": half_life,                          # periods to close half of a gap
        "n": int(ecm.nobs),
    }
