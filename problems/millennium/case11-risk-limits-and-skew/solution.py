def decide_request(inventory: dict, request: dict, liquidity_score: float, params: dict) -> dict:
    asset = request["asset"]
    side = request["side"]
    quantity = request["quantity"]
    reference = request["reference"]
    half_spread = request["half_spread"]

    current = inventory.get(asset, 0)

    hard = params["base_limit"] * liquidity_score
    soft = params["soft_frac"] * hard

    # client BUY -> le MM vend -> sa position baisse
    signed = -quantity if side == "BUY" else quantity
    projected = current + signed

    if abs(projected) > hard:
        return {"action": "reject", "quote": None}

    # on penche contre la position actuelle : long -> quotes plus basses
    skew = -params["skew_coeff"] * current

    if abs(projected) > soft:
        action = "widen"
        half = 2 * half_spread
    else:
        action = "accept"
        half = half_spread

    if side == "BUY":
        quote = reference + half + skew
    else:
        quote = reference - half + skew

    return {"action": action, "quote": round(quote, 6)}
