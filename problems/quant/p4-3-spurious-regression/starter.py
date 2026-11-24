import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint


def spurious_check(prices):
    """Levels vs changes for WTI on coffee and on Brent; DW; residual ADF (naive) vs Engle-Granger."""
    raise NotImplementedError("same regression in levels and in changes, two ways of testing the residuals")
