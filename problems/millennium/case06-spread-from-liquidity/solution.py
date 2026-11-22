def half_spread(liquidity_score: float, volatility: float, params: dict) -> float:
    raw = params['base'] + params['k_vol'] * volatility + params['k_liq'] * (1 - liquidity_score)
    return float(max(raw, params['min_half_spread']))
