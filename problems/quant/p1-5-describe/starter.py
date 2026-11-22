import pandas as pd


def summary_stats(x: pd.Series) -> dict:
    """Keys: n, mean, median, std, var, q05, q95, skew, excess_kurtosis (NaN ignored)."""
    raise NotImplementedError("compute the summary statistics")
