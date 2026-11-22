import numpy as np
import pandas as pd


def make_returns(prices: pd.Series) -> pd.DataFrame:
    """Columns: price, diff, pct_change, log_return (same index as `prices`).

    Raises ValueError if a price is <= 0.
    """
    raise NotImplementedError("build the three transformations")
