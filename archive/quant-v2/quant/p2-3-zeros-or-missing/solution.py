import pandas as pd


def total_imports(imports: pd.DataFrame) -> pd.DataFrame:
    imports = imports.copy()
    imports["month"] = pd.to_datetime(imports["month"], format="%Y-%m")

    # 1. long -> wide: one row per month, one column per importing country (sum over origins)
    by_country = imports.groupby(["month", "importer"])["volume_kbd"].sum()
    table = by_country.unstack("importer")          # a country with no rows that month -> NaN

    # 2. a country at exactly 0 from EVERY origin did not report: that is missing, not zero imports
    not_reported = table == 0
    table = table.mask(not_reported)

    # 3. regional total only when every country is known (min_count): a missing report is not a zero
    countries = list(table.columns)
    table["total"] = table[countries].sum(axis=1, min_count=len(countries))
    return table
