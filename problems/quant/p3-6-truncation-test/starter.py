import numpy as np
import pandas as pd


def truncation_test(build_features, prices: pd.DataFrame, cutoff: str) -> list:
    """Names of the features whose values up to `cutoff` change when later data are removed."""
    raise NotImplementedError("build twice, compare the common history")
