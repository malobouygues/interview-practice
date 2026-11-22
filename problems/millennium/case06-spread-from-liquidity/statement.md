**Desk context**

You can quote tight for a liquid asset and quote wide for an illiquid asset. You're provided with the liquidity score and the volatility; turn them into a half-spread.

**Problem**

Implement `half_spread(liquidity_score, volatility, params)` where `params` has `base`, `k_vol`, `k_liq` and `min_half_spread`.

**Formula**

```text
half_spread = max(base + k_vol * vol + k_liq * (1 - liquidity_score), min_half_spread)
```

**Constraints**

- `liquidity_score` in [0, 1], `volatility` >= 0.

**Sample I/O**

```text
half_spread(1.0, 0.001, {'base': ...})
half_spread(0.0, 0.08, {'base': ...})
```

> *Note : le Sample I/O est incomplet dans la photo source (bord droit de l'écran hors cadre) ; les valeurs de `params` et les résultats attendus manquent.*

**Notes**

- Increases with volatility and as liquidity falls; clamped at the floor.
