import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_ecm(y: pd.Series, x: pd.Series) -> dict:
    """Two-step ECM. Keys: beta_long_run, alpha, alpha_tstat, gamma, half_life, n."""
    raise NotImplementedError("long-run regression, then the ECM in differences")
