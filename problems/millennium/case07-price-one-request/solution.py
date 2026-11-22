import numpy as np

def quote_request(reference, half_spread, side, quantity, size_params, tick_size) -> float:
    k = size_params["k"]

    if side == "BUY":
        # client BUY -> le MM vend -> on cote l'ask
        raw = reference + half_spread + k * quantity
    else:
        # client SELL -> le MM achète -> on cote le bid
        raw = reference - half_spread - k * quantity

    # on retire le bruit floating-point avant d'arrondir au tick
    raw_ticks = round(raw / tick_size, 9)

    # arrondi vers l'extérieur : ask vers le haut, bid vers le bas
    if side == "BUY":
        ticks = np.ceil(raw_ticks)
    else:
        ticks = np.floor(raw_ticks)

    return round(float(ticks * tick_size), 10)
