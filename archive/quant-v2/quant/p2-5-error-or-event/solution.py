import pandas as pd


def classify_extremes(returns: pd.DataFrame, series: str) -> pd.DataFrame:
    # 1. robust score of every product: median and MAD of the 60 previous days only
    scores = pd.DataFrame(index=returns.index)
    for column in returns.columns:
        r = returns[column]
        rolling_median = r.rolling(60, min_periods=30).median().shift(1)
        rolling_mad = (r - rolling_median).abs().rolling(60, min_periods=30).median().shift(1)
        scores[column] = 0.6745 * (r - rolling_median) / rolling_mad

    others = [column for column in returns.columns if column != series]
    candidates = scores.index[scores[series].abs() > 5]

    rows = []
    previous_label = None
    previous_date = None
    for date in candidates:
        position = returns.index.get_loc(date)
        today = returns[series].iloc[position]

        # 2. evidence: did a related market move too? does the move reverse the next day?
        confirmed = bool((scores.loc[date, others].abs() > 3).any())
        reverses = False
        if position + 1 < len(returns):
            tomorrow = returns[series].iloc[position + 1]
            reverses = bool(tomorrow / today < -0.8)

        # 3. decision
        follows_error = previous_label == "data error" and returns.index.get_loc(previous_date) == position - 1
        if follows_error:
            label, action = "reversal of an error", "disappears once the bad price is removed"
        elif reverses and not confirmed:
            label, action = "data error", "set the price to NaN"
        elif confirmed:
            label, action = "market event", "keep and annotate"
        else:
            label, action = "investigate", "check a second source"

        rows.append([date, today, scores.loc[date, series], confirmed, reverses, label, action])
        previous_label = label
        previous_date = date

    columns = ["date", "return", "score", "confirmed", "reverses", "classification", "action"]
    return pd.DataFrame(rows, columns=columns)
