import numpy as np
import pandas as pd


def levels_and_returns(prices):
    prices = prices.copy()
    prices["date"] = pd.to_datetime(prices["date"])
    prices = prices.set_index("date")

    # 1. levels: two trending series correlate whether or not they are related
    level_corr = {"brent_wti": prices["brent"].corr(prices["wti"]),
                  "wti_coffee": prices["wti"].corr(prices["coffee"])}

    # 2. daily log returns: what moves together day by day
    returns = np.log(prices[["brent", "wti", "coffee"]]).diff().dropna()
    return_corr = {"brent_wti_pearson": returns["brent"].corr(returns["wti"]),
                   "brent_wti_spearman": returns["brent"].corr(returns["wti"], method="spearman"),
                   "wti_coffee_pearson": returns["wti"].corr(returns["coffee"])}

    # 3. the shape of the distribution of Brent returns
    brent = returns["brent"]
    distribution = {"mean": brent.mean(), "median": brent.median(), "std": brent.std(),
                    "skew": brent.skew(), "excess_kurtosis": brent.kurt()}

    # 4. volatility is not constant: 60-day rolling and calendar-year volatility, annualised
    rolling_vol = brent.rolling(60).std() * np.sqrt(252)
    yearly_vol = brent.groupby(brent.index.year).std() * np.sqrt(252)

    # 5. the Brent-WTI spread in USD/bbl, year by year
    spread = prices["brent"] - prices["wti"]
    spread_by_year = spread.groupby(spread.index.year).mean()

    return {"level_corr": level_corr, "return_corr": return_corr, "brent_distribution": distribution,
            "rolling_vol_60d": rolling_vol, "yearly_vol": yearly_vol, "spread_by_year": spread_by_year}
