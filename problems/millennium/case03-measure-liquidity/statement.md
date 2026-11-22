**Desk context**

Decisions such as how wide to quote or how much to hold depend on how liquid each asset is, and liquidity is not labelled in the data. You measure it from a clean, time-sorted prices tape and the requests flow: a liquid asset has a stable price and plenty of client interest; an illiquid one is jumpy and rarely asked for.

**Problem**

Implement `liquidity_scores(prices, requests)` which returns `{asset: score}` in [0.1, 1.0] (higher = more liquid), blending low return volatility with high request frequency.

**Formula**

```text
score = 0.1 + 0.9 * (0.5 * (1 - vol_norm) + 0.5 * freq_norm)
```

where `vol` is

```python
prices[asset].pct_change().std()
```

`freq` is the asset's share of all requests, and each (`vol`, `freq`) is min-max normalised across the assets. The `0.1 + 0.9*(...)` floor keeps even the least-liquid asset on a non-zero score, so it is still quotable (just wide) rather than frozen out.

**Rules**

- Asset columns are every column of `prices` except `timestamp`.
- If a signal has zero range across assets, its normalised value is 0.5 for every asset.
- Round each score to 6 dp.

**Constraints**

- At least 3 price rows. pandas / numpy available.

**Sample I/O**

```text
Input: prices where Asset_1 is [...]
Output: {'Asset_1': 1.0, 'Asset_2': [...]}
```

> *Note : le Sample I/O est incomplet dans la photo source (bord droit de l'écran hors cadre).*

**Notes**

- Volatility is inverted (low vol = liquid); frequency is kept (more flow = liquid). The [0.1, 1.0] floor is deliberate: the illiquid name keeps [...] *(fin de note coupée dans la photo source)*
