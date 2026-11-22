import pandas as pd


def as_of(vintages: pd.DataFrame, as_of_date: str) -> pd.Series:
    vintages = vintages.copy()
    vintages["obs_month"] = pd.to_datetime(vintages["obs_month"], format="%Y-%m")
    vintages["vintage_date"] = pd.to_datetime(vintages["vintage_date"])

    # 1. keep only the estimates that had been published on that date
    known = vintages[vintages["vintage_date"] <= pd.Timestamp(as_of_date)]

    # 2. for each month, the most recent of those estimates
    known = known.sort_values("vintage_date")
    view = known.groupby("obs_month")["demand_kbd"].last()
    return view
