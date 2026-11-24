import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import coint


def relationship_by_period(prices, break_date="2016-01-01"):
    """Engle-Granger, long-run coefficient, mean spread and pass-through by period; Chow test at the break."""
    raise NotImplementedError("full sample, before, after — then the Chow F")
