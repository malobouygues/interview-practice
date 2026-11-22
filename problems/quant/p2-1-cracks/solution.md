### A. Reasoning — why units come before everything

A crack is a margin: product minus the crude it is refined from. Product markets quote in their own units (gallons in New York, tonnes in Europe), so the first and most frequent error in product research is comparing numbers that are not in the same unit. Converting explicitly, with the factors written as named constants, makes the economics of every later number checkable.

### B. Theory

- Volume: 42 US gal/bbl. Mass → volume: barrels per tonne = depends on density (gasoil ≈ 7.45, jet ≈ 7.88, gasoline ≈ 8.5).
- Crack = product (USD/bbl) − crude (USD/bbl). The 3-2-1 crack approximates a refinery's product slate per barrel of crude.
- Seasonality is economic: diesel/heating oil demand peaks in winter; gasoline demand peaks in the driving season.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| crack (USD/bbl) | median | typical range |
|---|---|---|
| diesel | 17.2 | 15–19 |
| gasoil | 15.9 | 13.6–17.3 |
| jet | 18.1 | 16–20 |
| gasoline | 12.1 | 6.6–15.8 (one value at 863!) |

- Diesel crack by month: ≈ **19.5 in January**, ≈ **14 in July–August** — the heating season. Gasoline: lowest in winter (≈ 4), highest from May to August.
- 14 May 2019: gasoline crack **862.95** USD/bbl, normal the day before and after. A refinery margin cannot jump like that: the RBOB price is a data error (a shifted decimal), not information.
- Late August 2017: gasoline crack up sharply and fading over weeks — a refinery outage (hurricane-type event): real information.

### E. Decision

Work in USD/bbl from now on. Do not compute any statistic on the gasoline crack before the outlier work of steps 2.4–2.5.

### F. Pitfalls and limits

- Mixing USD/gal and USD/bbl (a −63 "crack") or USD/t and USD/bbl.
- One conversion factor for all products: density differs.
- Settlement times differ (ICE Gasoil 17:30 London, NYMEX 14:30 New York, Brent 19:30 London): a "same-day" crack mixes prices taken hours apart (step 2.7).

### G. Interview defence

> **Q: "How do you compute a diesel crack from NYMEX ULSD?"**
>
> **A:** ULSD trades in dollars per gallon, so I multiply by 42 to get dollars per barrel and subtract the crude benchmark — here Brent. For ICE Gasoil, which is in dollars per tonne, I divide by about 7.45 barrels per tonne. In this data the diesel crack is around 17 dollars, with a clear winter peak near 19.5 against 14 in summer, which is the heating season. And before computing anything on the gasoline crack I'd flag the 863-dollar day: that's a bad RBOB print, not a margin.
