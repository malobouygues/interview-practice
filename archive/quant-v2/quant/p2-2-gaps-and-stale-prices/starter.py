import numpy as np
import pandas as pd


def treat_gaps(products: pd.DataFrame) -> dict:
    """{"prices": treated prices, "filled": boolean frame of imputed values}."""
    raise NotImplementedError("one row per date, stale runs, limited forward fill")
