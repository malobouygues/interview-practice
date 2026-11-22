import pandas as pd
import numpy as np

def hedge_inventory(prices: pd.DataFrame, inventory: dict) -> dict:
    assets = [c for c in prices.columns if c != "timestamp"]
    liquid = ["Asset_1", "Asset_2"]

    returns = prices[assets].pct_change().dropna()
    C = returns.cov()

    v = np.array([inventory.get(a, 0.0) for a in assets], dtype=float)

    C_LL = C.loc[liquid, liquid].to_numpy()
    C_LL = C_LL + 1e-12 * np.eye(len(liquid))
    C_L_all = C.loc[liquid, assets].to_numpy()

    # h_L = -inv(C_LL) @ C_L,all @ v, résolu sans inverser explicitement
    hedge_rhs = C_L_all @ v
    h = -np.linalg.solve(C_LL, hedge_rhs)

    # w = inventaire + hedge sur les actifs liquides
    w = v.copy()
    for i, a in enumerate(liquid):
        w[assets.index(a)] += h[i]

    residual = w @ C.to_numpy() @ w
    residual = round(float(residual), 10)
    if residual == 0:
        residual = 0.0

    hedge = {}
    for i, a in enumerate(liquid):
        qty = round(float(h[i]), 4)
        if qty == 0:
            qty = 0.0
        hedge[a] = qty

    return {"hedge": hedge, "residual_variance": residual}
