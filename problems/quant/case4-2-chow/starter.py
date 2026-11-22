import pandas as pd
import statsmodels.api as sm
from scipy import stats


def chow_test(y: pd.Series, x: pd.Series, break_date: str) -> dict:
    """Chow test for a change in (constant, slope) at a known date.

    Keys: F, pvalue, ssr_pooled, ssr_pre, ssr_post, n_pre, n_post, reject.
    """
    raise NotImplementedError("three regressions, one F statistic")
