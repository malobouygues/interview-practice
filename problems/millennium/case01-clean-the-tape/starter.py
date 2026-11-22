import pandas as pd
import numpy as np

def clean_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Repair the raw price tape.

    Args:
        prices: DataFrame with a 'timestamp' column and one column per asset
                (Asset_1, Asset_2, Asset_3). May contain duplicate rows,
                out-of-order timestamps, non-positive bad prints and NaNs.

    Returns:
        A cleaned DataFrame: time-sorted, de-duplicated, index reset, with
        non-positive prints treated as missing and gaps forward-filled.
    """
    pass
