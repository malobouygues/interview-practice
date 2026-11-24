import numpy as np
import pandas as pd
import statsmodels.api as sm


def compare_specifications(returns: pd.DataFrame) -> pd.DataFrame:
    """One row per specification: n, r2, adj_r2, aic, bic, brent_beta, brent_se, added_coef, added_pvalue."""
    raise NotImplementedError("same sample, four regressions, one table")
