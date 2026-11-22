import pandas as pd


def total_imports(imports: pd.DataFrame) -> pd.DataFrame:
    """Wide monthly imports by country (kb/d) + a total that is NaN if a country is missing."""
    raise NotImplementedError("long -> wide, non-reports -> NaN, careful total")
