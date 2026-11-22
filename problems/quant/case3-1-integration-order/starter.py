import warnings

import pandas as pd
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.stattools import adfuller, kpss


def integration_order(x: pd.Series, max_order: int = 2) -> dict:
    """Difference until ADF + KPSS agree on "stationary".

    Returns {"order": d or None, "verdicts": [verdict at d=0, d=1, ...]}.
    """
    raise NotImplementedError("test, difference, re-test")
