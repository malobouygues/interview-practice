def quote_impact_stream(reference, impact_params, liquidity_score, requests_for_asset):
    k = impact_params["k"]
    decay = impact_params["decay"]
    half_spread = impact_params["half_spread"]

    accumulated_impact = 0.0
    quotes = []

    for req in requests_for_asset:
        side = req["side"]
        quantity = req["quantity"]

        # 1. spread signé
        signed_spread = half_spread if side == "BUY" else -half_spread

        # 2. quote avec l'état AVANT cet ordre (un seul spread, y compris au premier)
        quote = reference + signed_spread + accumulated_impact

        # 3. impact de l'ordre, pondéré par l'illiquidité
        side_sign = 1.0 if side == "BUY" else -1.0
        impact_term = k * quantity * (1 - liquidity_score)
        accumulated_impact = accumulated_impact + side_sign * impact_term

        # 4. mean-reversion de TOUT l'état
        accumulated_impact = accumulated_impact * decay

        quotes.append(round(quote, 9))

    return quotes
