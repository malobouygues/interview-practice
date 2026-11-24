import pandas as pd


def build_features(cracks: pd.DataFrame) -> pd.DataFrame:
    """Target crack_change + features known on the morning of day t."""
    raise NotImplementedError("build the features with an explicit information set")
