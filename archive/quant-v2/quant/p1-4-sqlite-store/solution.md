### A. Reasoning — why a database at all, and why this one

A research dataset is re-loaded many times (new deliveries, corrections). The structure must make the two classic accidents impossible: a date stored twice, and a re-run that appends everything again. A primary key and an upsert do that in two lines. SQLite ships with Python: no server, no dependency.

### B. Theory

- **Primary key** = uniqueness enforced by the database, not by discipline.
- **Idempotent load** (`INSERT OR REPLACE`, an "upsert"): running it once or ten times gives the same state.
- **Aggregation follows the economics**: a price or a spread is a level → monthly mean (or month-end value); a physical flow would be summed (Project 2).
- `NULL` handling: `AVG` ignores `NULL`s, so without the `WHERE` clause the two averages of a month could be computed on different days.

### C. Implementation

{{code}}

The rows are built with a plain loop over `iterrows()`: slower than vectorised code, but the table has 783 rows and the loop shows exactly what is inserted.

### D. Interpretation (this dataset)

- 36 months; a normal month shows Brent–WTI around 3–4 USD/bbl and Brent–Dubai around 1.2 USD/bbl (between 0.1 and 2.7).
- **2020-04**: Brent–WTI averages ≈ **10.1** USD/bbl. The storage glut widened the spread, and the single expiry day (−35.90 for WTI, a 55 USD/bbl spread) adds about 2.4 USD/bbl to the monthly average on its own (7.7 without it; median 7.8).
- Loading twice leaves 783 rows: the load is idempotent.

### E. Decision

Keep the database as the single source for the project (raw file → clean layer → table). For April 2020, report the median or the average excluding the expiry day next to the plain average.

### F. Pitfalls and limits

- Plain `INSERT` re-run → duplicated rows that silently double-weight days.
- Storing dates as free text (`"03/04/2020"`): string sorting and `substr` grouping become wrong; ISO `YYYY-MM-DD` sorts correctly as text.
- Summing prices to get a monthly figure.
- SQLite is right for a small research store; it is not a multi-user production database.

### G. Interview defence

> **Q: "How do you make sure re-running your data load doesn't corrupt the dataset?"**
>
> **A:** I make uniqueness a property of the storage: the table has the date as primary key, and the load uses an upsert — insert or replace — so loading the same file twice gives exactly the same table. Then aggregations follow the economics: a spread is a price, so monthly figures are averages, and I only average days where both legs exist. That's how I can say Brent–WTI averaged about 10 dollars in April 2020 — with the caveat that one expiry day drives a good part of it.
