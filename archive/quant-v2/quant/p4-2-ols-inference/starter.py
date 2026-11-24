import pandas as pd
import statsmodels.api as sm


def ols_fit(y: pd.Series, x: pd.Series) -> dict:
    """OLS of y on a constant and x, with the inference a researcher reports."""
    raise NotImplementedError("fit and report")
