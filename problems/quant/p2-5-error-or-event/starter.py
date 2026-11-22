import pandas as pd


def classify_extremes(returns: pd.DataFrame, series: str) -> pd.DataFrame:
    """Columns: date, return, score, confirmed, reverses, classification, action."""
    raise NotImplementedError("score, find candidates, weigh the evidence")
