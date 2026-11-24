import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, adfuller


def stationarity_table(prices, demand):
    """ADF (with justified deterministic terms) and ACF for each series and transformation."""
    raise NotImplementedError("build the eight candidates, test each one, read the ACFs")
