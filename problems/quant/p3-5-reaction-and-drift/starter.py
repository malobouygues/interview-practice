import pandas as pd
import statsmodels.api as sm

RESEARCH_END = pd.Timestamp("2022-12-31")    # 2023-2024 stays untouched for the out-of-sample test (3.6)


def reaction_and_drift(events, decisions):
    """Release-day reaction (one row per release) and 10-day drift (one row per day): OLS and HAC."""
    raise NotImplementedError("two regressions on the research sample, two kinds of standard errors")
