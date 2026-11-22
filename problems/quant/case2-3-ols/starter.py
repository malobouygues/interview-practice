import pandas as pd
import statsmodels.api as sm


def ols_fit(y: pd.Series, x: pd.Series) -> dict:
    """OLS of y on a constant and x. Keys: alpha, beta, beta_tstat, r2, resid_std, n."""
    raise NotImplementedError("fit the regression")
