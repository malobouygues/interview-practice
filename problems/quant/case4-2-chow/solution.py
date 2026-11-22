import pandas as pd
import statsmodels.api as sm
from scipy import stats


def _ssr(data):
    return float(sm.OLS(data["y"], sm.add_constant(data["x"])).fit().ssr)


def chow_test(y: pd.Series, x: pd.Series, break_date: str) -> dict:
    data = pd.concat([y, x], axis=1).dropna()
    data.columns = ["y", "x"]
    before = data.index < pd.Timestamp(break_date)
    ssr_pooled = _ssr(data)                 # one line for the whole sample (H0)
    ssr_pre = _ssr(data[before])            # separate lines before / after (H1)
    ssr_post = _ssr(data[~before])
    k, n = 2, len(data)                     # parameters per regression (constant + slope)
    f_stat = ((ssr_pooled - ssr_pre - ssr_post) / k) / ((ssr_pre + ssr_post) / (n - 2 * k))
    pvalue = float(stats.f.sf(f_stat, k, n - 2 * k))
    return {
        "F": float(f_stat),
        "pvalue": pvalue,
        "ssr_pooled": ssr_pooled,
        "ssr_pre": ssr_pre,
        "ssr_post": ssr_post,
        "n_pre": int(before.sum()),
        "n_post": int((~before).sum()),
        "reject": bool(pvalue < 0.05),
    }
