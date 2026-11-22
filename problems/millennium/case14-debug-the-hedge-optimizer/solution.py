import pandas as pd
import numpy as np

def hedge_optimizer(prices, inventory):
    if isinstance(prices, dict):
        df = pd.DataFrame(prices["data"], columns=prices["columns"])
    else:
        df = prices.copy()

    hedge_assets = ["Asset_1", "Asset_2"]
    target_asset = "Asset_3"

    q = float(inventory.get(target_asset, 0.0))
    if q == 0.0:
        return {"hedge": {a: 0.0 for a in hedge_assets}, "residual_variance": 0.0}

    # 1. rendements, pas niveaux de prix ; la première ligne est indéfinie
    returns = df[hedge_assets + [target_asset]].pct_change()
    returns = returns.iloc[1:]

    # 2. dé-moyenner cible et instruments
    y = returns[target_asset].to_numpy(dtype=float)
    X = returns[hedge_assets].to_numpy(dtype=float)
    y = y - y.mean()
    X = X - X.mean(axis=0)

    # 3. OLS sur données centrées (pas d'intercept nécessaire)
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    # 4. on trade contre l'exposition
    hedge = {a: round(float(-beta[i] * q), 4) for i, a in enumerate(hedge_assets)}

    # 5. variance de population du rendement hedgé, mesurée autour de sa moyenne
    hedged = y - X @ beta
    hedged = hedged - hedged.mean()
    residual_variance = np.mean(hedged ** 2)
    residual_variance = round(float(residual_variance), 4)

    return {"hedge": hedge, "residual_variance": residual_variance}
