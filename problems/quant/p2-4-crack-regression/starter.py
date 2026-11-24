import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor

REGRESSORS = ["stocks_vs_5y_pct", "outages_kbd", "refinery_utilisation_pct"]


def crack_regression(monthly):
    """OLS of the monthly gasoil crack; conventional vs HC3 SEs; White test; VIF; residual checks."""
    raise NotImplementedError("fit, test the variance, compare the standard errors, look at the residuals")
