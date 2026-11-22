import pandas as pd


def profile_raw_file(raw: pd.DataFrame) -> dict:
    price_columns = ["Brent (USD/bbl)", "WTI (USD/bbl)", "Dubai (USD/bbl)"]

    # 1. Structure: which type did pandas guess for each column?
    dtypes = {}
    for column in raw.columns:
        dtypes[column] = str(raw[column].dtype)

    # 2. Duplicates: identical rows (a day loaded twice) vs a date that appears more than once
    exact_duplicate_rows = int(raw.duplicated().sum())
    repeated_dates = int(raw["Date"].duplicated().sum())

    # 3. Which text values stop the price columns from being numeric?
    non_numeric_codes = {}
    for column in price_columns:
        as_number = pd.to_numeric(raw[column], errors="coerce")
        bad_values = raw.loc[as_number.isna(), column]
        non_numeric_codes[column] = sorted(bad_values.unique().tolist())

    # 4. Dates: parse them explicitly (day first), then check order and range
    dates = pd.to_datetime(raw["Date"], format="%d/%m/%Y")

    return {
        "n_rows": int(len(raw)),
        "dtypes": dtypes,
        "exact_duplicate_rows": exact_duplicate_rows,
        "repeated_dates": repeated_dates,
        "non_numeric_codes": non_numeric_codes,
        "dates_in_order": bool(dates.is_monotonic_increasing),
        "first_date": dates.min().strftime("%Y-%m-%d"),
        "last_date": dates.max().strftime("%Y-%m-%d"),
    }
