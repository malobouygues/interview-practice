import pandas as pd


def lead_lag_table(x: pd.Series, y: pd.Series, max_lag: int) -> pd.Series:
    """corr(x_{t-k}, y_t) for k = -max_lag .. max_lag (positive k: x moved first)."""
    raise NotImplementedError("loop over the lags")
