import numpy as np
import pandas as pd

MARKET_TZ = "Europe/Paris"


def daily_zone_table(temps, load, zones):
    """One row per zone x local market day: temperature, HDD, CDD, average MW and MWh."""
    raise NotImplementedError("temperatures -> hourly -> local day; degree days; load -> local day")
