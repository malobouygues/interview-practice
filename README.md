# Interview Practice

A small LeetCode-style judge that runs entirely on this computer, organised in two
learning tracks:

| Track | What it is | Content |
|---|---|---|
| **Past Interview Questions** | One question bank built from your two real screens, ranked by actual difficulty | 23 questions: 15 Millennium × AmplifyME cases + 8 Glencore questions (6 Python, 1 SQL, 1 written) |
| **Quantitative Methods** | Four commodity-desk situations (Gas & Power, Oil Products, Crude), built on *Carte mentale opérationnelle — Séries temporelles & recherche quantitative énergie* | 23 exercises: 20 code exercises with a written explanation, 3 written desk answers |

## Start

Double-click **`start.command`**, or in a terminal:

```bash
cd ~/code/interview-practice
python3 server.py
```

The app opens at <http://127.0.0.1:8790>. Stop it with Ctrl+C (or close the terminal window).
After updating the app, restart the server and reload the page: a banner tells you if the page
and the server come from different versions.

**Dependencies.** The server is standard-library Python 3.8+. The exercises need `pandas` and
`numpy` (Millennium cases, Quantitative Methods) and `statsmodels` (Quantitative Methods: OLS,
robust standard errors, ACF, ADF, Engle-Granger; it installs `scipy`, used for the Chow test).
`matplotlib` draws the charts of the Quantitative Methods *Test code* pads — optional: without it
every exercise still runs and is judged, only the charts are missing. SQL exercises use SQLite from
the standard library. `start.command` looks for a Python that has these and otherwise offers to
install them into a private `.venv` folder. Manually:
`python3 -m pip install pandas numpy statsmodels matplotlib`.

## Past Interview Questions

- **One list, ranked globally** from easiest to most challenging, grouped only by difficulty
  level: 1 Warm-up · 2 Foundations · 3 Intermediate · 4 Advanced · 5 Expert. Levels reflect the
  number of concepts, the reasoning and coding involved, the number of steps, the edge cases and
  how hard the solution is to defend; each problem page shows a one-line rationale and its place
  in the global ranking. Glencore and Millennium questions are interleaved where their difficulty
  is comparable (levels 1–2); levels 3–5 are Millennium cases because they are genuinely harder.
  Within a level, order follows prerequisites (e.g. Q11's ceiling division before Case 7's tick
  rounding; Q17 right after the SQL query it defends).
- **Source** is metadata only: a badge with the original number (Glencore Q8, Millennium Case 7…).
  An optional "Source" dropdown filters the list; the default is always the full ranking.
- **Removed:** the 9 Glencore multiple-choice questions (Q1–Q7, Q14, Q15), archived unchanged in
  `archive/glencore-mcq/`. They no longer load in the app; any attempt you made stays in your
  progress file.

## Quantitative Methods — four desk situations

Each project starts with a trader's question and a deliberately imperfect synthetic dataset, and
ends with an answer to that trader. The questions are realistic desk requests, not chapters about a
technique: each one needs a different mix of data work, exploratory analysis, statistics and market
reasoning. Training projects inspired by commodity-desk work — not actual interview questions or
internal methodologies of any firm.

