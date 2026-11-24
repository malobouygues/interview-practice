import numpy as np
import pandas as pd

FUNCTION = "crack_regression"


def hand_made():
    rng = np.random.default_rng(21)
    n = 48
    stocks = rng.normal(-3, 8, n)
    outages = np.where(rng.random(n) < 0.2, rng.uniform(100, 900, n), 0.0)
    utilisation = 86 + rng.normal(0, 1.5, n)
    noise = rng.normal(0, 1, n) * (1 + 0.3 * np.clip(-stocks, 0, None))
    crack = 15 - 0.9 * stocks + 0.004 * outages + noise
    monthly = pd.DataFrame({"month": pd.period_range("2019-01", periods=n, freq="M").astype(str),
                            "gasoil_crack": crack, "stocks_vs_5y_pct": stocks, "outages_kbd": outages,
                            "refinery_utilisation_pct": utilisation, "imports_kbd": 1200.0})
    monthly.loc[7, "refinery_utilisation_pct"] = np.nan
    return {"monthly": monthly}


TESTS = [
    {"name": "Hand-made: variance that grows when stocks are tight", "origin": "extra", "args": hand_made},
    {"name": "Monthly table 2017-2023", "origin": "extra",
     "args": lambda: {"monthly": pd.read_csv("data/p2_monthly_table_synthetic.csv")}},
]
