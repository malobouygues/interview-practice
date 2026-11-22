print(quote_request(100.0, 0.05, 'BUY', 100, {'k': 1e-5}, 0.01))   # 100.06
print(quote_request(100.0, 0.05, 'SELL', 100, {'k': 1e-5}, 0.01))  # 99.94
