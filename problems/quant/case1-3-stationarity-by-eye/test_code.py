import numpy as np
import pandas as pd

# Three reference processes (as in the source document)
rng = np.random.default_rng(0)
e = rng.normal(size=500)
white_noise = pd.Series(e)                               # stationary
random_walk = pd.Series(e).cumsum()                      # unit root: shocks are permanent
trend_stationary = pd.Series(0.05 * np.arange(500) + e)  # deterministic trend + stationary noise

ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
series = {"white noise": white_noise, "random walk": random_walk,
          "trend-stationary": trend_stationary, "TTF price": ttf,
          "TTF log returns": np.log(ttf).diff()}

for name, s in series.items():
    out = subsample_stats(s)
    print(f"{name:18s} mean_shift={out['mean_shift']:6.2f}  std_ratio={out['std_ratio']:5.2f}  "
          f"means={[round(m, 3) for m in out['means']]}")
