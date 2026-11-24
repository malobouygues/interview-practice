import pandas as pd


def quality_checks(prices: pd.DataFrame) -> pd.DataFrame:
    """One row per flagged observation: date, series, value, issue, action."""
    raise NotImplementedError("code the three controls")
