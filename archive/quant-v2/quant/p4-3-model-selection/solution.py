import numpy as np
import pandas as pd
import statsmodels.api as sm


def compare_specifications(returns: pd.DataFrame) -> pd.DataFrame:
    data = returns.copy()
    data["brent_lag1"] = data["brent"].shift(1)

    # the SAME observations for every specification, otherwise R2, AIC and BIC are not comparable
    data = data.dropna()

    specifications = {
        "brent": ["brent"],
        "brent + dubai": ["brent", "dubai"],
        "brent + coffee": ["brent", "coffee"],
        "brent + brent_lag1": ["brent", "brent_lag1"],
    }

    rows = []
    for name, regressors in specifications.items():
        result = sm.OLS(data["wti"], sm.add_constant(data[regressors])).fit()

        added = regressors[-1] if len(regressors) > 1 else None
        added_coef = float(result.params[added]) if added else np.nan
        added_pvalue = float(result.pvalues[added]) if added else np.nan

        rows.append({"specification": name,
                     "n": int(result.nobs),
                     "r2": float(result.rsquared),
                     "adj_r2": float(result.rsquared_adj),
                     "aic": float(result.aic),
                     "bic": float(result.bic),
                     "brent_beta": float(result.params["brent"]),
                     "brent_se": float(result.bse["brent"]),
                     "added_coef": added_coef,
                     "added_pvalue": added_pvalue})

    table = pd.DataFrame(rows)
    table = table.set_index("specification")
    return table
