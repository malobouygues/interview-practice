def quote_stream_with_impact(reference, requests_for_asset, liquidity_score, impact_params):
    half_spread = impact_params["half_spread"]
    k = impact_params["k"]
    decay = impact_params.get("decay", 1.0)

    offset = 0.0
    quotes = []

    for req in requests_for_asset:
        if req["side"] == "BUY":
            quote = reference + offset + half_spread
            signed_qty = req["quantity"]
        else:
            quote = reference + offset - half_spread
            signed_qty = -req["quantity"]

        quotes.append(round(quote, 9))

        # l'impact de ce fill ne touche que les quotes suivantes
        offset += k * signed_qty * (1 - liquidity_score + 1e-6)
        offset *= decay

    return quotes
