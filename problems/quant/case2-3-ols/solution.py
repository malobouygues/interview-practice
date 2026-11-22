import pandas as pd
import statsmodels.api as sm


def ols_fit(y: pd.Series, x: pd.Series) -> dict:
    data = pd.concat([y, x], axis=1).dropna()        # align on dates, drop incomplete rows
    yy, xx = data.iloc[:, 0], data.iloc[:, 1]
    res = sm.OLS(yy, sm.add_constant(xx)).fit()      # y = alpha + beta * x + residual
    return {
        "alpha": float(res.params.iloc[0]),
        "beta": float(res.params.iloc[1]),
        "beta_tstat": float(res.tvalues.iloc[1]),
        "r2": float(res.rsquared),
        "resid_std": float(res.resid.std()),
        "n": int(res.nobs),
    }
