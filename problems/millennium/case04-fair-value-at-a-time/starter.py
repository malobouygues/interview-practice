import pandas as pd
import numpy as np

def reference_price(prices: pd.DataFrame, asset: str, ts, max_staleness_minutes: float) -> dict:
    """
    As-of reference price with a staleness cutoff.

    Args:
        prices: clean DataFrame, 'timestamp' + one column per asset (may hold NaNs).
        asset: which asset column to read.
        ts: the request time.
        max_staleness_minutes: refuse (price None) if the last valid print is older.

    Returns:
        {'price': float} as of ts, or {'price': None} if missing / too stale.
    """
    pass
