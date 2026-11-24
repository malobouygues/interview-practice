import pandas as pd
import statsmodels.api as sm
from scipy import stats


def chow_test(y: pd.Series, x: pd.Series, break_date: str) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]
    before = data.index < pd.Timestamp(break_date)
    pre = data[before]
    post = data[~before]

    # H0: one line for the whole sample. H1: one line before, another after the known date.
    pooled = sm.OLS(data["y"], sm.add_constant(data["x"])).fit()
    fit_pre = sm.OLS(pre["y"], sm.add_constant(pre["x"])).fit()
    fit_post = sm.OLS(post["y"], sm.add_constant(post["x"])).fit()

    k = 2                        # parameters per regression: constant and slope
    n = len(data)
    ssr_split = fit_pre.ssr + fit_post.ssr
    f_stat = ((pooled.ssr - ssr_split) / k) / (ssr_split / (n - 2 * k))
    pvalue = float(stats.f.sf(f_stat, k, n - 2 * k))

    return {
        "F": float(f_stat),
        "pvalue": pvalue,
        "ssr_pooled": float(pooled.ssr),
        "ssr_pre": float(fit_pre.ssr),
        "ssr_post": float(fit_post.ssr),
        "n_pre": int(len(pre)),
        "n_post": int(len(post)),
        "reject": bool(pvalue < 0.05),
    }