| Project | The trader asks | Data work | Analysis | Exercises |
|---|---|---|---|---|
| **1 · Gas & Power** — weather, load and day-ahead prices | “Do cold, low-wind periods explain the price spikes, or is something else happening?” | local time vs UTC, 23/25-hour days, duplicates vs revisions, structural vs failed gaps, a stale daily state (`ffill(limit)` + age), irregular weather observations, zones | HDD / CDD with zone bases, load ~ HDD + CDD (OLS, intervals), **weather-adjusted load**, hourly boxplots, fat tails, ACF, a correlation made by the clock, residual load and the merit order | 6 |
| **2 · Oil Products** — diesel cracks and extreme observations | “The diesel crack has widened: tighter supply, a data problem, or a misleading relationship?” | a long vendor file with mixed units, duplicate keys, a frozen feed, a cents-for-dollars error, an impossible print, genuine zeros vs non-reporting, outage events to months | z / modified z / IQR and **iterative investigation** (correct, blank, keep, keep with sensitivity), OLS with units, residuals, **White test**, **HC3**, VIF | 5 |
| **3 · Crude** — what did the desk know at the time? | “I need to know what information was available when the market moved, not what the database says today.” | five timestamps, release calendar and delays, New York vs UTC, backfilled records, backward `merge_asof` on availability, vintages, **truncation tests** | event study, overlapping returns and **Newey-West (HAC)**, **train 2019–2022 / test 2023–2024**, baselines, MAE / RMSE, **expanding walk-forward** | 7 |
| **4 · Crude** — Brent, WTI: statistical or economic relationship? | “Are we simply correlating two trending price series?” | a clean research panel: the work is choosing transformations and tests | levels vs returns, Pearson vs Spearman, changing volatility, **stochastic vs deterministic trend vs seasonality**, ADF with justified `n / c / ct`, over-differencing, spurious regression and **Durbin-Watson**, Engle-Granger with the right critical values, structural break and Chow test (ECM as an optional extension) | 5 |

**From code to desk.** Inside each project the steps move from *knowing how to code* (load, clean,
join, estimate) to *knowing how to work on a desk* (what the numbers mean, what to tell the trader).
Each exercise page says where it sits: *Level 1: code it*, *Level 1 → 2: code it, then read it*,
*Level 2: desk judgement*. Code exercises have an **Explain** tab where the desk question is answered
with the numbers of your run; the last step of each project is the answer to the trader.

**Every exercise** follows the same frame: the desk's request (without giving the method away) →
what you have → what to find out → minimum theory → assumptions → your task. The hidden notes give
the reasoning, theory, implementation, interpretation with the dataset's numbers, the decision,
pitfalls and limits, and an interview defence.

**Charts.** The *Test code* pads draw the charts that answer a question — a boxplot of prices by
hour, a histogram of price changes, an ACF, actual vs weather-adjusted load, residuals against stocks,
errors over time out of sample. **Run** shows them under the output.

**Coding style.** Reference solutions are written the way a strong financial-engineering student
would write them: one logical step per line, explicit pandas operations, named domain variables,
comments that explain decisions, and the methodology visible in the code (information sets, shifts,
samples, tests). No classes, lambdas, apply chains or framework-like helpers; no backward fill,
interpolation or random split; every `ffill` has a limit; every as-of join looks backward.

**Data.** All datasets in `problems/quant/data/` are synthetic, generated with fixed seeds by
`generate_data.py`; `problems/quant/data/README.md` documents, for each one, how it was generated,
why it is realistic, what a correct analysis reveals and which mistake it is designed to expose —
including the zone base temperatures and the reference weather of Project 1, and the split, target,
decision time and feature availability of the out-of-sample test of Project 3. Nothing is downloaded.

**Scope.** Included: data ingestion and quality, missing values and outliers, units, long/wide,
calendars and time zones, point-in-time data (publication lags, availability, vintages, truncation
tests), exploratory analysis (time series, histograms, boxplots, seasonal plots, scatter plots,
rolling statistics, ACF, correlation), OLS with confidence intervals, VIF, White's test, HC3 and
Newey-West (HAC) standard errors, Durbin-Watson, ADF — the only formal unit-root test of the track —
detrending and differencing, spurious regression, Engle-Granger, the Chow test at a known date,
degree days and weather-adjusted load, and a simple out-of-sample validation (chronological split,
baselines, MAE / RMSE, expanding walk-forward). Excluded: classical forecasting model families
(autoregressive / moving-average models, exponential smoothing), multivariate and regularised
regression, machine learning and tuning, other unit-root, cointegration, residual-diagnostic and
unknown-date break tests, relative forecast-error metrics, and operational calculations (netbacks,
transport economics). `tools/check_all.py` checks both lists.

**Previous version.** The earlier, technique-by-technique version of this track (34 exercises) is
archived unchanged in `archive/quant-v2/`. Exercises that continue in the new track list their old
ids in `previous_ids`, so drafts and submissions carry over; the few with no successor are listed
as `retired_ids` in `problems/quant/set.json` and their progress stays in your file.

