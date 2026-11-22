import pandas as pd
import statsmodels.api as sm


def levels_vs_differences(y: pd.Series, x: pd.Series) -> dict:
    """Same OLS in levels and in first differences.

    Keys: r2_levels, tstat_levels, r2_differences, tstat_differences, verdict
    ("co-moving" / "spurious" / "unrelated").
    """
    raise NotImplementedError("compare the two regressions")
