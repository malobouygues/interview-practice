def quote_impact_stream(reference, impact_params, liquidity_score, requests_for_asset):
    k = impact_params["k"]
    decay = impact_params["decay"]
    half_spread = impact_params["half_spread"]

    accumulated_impact = 0.0
    quotes = []
    first = True

    for req in requests_for_asset:
        side = req["side"]
        quantity = req["quantity"]

        signed_spread = half_spread if side == "BUY" else -half_spread

        if first:
            quote = reference + 2.0 * signed_spread + accumulated_impact
            first = False
        else:
            quote = reference + signed_spread + accumulated_impact

        side_sign = 1.0 if side == "BUY" else -1.0
        impact_term = k * quantity
        accumulated_impact = accumulated_impact + side_sign * (impact_term * decay)

        quotes.append(round(quote, 9))

    return quotes
