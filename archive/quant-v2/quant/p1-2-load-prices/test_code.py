prices = load_crude_prices("data/p1_crude_prices_vendor_synthetic.csv")
print(prices.info())
print(prices.head())
print("missing values per column:")
print(prices.isna().sum())
print(prices.loc["2019-06-12"])      # a corrected date: which value did you keep?
