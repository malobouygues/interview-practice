import math

def price_quote(params, request, inventory, liquidity_score):
    data = {"params": params, "request": request, "inventory": inventory, "liquidity_score": liquidity_score}
    params = data["params"]
    req = data["request"]
    inventory = data["inventory"]

    soft_frac = params["soft_frac"]
    base_limit = params["base_limit"]
    skew_coeff = params["skew_coeff"]

    side = req["side"]
    asset = req["asset"]
    quantity = req["quantity"]
    reference = req["reference"]
    half_spread = req["half_spread"]

    current = inventory.get(asset, 0)
    signed_qty = quantity if side == "BUY" else -quantity
    projected = current + signed_qty

    hard_limit = base_limit
    soft_limit = soft_frac * hard_limit

    # Refuse anything that breaches our risk limit, then widen if we are loaded up.
    if abs(current) > hard_limit:
        return {"quote": None, "action": "reject"}

    if abs(current) > soft_limit:
        action = "widen"
        half = 2 * half_spread
    else:
        action = "accept"
        half = half_spread

    # Lean the quote against the inventory we are carrying.
    skew = skew_coeff * current

    if side == "BUY":
        quote = reference + half + skew
    else:
        quote = reference - half + skew

    return {"quote": round(quote, 4), "action": action}
