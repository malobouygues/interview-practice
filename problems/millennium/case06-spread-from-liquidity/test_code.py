params = {'base': 0.01, 'k_vol': 2.0, 'k_liq': 0.05, 'min_half_spread': 0.02}
print(half_spread(1.0, 0.001, params))
print(half_spread(0.0, 0.08, params))
