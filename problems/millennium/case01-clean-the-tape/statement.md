**Desk context**

You're on a market-making desk quoting three assets of varying liquidity, and everything starts from the prices tape, a per-timestamp reference price for Asset_1, Asset_2 and Asset_3. The raw feed is dirty: rows arrive out of order and occasionally duplicated, some prints are non-positive (a zero or a negative is never a real price), and there are gaps where nothing is printed. You can't quote off a dirty tape, so the first task is to repair it.

**Problem**

Implement `clean_prices(prices)` which returns a repaired copy of the tape, time-sorted and gap-filled.

**Rules**

- Sort by `timestamp` and drop exact duplicate rows; reset the index to 0..n-1.
- For each asset column, treat any value <= 0 as missing (NaN).
- Forward-fill each asset column so gaps and stale bars carry the last good price. Never back-fill, because using a future price is look-ahead.
- A leading gap (no earlier price exists) stays NaN.

**Constraints**

- `prices` has a `timestamp` column plus `Asset_1`, `Asset_2`, `Asset_3`.
- Operate vectorized. pandas / numpy available.

**Sample I/O**

```text
Input (unsorted, one duplicate):
09:00, 100.2, 50.2, 20.2
09:00, 100.0, 50.0, 20.0
09:01, 100.1, NaN, 20.1
09:00, 100.0, 50.0, 20.0

Output:
09:00, 100.0, 50.0, 20.0
09:01, 100.1, 50.0, 20.1
09:02, 100.2, 50.2, 20.2
```

> *Note : l'échantillon ci-dessus est retranscrit tel quel depuis la photo source ; il manquait une ligne d'input 09:02, à vérifier sur l'énoncé original si besoin.*

**Notes**

- Forward-fill only. The leading-NaN case is intentional: there is no price before the first print.
