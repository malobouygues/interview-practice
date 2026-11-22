import pandas as pd

GALLONS_PER_BARREL = 42.0
BARRELS_PER_TONNE_GASOIL = 7.45     # density-based conversion, gasoil / diesel
BARRELS_PER_TONNE_JET = 7.88        # jet fuel is lighter: more barrels per tonne


def crack_spreads(products: pd.DataFrame) -> pd.DataFrame:
    brent = products["brent_usd_bbl"]

    # 1. every product in USD per barrel before comparing it with crude
    ulsd = products["ulsd_usd_gal"] * GALLONS_PER_BARREL
    rbob = products["rbob_usd_gal"] * GALLONS_PER_BARREL
    gasoil = products["gasoil_usd_t"] / BARRELS_PER_TONNE_GASOIL
    jet = products["jet_usd_t"] / BARRELS_PER_TONNE_JET

    # 2. crack = product price - crude price: the gross refining margin of that product
    cracks = pd.DataFrame(index=products.index)
    cracks["diesel_crack"] = ulsd - brent
    cracks["gasoline_crack"] = rbob - brent
    cracks["gasoil_crack"] = gasoil - brent
    cracks["jet_crack"] = jet - brent

    # 3. a 3-2-1 crack: 3 barrels of crude -> 2 of gasoline + 1 of diesel, per barrel of crude
    cracks["crack_321"] = (2 * rbob + ulsd - 3 * brent) / 3
    return cracks
