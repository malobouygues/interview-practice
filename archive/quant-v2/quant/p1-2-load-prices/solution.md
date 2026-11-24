### A. Reasoning — why each step, in this order

The loader is where silent errors are born: a guessed date format, a correction overwritten by the original, a holiday turned into a price. Each step answers one finding of 1.1, and the order matters because later steps rely on earlier ones (you cannot sort meaningfully before parsing dates, nor resolve corrections before sorting by load time).

### B. Theory

- Declaring missing-value codes at read time keeps numeric columns numeric and documents the codes in the code.
- `drop_duplicates()` first: identical rows carry no information. What remains duplicated on `date` has different values.
- `sort_values(["date", "loaded_at"])` then `drop_duplicates(subset="date", keep="last")`: within each date, the latest load is last. Without the sort, `keep="last"` keeps whatever happens to be last in the file — the PDF's warning: *keep='last' is only correct if the ingestion order is known*.
- No filling: the loader should return what the vendor said, nothing more.

### C. Implementation

{{code}}

### D. Interpretation (this file)

- 790 raw rows → 785 after removing identical rows → **783 dates** after resolving the two corrections.
- 2019-06-12: the first delivery said WTI 61.48, the correction (loaded 9 days later) 59.98 — the loader keeps **59.98**.
- Missing values left: Brent 23, WTI 27, Dubai 7 — mostly holidays on three different calendars, plus four values the vendor did not deliver.

### E. Decision

This frame is the input of the quality checks (1.3). It is still not "clean": a ×10 print and a negative WTI are in it, on purpose — the loader's job is to be faithful, not to judge values.

### F. Pitfalls and limits

- `keep="last"` on an unsorted file (keeps the late June-2020 batch row or the wrong delivery).
- `dayfirst` guessing instead of an explicit format.
- `fillna` or `dropna` in the loader: decisions about missing values depend on the analysis.
- Forgetting assertions: the next file may break the "one row per date" assumption without any error.

### G. Interview defence

> **Q: "Two rows have the same date with different prices. Which do you keep?"**
>
> **A:** It depends on why there are two. Here the second row was loaded nine days later: it's the vendor correcting a settlement, so I keep the latest load, using the `loaded_at` timestamp — not the position in the file, because the file isn't in time order. If two rows came from two different sources at the same time, I wouldn't pick one mechanically: I'd investigate and choose a reference source.
