import pandas as pd


def summary_stats(x: pd.Series) -> dict:
    x = x.dropna()                      # statistics describe the observed values only
    return {
        "n": int(len(x)),
        "mean": float(x.mean()),
        "median": float(x.median()),
        "var": float(x.var()),          # sample variance (ddof=1)
        "std": float(x.std()),          # sample standard deviation (ddof=1)
        "skew": float(x.skew()),        # > 0: long right tail (spikes up)
        "excess_kurtosis": float(x.kurt()),  # pandas returns EXCESS kurtosis: 0 for a normal
    }
