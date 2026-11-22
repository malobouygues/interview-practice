import pandas as pd

prices = pd.read_csv("data/p1_crude_prices_clean_synthetic.csv", parse_dates=["date"], index_col="date")

for a, b in [("brent", "dubai"), ("brent", "wti")]:
    print(a, b, {key: round(value, 3) for key, value in correlation_report(prices, a, b).items()})

event_days = pd.to_datetime(["2020-04-20", "2020-04-21"])
without_event = prices.drop(event_days)
print("brent wti without the expiry", {k: round(v, 3) for k, v in correlation_report(without_event, "brent", "wti").items()})
