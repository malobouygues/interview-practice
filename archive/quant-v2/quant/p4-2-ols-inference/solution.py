import pandas as pd
import statsmodels.api as sm


def ols_fit(y: pd.Series, x: pd.Series) -> dict:
    # align the two series on their dates and drop incomplete rows
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]

    # y = alpha + beta * x + residual
    model = sm.OLS(data["y"], sm.add_constant(data["x"]))
    result = model.fit()

    ci_low, ci_high = result.conf_int(alpha=0.05).loc["x"]

    return {
        "alpha": float(result.params["const"]),
        "beta": float(result.params["x"]),
        "beta_se": float(result.bse["x"]),
        "beta_tstat": float(result.tvalues["x"]),
        "beta_pvalue": float(result.pvalues["x"]),
        "beta_ci_low": float(ci_low),
        "beta_ci_high": float(ci_high),
        "r2": float(result.rsquared),
        "resid_std": float(result.resid.std()),
        "n": int(result.nobs),
    }
