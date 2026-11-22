import numpy as np
import pandas as pd


def make_returns(prices: pd.Series) -> pd.DataFrame:
    """Columns price, diff, pct_change, log_return on observed prices; ValueError if a price <= 0."""
    raise NotImplementedError("build the three transformations")
