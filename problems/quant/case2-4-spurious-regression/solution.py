import pandas as pd
import statsmodels.api as sm


def _fit(y, x):
    data = pd.concat([y, x], axis=1).dropna()
    return sm.OLS(data.iloc[:, 0], sm.add_constant(data.iloc[:, 1])).fit()


def levels_vs_differences(y: pd.Series, x: pd.Series) -> dict:
    lev = _fit(y, x)                    # regression in (log) price levels
    dif = _fit(y.diff(), x.diff())      # same regression on daily changes
    t_lev, t_dif = float(lev.tvalues.iloc[1]), float(dif.tvalues.iloc[1])
    if abs(t_dif) >= 1.96:
        verdict = "co-moving"           # the link survives in changes: real day-to-day co-movement
    elif abs(t_lev) >= 1.96:
        verdict = "spurious"            # 'significant' in levels only: shared drift, not a link
    else:
        verdict = "unrelated"
    return {
        "r2_levels": float(lev.rsquared),
        "tstat_levels": t_lev,
        "r2_differences": float(dif.rsquared),
        "tstat_differences": t_dif,
        "verdict": verdict,
    }
