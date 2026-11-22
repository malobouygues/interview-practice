import pandas as pd


def as_of(vintages: pd.DataFrame, as_of_date: str) -> pd.Series:
    """Latest estimate of each month among those published on or before as_of_date."""
    raise NotImplementedError("filter by vintage date, then latest per month")
