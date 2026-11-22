import pandas as pd
import numpy as np

def liquidity_scores(prices: pd.DataFrame, requests: pd.DataFrame) -> dict:
    """
    Score each asset's liquidity in [0.1, 1.0] (higher = more liquid).

    Args:
        prices: clean, time-sorted DataFrame (timestamp + one col per asset).
        requests: client RFQs (request_id, timestamp, asset, side, quantity).

    Returns:
        {asset: score} rounded to 6 dp, blending low volatility and high
        request frequency (each min-max normalised), floored onto [0.1, 1.0].
    """
    pass
