import pandas as pd

def track_book(filled_requests: pd.DataFrame, prices: pd.DataFrame) -> dict:
    assets = [c for c in prices.columns if c != "timestamp"]

    inventory = {a: 0 for a in assets}
    cash = 0.0

    for _, fill in filled_requests.iterrows():
        qty = fill["quantity"]

        if fill["side"] == "BUY":
            # client BUY -> le MM a vendu
            inventory[fill["asset"]] -= qty
            cash += fill["fill_price"] * qty
        else:
            # client SELL -> le MM a acheté
            inventory[fill["asset"]] += qty
            cash -= fill["fill_price"] * qty

    last_price = prices[assets].iloc[-1]
    mark_to_market = sum(inventory[a] * last_price[a] for a in assets)
    pnl = cash + mark_to_market

    return {
        "inventory": inventory,
        "cash": round(float(cash), 6),
        "pnl": round(float(pnl), 6),
    }
