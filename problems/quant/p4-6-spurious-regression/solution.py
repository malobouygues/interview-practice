import pandas as pd
import statsmodels.api as sm


def levels_vs_differences(y: pd.Series, x: pd.Series) -> dict:
    # 1. regression in (log) price levels
    levels = pd.concat([y, x], axis=1).dropna()
    levels.columns = ["y", "x"]
    in_levels = sm.OLS(levels["y"], sm.add_constant(levels["x"])).fit()

    # 2. the same regression on daily changes
    changes = levels.diff().dropna()
    in_changes = sm.OLS(changes["y"], sm.add_constant(changes["x"])).fit()

    t_levels = float(in_levels.tvalues["x"])
    t_changes = float(in_changes.tvalues["x"])

    if abs(t_changes) >= 1.96:
        verdict = "co-moving"        # the link survives in changes: real day-to-day co-movement
    elif abs(t_levels) >= 1.96:
        verdict = "spurious"         # 'significant' in levels only: shared drift, not a link
    else:
        verdict = "unrelated"

    return {
        "r2_levels": float(in_levels.rsquared),
        "tstat_levels": t_levels,
        "r2_differences": float(in_changes.rsquared),
        "tstat_differences": t_changes,
        "verdict": verdict,
    }
