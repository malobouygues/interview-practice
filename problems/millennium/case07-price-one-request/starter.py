import pandas as pd
import numpy as np

def quote_request(reference, half_spread, side, quantity, size_params, tick_size) -> float:
    """
    Price one client request.

    Args:
        reference: fair value to quote around.
        half_spread: edge per side.
        side: client's direction, 'BUY' (MM sells -> ask) or 'SELL' (MM buys -> bid).
        quantity: order size (drives the size penalty).
        size_params: {'k': size-penalty coefficient}.
        tick_size: venue minimum increment.

    Returns:
        The quoted price, snapped to the tick grid (ask up / bid down).
    """
    pass
