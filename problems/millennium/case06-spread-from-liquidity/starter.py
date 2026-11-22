import pandas as pd
import numpy as np

def half_spread(liquidity_score: float, volatility: float, params: dict) -> float:
    """
    Map liquidity + volatility to a half-spread.

    Args:
        liquidity_score: 0..1, higher = more liquid.
        volatility: short-term return volatility of the asset.
        params: {'base', 'k_vol', 'k_liq', 'min_half_spread'}.

    Returns:
        Half-spread, never below params['min_half_spread'].
    """
    pass
