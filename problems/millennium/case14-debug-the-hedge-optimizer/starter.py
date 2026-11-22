import pandas as pd
import numpy as np

def hedge_optimizer(prices, inventory):
    """
    Minimum-variance hedge of an Asset_3 inventory using Asset_1 and Asset_2.

    NOTE: this is the desk's current (mistrusted) version. The hedge ratios come
    out unstable and oversized, and the leftover-risk number looks wrong.
    Diagnose and fix it so it meets the specification.
    """
    df = prices

    hedge_assets = ["Asset_1", "Asset_2"]
    target_asset = "Asset_3"

    q = float(inventory.get(target_asset, 0.0))
    if q == 0.0:
        return {"hedge": {a: 0.0 for a in hedge_assets}, "residual_variance": 0.0}

    # Fit the target against the two instruments and size by inventory.
    y = df[target_asset].to_numpy(dtype=float)
    X = df[hedge_assets].to_numpy(dtype=float)
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    hedge = {a: round(float(-beta[i] * q), 4) for i, a in enumerate(hedge_assets)}

    # How much variability is left in the hedged book?
    resid = y - X @ beta
    residual_variance = round(float(np.mean(resid ** 2)), 4)

    return {"hedge": hedge, "residual_variance": residual_variance}
