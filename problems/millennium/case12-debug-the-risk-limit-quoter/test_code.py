params = {"soft_frac": 0.6, "base_limit": 1000, "skew_coeff": 0.001}
request = {"side": "BUY", "asset": "Asset_X", "quantity": 100, "reference": 100.0, "half_spread": 0.05}

print(price_quote(params, request, {}, 0.7))                  # flat book
print(price_quote(params, request, {"Asset_X": 550}, 0.7))    # crosses the soft limit
print(price_quote(params, request, {"Asset_X": 900}, 0.7))    # lands exactly on the cap
