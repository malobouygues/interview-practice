### A. Reasoning — fix the clock before anything else

Every later number — a daily average, a MWh total, a price profile by hour — silently assumes one row per delivery hour. A vendor file in local wall-clock time breaks that assumption twice a year, and a re-sent or corrected record breaks it whenever it happens. So the first job is not statistics: it is to choose a key with no ambiguity (UTC), then to decide, record by record, which version to trust.

### B. Theory (PDF A01-C frequency, A02-C quality control, A03-C order of cleaning operations)

- **Delivery period vs timestamp.** The row describes the interval [start, start + 1 h). The local date is a *label*; UTC is the *key*.
- **Daylight saving.** CET is UTC+1, CEST is UTC+2. Last Sunday of March: 23 hours. Last Sunday of October: 25 hours, the 02:00 hour twice. A local timestamp without its offset is ambiguous one hour a year and impossible one hour a year.
- **Copies vs versions.** An exact copy carries no information → drop it. Two versions of the same key are a *correction*: the latest version wins, and the number of corrections is worth reporting.
- **Order** (A03-C): types and timezone first, sort, then duplicates — never deduplicate on a key you have not standardised.

### C. Implementation

`pd.to_datetime(local + offset, format="%Y-%m-%d %H:%M%z", utc=True)` turns the wall-clock text and its offset into one UTC instant. `drop_duplicates()` removes the copies. Sorting on (`delivery_start_utc`, `loaded_at`) then `drop_duplicates(subset="delivery_start_utc", keep="last")` keeps the latest version. `tz_convert("Europe/Paris")` gives the market's local view; `tz_localize(None).normalize()` turns it into a plain date label.

### D. Interpretation (this dataset)

- 17,553 rows → 6 exact copies dropped → 3 delivery hours with two versions → **17,544 delivery hours** = 727 days × 24 + 2 × 23 (26 Mar 2023, 31 Mar 2024) + 2 × 25 (29 Oct 2023, 27 Oct 2024).
- Deduplicating on `delivery_start_local` alone flags **11** rows instead of 9: it would delete the two genuine second 02:00 hours.
- The three corrected records: 21 Nov 2023 18:00, first **772.50** then **77.25** €/MWh (×10); 12 Mar 2024 19:00, 23.82 → 32.82 (two digits swapped); 3 Jun 2024 13:00, solar blank → 12,866 MW.

### E. Decision

Trust the UTC-keyed table with the latest versions, and say so: “3 records were corrected by the vendor; the 772 €/MWh print of 21 November was a decimal error, not a spike.” The question the trader asked is about *real* spikes — this step just removed one fake one.

### F. Pitfalls and limits

- Parsing `delivery_start_local` without the offset: pandas either raises on the ambiguous hour or silently picks one.
- `pd.date_range` in local time to “check completeness” invents a 02:00 hour in March.
- `keep="last"` without sorting on `loaded_at` keeps whatever happens to be last in the file.
- The latest version is not always the right one (a vendor can “correct” wrongly). Keep the count and, for large changes, look.

### G. Interview defence

*“Why convert to UTC if traders think in local time?”* — Because UTC is the only clock where every hour exists exactly once: duplicates, gaps, rolling windows and joins are all defined on it. I keep the local date and hour as labels for grouping by market day and for presenting results, but I never use them as a key. On DST days that is the difference between 25 real hours and 24 hours plus a deleted one.
