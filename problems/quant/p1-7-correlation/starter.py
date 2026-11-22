import pandas as pd


def correlation_report(prices: pd.DataFrame, a: str, b: str) -> dict:
    """Pearson and Spearman correlations of levels and of daily changes (diff)."""
    raise NotImplementedError("compute the four correlations")
