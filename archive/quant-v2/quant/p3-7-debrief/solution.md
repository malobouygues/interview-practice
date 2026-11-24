### Reference answer

> **Neither claim survives as stated. The stock "signal" disappears once the reports are dated at their release, and the demand–crack link is real but much weaker than the revised-data chart suggests.**
>
> Every number has several dates. The weekly stock level describes the week to Friday, is published the following Wednesday at 10:30 New York — Thursday after a holiday — and most of our history was loaded into the database in a backfill in January 2019. The economics are indexed on the observation date, but anything about "what we knew" must use the availability time. Joined on the week-ending date, the stock number is used before its release on about 630 of 1,042 days. That alone produces the −0.19 correlation with next week's WTI return. Aligned on the release time, the correlation is 0.02. The market does react to the report — about −0.5 correlation on the release day itself — but that reaction is priced at publication, not tradable in advance.
>
> Monthly demand is published about two months late and revised: first estimates are revised up by about 145 kb/d on average. The chart that gives 0.83 compares each month's crack with the same month's final demand growth, a number nobody had at the time. Rebuilding the view available at each month-end from the vintages, the correlation is 0.59, and real-time growth even had the wrong sign in 10 of 46 months.
>
> Safeguards: backward as-of joins on availability, with a tolerance and assertions that nothing was used before its release; as-of views from the vintage table; and a truncation test at several dates on every feature pipeline. On a deliberately leaky builder, that test catches centred windows, full-sample normalisation and negative shifts.
>
> Wording: the demand result is point-in-time, because we have vintages. If we only had today's revised history, I would call it pseudo point-in-time and say performance is probably overstated. Limits: daily settlements cannot show the intraday reaction, the monthly sample is short, and correlation is not causation. Next, store our own vintages for every source, starting now.

### What makes this a strong answer

- **Each claim re-tested** with the correct information set, with the before/after numbers.
- **The mechanism of the error** explained (publication lag inside a forward window; revisions + lag in a chart).
- **Safeguards that generalise** (as-of joins, vintages, truncation test) and their limits.
- **Precise vocabulary** — point-in-time vs pseudo point-in-time — tied to whether vintages exist.

### Common weaknesses

- "We used merge_asof so it's point-in-time" — the key and the vintage matter.
- Concluding that stocks do not affect prices (they do — on the release day).
- Presenting 0.83 as usable predictive information.
