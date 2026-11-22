def price_quote(params, request, inventory, liquidity_score):
    soft_frac = params["soft_frac"]
    base_limit = params["base_limit"]
    skew_coeff = params["skew_coeff"]

    side = request["side"]
    asset = request["asset"]
    quantity = request["quantity"]
    reference = request["reference"]
    half_spread = request["half_spread"]

    current = inventory.get(asset, 0)
    signed_qty = quantity if side == "BUY" else -quantity
    projected = current + signed_qty

    hard_limit = base_limit
    soft_limit = soft_frac * hard_limit

    # décisions de risque sur la position POST-trade ; toucher le cap = breach
    if abs(projected) >= hard_limit:
        return {"quote": None, "action": "reject"}

    if abs(projected) > soft_limit:
        action = "widen"
        half = 2 * half_spread
    else:
        action = "accept"
        half = half_spread

    # skew calculé sur l'inventaire PRÉ-trade, et SOUSTRAIT : long -> quotes plus basses
    skew = skew_coeff * current

    if side == "BUY":
        quote = reference + half - skew
    else:
        quote = reference - half - skew

    return {"quote": round(quote, 4), "action": action}
