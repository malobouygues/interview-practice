print(quote_stream_with_impact(20.0, [{'side': 'BUY', 'quantity': 2500}] * 3, 0.0,
                               {'half_spread': 0.1, 'k': 2e-5, 'decay': 0.9}))
# -> [20.1, 20.145000045, 20.185500086]
