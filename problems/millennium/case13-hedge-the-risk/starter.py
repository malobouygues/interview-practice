import pandas as pd
import numpy as np

def hedge_inventory(prices: pd.DataFrame, inventory: dict) -> dict:
    """
    Variance-minimising hedge of inventory using the two liquid assets.

    Args:
        prices: clean DataFrame, 'timestamp' + Asset_1/2/3.
        inventory: {asset: signed position}.

    Returns:
        {'hedge': {'Asset_1': qty, 'Asset_2': qty}, 'residual_variance': float}.
    """
    pass
