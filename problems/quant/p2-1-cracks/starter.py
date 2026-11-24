import numpy as np
import pandas as pd

USD_PER_BBL_FACTOR = {"USD/bbl": 1.0, "USD/gal": 42.0, "USc/gal": 0.42}   # 42 gallons per barrel
BARRELS_PER_TONNE = {"gasoil": 7.45, "jet": 7.88}                          # density, product by product


def build_daily_table(raw):
    """Wide daily table in USD/bbl, frozen runs blanked, cracks against Brent."""
    raise NotImplementedError("key, units, pivot, frozen feed, cracks")
