import pandas as pd
import numpy as np

def client_markout(fills: pd.DataFrame, prices: pd.DataFrame, horizon_minutes) -> dict:
    """
    Per-client markout (MM-side PnL at a future horizon) and a toxic flag.

    Args:
        fills: DataFrame with client_id, timestamp, asset, side, quantity, ...
        prices: clean tape (timestamp + one column per asset).
        horizon_minutes: how far after each fill to mark the PnL.

    Returns:
        {client_id: {'avg_markout': float (6 dp), 'toxic': bool}} where toxic
        means the client's average markout is negative.
    """
    pass
