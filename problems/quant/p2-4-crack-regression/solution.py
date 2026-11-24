import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor

REGRESSORS = ["stocks_vs_5y_pct", "outages_kbd", "refinery_utilisation_pct"]


def crack_regression(monthly):
    sample = monthly.dropna(subset=["gasoil_crack"] + REGRESSORS)
    y = sample["gasoil_crack"]
    X = sm.add_constant(sample[REGRESSORS])

    # the same OLS coefficients, two ways of estimating their standard errors
    conventional = sm.OLS(y, X).fit()
    robust = sm.OLS(y, X).fit(cov_type="HC3")
    table = pd.DataFrame({"coef": conventional.params,
                          "se": conventional.bse, "p": conventional.pvalues,
                          "se_hc3": robust.bse, "p_hc3": robust.pvalues})

    # White test: squared residuals on the regressors, their squares and cross-products.
    # H0: the error variance is constant (homoskedasticity).
    white_lm, white_p, white_f, white_f_p = het_white(conventional.resid, X)

    # multicollinearity: variance inflation factor of each regressor
    vif = {}
    for position, name in enumerate(X.columns):
        if name != "const":
            vif[name] = variance_inflation_factor(X.values, position)

    # residuals by stock regime: is the model wrong on average, or only noisier, when stocks are tight?
    regime = pd.cut(sample["stocks_vs_5y_pct"], [-100, -15, -5, 5, 100],
                    labels=["below -15%", "-15% to -5%", "-5% to +5%", "above +5%"])
    by_regime = conventional.resid.groupby(regime, observed=False).agg(["mean", "std", "count"])

    return {"coefficients": table, "r2": conventional.rsquared, "n": int(conventional.nobs),
            "white_lm": white_lm, "white_p": white_p, "vif": vif,
            "durbin_watson": sm.stats.durbin_watson(conventional.resid),
            "residuals_by_stocks": by_regime}
