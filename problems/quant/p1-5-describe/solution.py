import pandas as pd


def summary_stats(x: pd.Series) -> dict:
    x = x.dropna()                      # describe the observed values only

    return {
        "n": int(len(x)),
        "mean": float(x.mean()),
        "median": float(x.median()),
        "std": float(x.std()),          # sample standard deviation (ddof=1)
        "var": float(x.var()),          # sample variance (ddof=1)
        "q05": float(x.quantile(0.05)),
        "q95": float(x.quantile(0.95)),
        "skew": float(x.skew()),        # > 0: long right tail
        "excess_kurtosis": float(x.kurt()),   # pandas gives EXCESS kurtosis: 0 for a normal
    }
