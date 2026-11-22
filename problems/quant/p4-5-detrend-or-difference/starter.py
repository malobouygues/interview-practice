import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def trend_or_random_walk(y: pd.Series) -> dict:
    """Seasonal profile removed, ADF 'c' vs 'ct' -> "stationary" / "detrend" / "difference"."""
    raise NotImplementedError("remove the seasonal profile, test, decide")
