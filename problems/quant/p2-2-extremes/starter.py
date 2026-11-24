import numpy as np
import pandas as pd

SISTER_MARKETS = {"brent": ["gasoil", "ulsd"], "gasoil": ["ulsd", "jet"], "ulsd": ["gasoil", "jet"],
                  "rbob": ["ulsd", "brent"], "jet": ["gasoil", "ulsd"]}
UNIT_FACTORS = [100.0, 42.0, 10.0, 0.1, 1 / 42, 0.01]


def investigate_extremes(prices, events):
    """Pass 1: impossible values and unit errors. Pass 2: scores. Pass 3: investigate and decide."""
    raise NotImplementedError("fix the gross errors first, then score, then investigate")
