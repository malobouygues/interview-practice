print(decide_request({'Asset_1': 0},
                     {'asset': 'Asset_1', 'side': 'BUY', 'quantity': 100,
                      'reference': 100.0, 'half_spread': 0.05},
                     1.0, {'base_limit': 50000, 'soft_frac': 0.6, 'skew_coeff': 0.0001}))
# -> {'action': 'accept', 'quote': 100.05}