## Using it

| | |
|---|---|
| **Run** (⌘↵) | Executes your code, then the *Test code* pad below the editor, and shows what was printed — and the charts it drew. |
| **Submit** (⌘⇧↵) | Runs every test case and shows input, expected output, your output, prints and tracebacks for each. All tests green = solved. |
| **Written questions** | Write your answer (autosaved) → **Submit answer** → the reference answer appears in the *Solution* tab and a **self-review** checklist appears under your answer → tick what you covered → **Mark as mastered** or **Review again later**. Never graded automatically. |
| **Solution** tab | Hidden until you solve the problem (or ask to see it). |
| **Submissions** tab | Every attempt, with the code, answer text or explanation; any code can be loaded back into the editor. |

Your work is saved as you type in `data/progress.json`. An exercise that was renamed or rebuilt lists
its old ids (`previous_ids` in `meta.json`) and your progress under the old id is copied to the new one
(the old entry is kept; the old *Test code* pad is not copied, because it may read files that no
longer exist). *Reset this track* on the home page erases one track
only. To try things without touching your progress: `python3 server.py --data /some/folder`.

## Where the tests come from

- **Book** — input and expected output taken from your documents.
- **Rebuilt** — named or partly shown in your documents; missing values reconstructed so that the documented result still holds.
- **Added** — extra cases (edge cases, each rule of a statement, each bug of the debug cases, each data problem or statistical situation of the Quantitative Methods track), written out or computed by the reference solution.

## Checks

```bash
python3 server.py --check        # metadata of every problem
python3 tools/check_all.py       # everything: the unified interview bank; four desk situations and
                                 # their code-to-desk progression; a concept-coverage matrix; allowed
                                 # vs excluded techniques; plain, look-ahead-free
                                 # reference code; derived data layers; the numbers quoted by the
                                 # notes; mutated solutions rejected (random split, unpurged labels,
                                 # forward joins...); every reference solution accepted, every
                                 # starter rejected, every pad running and drawing its charts;
                                 # progress file; written-answer flow
```

## Layout

```
server.py              local web server (standard library only, listens on 127.0.0.1)
judge/runner.py        runs one submission in a separate process (6 s per test)
web/                   the interface (editor: CodeMirror 5, vendored — works offline)
problems/tracks.json   the two learning tracks and how each is ordered
problems/<folder>/set.json
    track              "interview" or "quant"
    source             shown as a badge (Glencore, Millennium × AmplifyME)
    projects           (quant) the four desk situations: area, the trader's question, market, data work,
                       files, concepts;  retired_ids: old exercises with no successor
problems/<folder>/<problem>/
    meta.json          number, title, type (code | sql | open), difficulty (1-5), and
                       interview: sequence (tie-break inside a level), difficulty_why, book_difficulty
                       quant: project, step, level (technical | mixed | desk), architectures (A01-A13 of
                              the source document), concepts, data (datasets copied to ./data for the run),
                              previous_ids, explain {prompt, rubric} for code, rubric for written questions
    statement.md       the question
    starter.py         code shown in the editor      (starter.sql for SQL)
    test_code.py       initial content of the Test code pad
    solution.py        reference solution             (solution.sql for SQL)
    solution.md        explanation / interview defence
    tests.py           FUNCTION = "name";  TESTS = [{name, origin, args, expected | raises}, …]
    dataset.sql        table contents for SQL questions (run on SQLite)
problems/quant/data/   synthetic datasets + generate_data.py + README
archive/glencore-mcq/  the 9 Glencore multiple-choice questions, removed from the app
archive/quant-v2/      the previous version of the Quantitative Methods track (not loaded)
sources/               your four original Word documents
tools/check_all.py     end-to-end checks
data/                  your progress (created on first use)
```

To add a problem, copy a folder, edit the files and reload the page — problems are read from disk
on every request; `python3 server.py --check` tells you if a field is missing. In `tests.py`,
`args` is a function returning the arguments **in the function's parameter order**; leave
`expected` out to have it computed by `solution.py`.
