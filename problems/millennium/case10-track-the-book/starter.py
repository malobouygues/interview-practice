import pandas as pd
import numpy as np

def track_book(filled_requests: pd.DataFrame, prices: pd.DataFrame) -> dict:
    """
    Replay fills into per-asset inventory, cash, and mark-to-market PnL.

    Args:
        filled_requests: DataFrame with asset, side (client direction), quantity, fill_price.
        prices: clean DataFrame; last row is used to mark inventory.

    Returns:
        {'inventory': {asset: qty}, 'cash': float, 'pnl': float}.
    """
    pass
