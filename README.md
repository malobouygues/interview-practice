# Interview Practice

A small LeetCode-style judge that runs entirely on this computer, organised in two
learning tracks:

| Track | What it is | Content |
|---|---|---|
| **Past Interview Questions** | One question bank built from your two real screens, ranked by actual difficulty | 23 questions: 15 Millennium × AmplifyME cases + 8 Glencore questions (6 Python, 1 SQL, 1 written) |
| **Quantitative Methods** | Four crude / oil-products research projects, built from *Carte mentale opérationnelle — Séries temporelles & recherche quantitative énergie* | 34 exercises: 29 code exercises with a written explanation, 5 written debriefs |

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
`numpy` (Millennium cases, Quantitative Methods) and `statsmodels` (Quantitative Methods: ADF,
OLS, Engle-Granger; it installs `scipy`, used for the Chow test's F distribution). SQL exercises
use SQLite from the standard library. `start.command` looks for a Python that has these and
otherwise offers to install them into a private `.venv` folder. Manually:
`python3 -m pip install pandas numpy statsmodels`.

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

## Quantitative Methods — four projects

Each project is one research question on a desk-like synthetic dataset, with its own
data-preparation challenge, and ends with a written defence. Training projects inspired by the
analytical work of a crude / oil-products desk — not actual interview questions or internal
methodologies of any firm.

| Project | Research question | Data work | Statistics / econometrics |
|---|---|---|---|
| **1 · Crude oil: building and understanding a market dataset** (8) | Can a raw vendor file of Brent, WTI, Dubai (2019–2021) be trusted, and what do prices and spreads say? | profiling a raw CSV, data dictionary, types, day-first dates, duplicates vs corrections, holiday calendars, quality rules (error vs event), an idempotent SQLite store | mean / median / variance / quantiles, skewness, kurtosis, differences, % changes, log returns, spreads, Pearson vs Spearman, correlation ≠ causality |
| **2 · Oil products: missing data, outliers and features** (8) | What moves the US diesel crack, and which variables can be built without look-ahead? | unit conversion and cracks, leading / interior / trailing gaps, stale feeds, missing vs zero (long → wide), z-score / modified z-score / IQR, error vs genuine shock, lags, rolling and calendar features | seasonality, levels vs changes, feature screening, lead-lag and settlement times |
| **3 · Point-in-time data and temporal alignment** (7) | Could a desk have used stock and demand data at the time? | observation / publication / availability / ingestion dates, release calendars, backward `merge_asof`, vintages and as-of views, pseudo vs genuine point-in-time, truncation tests | how misalignment fakes predictability, how revisions and lags overstate relationships |
| **4 · Oil markets: econometric research and model selection** (11) | Is WTI tied to Brent by a long-run equilibrium, which simple model fits, and did it survive the end of the export ban? | a clean research panel: the work is choosing transformations, specifications and tests | OLS inference (SE, t, p, CI), model selection (adjusted R², AIC / BIC, multicollinearity, parsimony), ADF (`c` / `ct` / `n`, lags, power, breaks), I(0) / I(1), detrend vs difference, spurious regression, Engle-Granger with correct critical values, basic ECM and half-life, sub-periods and Chow test, research defence |

**How to navigate.** Pick the *Quantitative Methods* card on the home page: exercises are grouped
by project (research question, market, data work and files shown above each project) and
numbered `project.step`. Work in order inside a project; the ‹ › buttons follow the path.

**Every exercise** follows the same frame: context → objective → minimum theory → assumptions →
task in the statement; the hidden solution gives the reasoning, theory, implementation,
interpretation with the dataset's numbers, decision, pitfalls and limits, and an interview
question with a model answer. Code exercises have an **Explain** tab for your written
interpretation; once solved, it shows the key points of a strong explanation as a checklist.

**Coding style.** Reference solutions are written the way a strong financial-engineering student
would write them: one logical step per line, explicit pandas operations, named domain variables,
the methodology visible in the code (information sets, shifts, samples, tests) and no classes,
lambdas or framework-like helpers. `tools/check_all.py` scans them for this.

**Data.** All datasets in `problems/quant/data/` are synthetic, generated with fixed seeds by
`generate_data.py`, and several are deliberately imperfect (see `problems/quant/data/README.md`).
Nothing is downloaded.

**Scope.** Included: data ingestion and basic SQLite, data quality, missing values, outlier scores,
point-in-time data (publication lags, availability, vintages, truncation tests), feature
engineering (lags, rolling and calendar features, always shifted to respect the information set),
descriptive statistics and correlation, OLS inference and simple model selection, ADF — the only
formal unit-root test of the track — Engle-Granger, a basic single-equation ECM and the Chow test
at a known date. Excluded: classical forecasting models (AR/MA families, exponential smoothing),
multivariate and advanced regression, machine learning, other unit-root, cointegration,
residual-diagnostic and unknown-date break tests, forecasting strategies, validation schemes and
error metrics, and operational calculations (netbacks, transport economics). `tools/check_all.py`
scans the track for the excluded topics.

## Using it

| | |
|---|---|
| **Run** (⌘↵) | Executes your code, then the *Test code* pad below the editor, and shows what was printed. |
| **Submit** (⌘⇧↵) | Runs every test case and shows input, expected output, your output, prints and tracebacks for each. All tests green = solved. |
| **Written questions** | Write your answer (autosaved) → **Submit answer** → the reference answer appears in the *Solution* tab and a **self-review** checklist appears under your answer → tick what you covered → **Mark as mastered** or **Review again later**. Never graded automatically. |
| **Solution** tab | Hidden until you solve the problem (or ask to see it). |
| **Submissions** tab | Every attempt, with the code, answer text or explanation; any code can be loaded back into the editor. |

Your work is saved as you type in `data/progress.json`. Problem ids never change; an exercise that
was renamed lists its old ids (`previous_ids` in `meta.json`) and your progress under the old id is
copied to the new one — the old entry is kept. *Reset this track* on the home page erases one track
only. To try things without touching your progress: `python3 server.py --data /some/folder`.

## Where the tests come from

- **Book** — input and expected output taken from your documents.
- **Rebuilt** — named or partly shown in your documents; missing values reconstructed so that the documented result still holds.
- **Added** — extra cases (edge cases, each rule of a statement, each bug of the debug cases, each data problem or statistical situation of the Quantitative Methods track), written out or computed by the reference solution.

## Checks

```bash
python3 server.py --check        # metadata of every problem
python3 tools/check_all.py       # everything: one unified interview bank, four projects and their
                                 # coverage, ADF only, excluded topics absent, plain reference code,
                                 # the results quoted by the notes, every reference solution accepted
                                 # by the judge, every starter rejected, test-code pads, progress
                                 # file, written-answer flow
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
    projects           (quant) the four projects: research question, market, data work, files, concepts
problems/<folder>/<problem>/
    meta.json          number, title, type (code | sql | open), difficulty (1-5), and
                       interview: sequence (tie-break inside a level), difficulty_why, book_difficulty
                       quant: project, step, architectures (A01-A07 of the source document), concepts,
                              data (datasets copied to ./data for the run), previous_ids,
                              explain {prompt, rubric} for code, rubric for written questions
    statement.md       the question
    starter.py         code shown in the editor      (starter.sql for SQL)
    test_code.py       initial content of the Test code pad
    solution.py        reference solution             (solution.sql for SQL)
    solution.md        explanation / interview defence
    tests.py           FUNCTION = "name";  TESTS = [{name, origin, args, expected | raises}, …]
    dataset.sql        table contents for SQL questions (run on SQLite)
problems/quant/data/   synthetic datasets + generate_data.py + README
archive/glencore-mcq/  the 9 Glencore multiple-choice questions, removed from the app
sources/               your four original Word documents
tools/check_all.py     end-to-end checks
data/                  your progress (created on first use)
```

To add a problem, copy a folder, edit the files and reload the page — problems are read from disk
on every request; `python3 server.py --check` tells you if a field is missing. In `tests.py`,
`args` is a function returning the arguments **in the function's parameter order**; leave
`expected` out to have it computed by `solution.py`.
