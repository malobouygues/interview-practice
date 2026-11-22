import numpy as np
import pandas as pd


def subsample_stats(x: pd.Series, parts: int = 4) -> dict:
    """Mean and std of `parts` consecutive blocks, plus mean_shift and std_ratio."""
    raise NotImplementedError("split into blocks and compare their moments")
