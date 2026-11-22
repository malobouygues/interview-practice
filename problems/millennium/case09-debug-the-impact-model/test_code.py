print(quote_impact_stream(200.0, {"k": 0.01, "decay": 0.5, "half_spread": 0.0}, 0.0,
                          [{"side": "BUY", "quantity": 100}] * 3))
# -> [200.0, 200.5, 200.75]
