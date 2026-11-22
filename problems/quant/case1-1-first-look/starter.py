import pandas as pd


def summary_stats(x: pd.Series) -> dict:
    """Descriptive statistics of a series, ignoring missing values.

    Returns a dict with keys: n, mean, median, var, std, skew, excess_kurtosis.
    """
    raise NotImplementedError("compute the summary statistics")
