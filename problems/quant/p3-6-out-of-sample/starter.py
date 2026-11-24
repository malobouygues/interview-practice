import numpy as np
import pandas as pd
import statsmodels.api as sm

FEATURES = ["surprise_mbbl", "demand_growth_known_pct"]
TARGET = "ret_fwd_10d"
TRAIN_END = pd.Timestamp("2022-12-31")
TEST_START = pd.Timestamp("2023-01-01")
TEST_END = pd.Timestamp("2024-12-31")


def validate_out_of_sample(decisions):
    """Fixed chronological split with baselines, then an expanding-window walk-forward by quarter."""
    raise NotImplementedError("estimate on 2019-2022 only, freeze, test on 2023-2024, then walk forward")
