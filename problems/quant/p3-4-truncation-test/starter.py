import pandas as pd


def truncation_test(build_features, stocks, prices, cutoff):
    """Build the features on all data and on the data available at `cutoff`; count the rows that differ."""
    raise NotImplementedError("full build, truncated build, compare the common rows")
