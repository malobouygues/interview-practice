import numpy as np
import pandas as pd


def outlier_scores(returns: pd.Series) -> pd.DataFrame:
    """Columns: return, z, modified_z, iqr_outlier, rolling_modified_z."""
    raise NotImplementedError("compute the four scores")
