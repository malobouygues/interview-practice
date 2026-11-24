import pandas as pd
import statsmodels.api as sm


def weather_adjusted_load(daily, normals):
    """OLS of daily load on HDD, CDD and a weekend dummy, zone by zone; load adjusted to normal weather."""
    raise NotImplementedError("merge the normals, one regression per zone, adjust, compare the winters")
