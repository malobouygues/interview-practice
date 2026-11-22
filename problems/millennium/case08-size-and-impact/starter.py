import pandas as pd
import numpy as np

def quote_stream_with_impact(reference, requests_for_asset, liquidity_score, impact_params):
    """
    Quote a sequence of same-asset requests with cumulative, decaying impact.

    Args:
        reference: starting fair value.
        requests_for_asset: list of {'side': 'BUY'|'SELL', 'quantity': float}.
        liquidity_score: 0..1; lower => bigger price moves.
        impact_params: {'half_spread', 'k', optional 'decay'}.

    Returns:
        List of quoted prices, one per request (rounded to 9 dp).
    """
    pass
