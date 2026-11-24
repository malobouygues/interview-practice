import pandas as pd


def realtime_growth(vintages: pd.DataFrame, decision_dates: list) -> pd.DataFrame:
    """Index decision_date; columns obs_month, growth_realtime, growth_final (YoY, %)."""
    raise NotImplementedError("rebuild the information set at each decision date")
