import pandas as pd
import numpy as np

def decide_request(inventory: dict, request: dict, liquidity_score: float, params: dict) -> dict:
    """
    Decide accept / widen / reject for one request and produce the quote.

    Args:
        inventory: {asset: signed position}.
        request: {asset, side, quantity, reference, half_spread}.
        liquidity_score: 0..1; scales the position cap.
        params: {base_limit, soft_frac, skew_coeff}.

    Returns:
        {'action': 'accept'|'widen'|'reject', 'quote': float|None}.
    """
    pass
