import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def trend_or_random_walk(y: pd.Series) -> dict:
    """Seasonality removed, then ADF 'c' vs 'ct' -> "stationary" / "detrend" / "difference".

    Keys: trend_per_year, seasonal_amplitude, adf_p_c, adf_p_ct,
          std_detrended, std_differenced, decision.
    """
    raise NotImplementedError("remove the seasonal profile, test, decide")
