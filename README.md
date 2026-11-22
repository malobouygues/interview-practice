# Interview Practice

A small LeetCode-style judge that runs entirely on this computer, organised in two
learning tracks:

| Track | What it is | Content |
|---|---|---|
| **Past Interview Questions** | One question bank built from your two real screens, ranked by actual difficulty | 23 questions: 15 Millennium × AmplifyME cases + 8 Glencore questions (6 Python, 1 SQL, 1 written) |
| **Quantitative Methods** | A practical path through statistical diagnosis, correlation, stationarity tests, cointegration and stability, built from *Carte mentale opérationnelle — Séries temporelles & recherche quantitative énergie* | 4 progressive commodity cases, 19 exercises (14 code + explanation, 5 written debriefs) |

## Start

Double-click **`start.command`**, or in a terminal:

```bash
cd ~/code/interview-practice
python3 server.py
```

The app opens at <http://127.0.0.1:8790>. Stop it with Ctrl+C (or close the terminal window).

**Dependencies.** The server itself is standard-library Python 3.8+. The exercises need:

- `pandas` and `numpy` — Millennium cases and Quantitative Methods;
- `statsmodels` (which brings `scipy`) — Quantitative Methods only (ADF, KPSS, OLS, Engle-Granger, Chow p-values). **New in this version.**

`start.command` looks for a Python that has all three and, if there is none, offers to
install them into a private `.venv` folder here. Otherwise: `python3 -m pip install pandas numpy statsmodels`.
If macOS refuses to open `start.command`, run `chmod +x start.command` once.

## Past Interview Questions

- **One list, ranked globally** from easiest to most challenging. Glencore and Millennium
  questions are interleaved according to difficulty, never shown as two sections.
- **Difficulty** is an explicit level from 1 to 5 — 1 Warm-up · 2 Foundations · 3 Intermediate ·
  4 Advanced · 5 Expert — judged on the number of concepts, the reasoning and coding involved,
  the number of steps, the edge cases and how hard the solution is to defend. Each problem
  page shows a one-line rationale for its level. Within a level, order follows prerequisites
  (e.g. the written Q17 comes right after the SQL query it asks you to defend; each Millennium
  *Debug* case follows the case it debugs).
- **Source** is metadata: every question carries a badge — *Glencore* or *Millennium × AmplifyME* —
  with its original number (Q8, Case 7…). The source filter is optional; the default view is the
  global ranking.
- **Removed:** the 9 Glencore multiple-choice questions (Q1–Q7, Q14, Q15). They are archived,
  unchanged, in `archive/glencore-mcq/` (see its README) and no longer load in the app.

## Quantitative Methods

Organised as **progressive cases**, not chapters: each case is one research question on
synthetic commodity data, and each step needs the previous one.

| Case | Research question | Steps |
|---|---|---|
| 1 · Diagnosing one gas price series | TTF rose from 18 to 33 €/MWh: what kind of series is it — prices or returns? | describe (mean, median, variance, skewness, kurtosis) → diff / % / log returns → weak stationarity & random walk → ADF → KPSS and the joint reading → deterministic vs stochastic trend (with a seasonal demand series) → written defence |
| 2 · Two related markets: Brent and WTI | How strong is the link, and which statistics survive trending prices? | economic mechanism first → Pearson / Spearman, levels vs returns → bivariate OLS → spurious regression → written defence (correlation ≠ causality) |
| 3 · Testing the long-run Brent–WTI relationship | Is there an equilibrium, and how fast does WTI return to it? | orders of integration → Engle-Granger step by step (and why its critical values differ) → error correction model, half-life → "WTI looks cheap — trade it?" |
| 4 · Did the relationship survive a structural change? | Is 2012–2019 one relationship or two (end of the US export ban)? | sub-period comparison and what a break does to cointegration tests → Chow test at a known date, with placebo dates → final written defence |

**How to navigate.** Pick the *Quantitative Methods* card on the home page: exercises are
grouped by case (research question, dataset and concepts shown above each case) and
numbered `case.step`. Work them in order; the case banner on each page reminds you where you
are. The ‹ › buttons move along the path.

**Every exercise** follows the same frame: context → objective → minimum theory → assumptions →
task in the statement; the hidden solution gives the reasoning, theory, implementation,
interpretation with the dataset's numbers, decision, limitations and pitfalls, and an
interview question with a model answer.

**Code + explanation.** Coding exercises have an **Explain** tab next to *Test code*: write your
interpretation there (saved as you type, stored with your submission). Once the tests pass — or
you reveal the solution — the key points of a strong explanation appear as a checklist.

**Data.** All datasets in `problems/quant/data/` are **synthetic**, generated with fixed seeds
by `generate_data.py` so that each phenomenon is observable (see `problems/quant/data/README.md`).
Nothing is downloaded; nothing is presented as a market observation.

**Scope.** The track deliberately excludes classical forecasting models, multivariate / advanced
regression and machine learning, residual-diagnostic and unknown-date break tests, forecasting
frameworks and error metrics, and the operational / data-engineering parts of the source document
(netbacks, point-in-time data, feature engineering, outlier methods, SQL). `tools/check_all.py`
scans the track for those topics.

## Using it

| | |
|---|---|
| **Run** (⌘↵) | Executes your code, then the *Test code* pad below the editor, and shows what was printed. |
| **Submit** (⌘⇧↵) | Runs every test case and shows input, expected output, your output, prints and tracebacks for each. All tests green = solved. |
| **Written questions** | Write your answer (autosaved) → **Submit answer** → the reference answer appears in the *Solution* tab and a **self-review** checklist of key points appears under your answer → tick what you covered → **Mark as mastered** or **Review again later**. Written answers are never graded automatically. |
| **Solution** tab | Hidden until you solve the problem (or ask to see it). |
| **Submissions** tab | Every attempt, with the code, answer text or explanation; any code can be loaded back into the editor. |

Your work is saved as you type. Progress, drafts and submissions live in `data/progress.json`;
problem ids never change, so progress made before the reorganisation is kept (archived MCQ
attempts stay recorded under their original id). *Reset this track* on the home page erases one
track only. To try things without touching your progress: `python3 server.py --data /some/folder`.

## Where the tests come from

Each test carries a label:

- **Book** — input and expected output are taken from your documents.
- **Rebuilt** — the document names the test or shows it partly; missing values were reconstructed so that the documented result still holds.
- **Added** — extra cases (edge cases, each rule of the statement, each bug of the debug cases, each statistical situation of the Quantitative Methods track). Their expected output is written in the test or computed by the reference solution.

## Checks

```bash
python3 server.py --check        # metadata of every problem
python3 tools/check_all.py       # everything: metadata, ranking, exclusions, every reference solution
                                 # accepted by the judge, every starter rejected, test-code pads,
                                 # the outcomes the teaching notes quote, progress file, written-answer flow
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
    cases              (quant) the ordered cases: title, research question, data, concepts
problems/<folder>/<problem>/
    meta.json          number, title, type (code | sql | open), difficulty (1-5), and
                       interview: sequence (tie-break inside a level), difficulty_why, book_difficulty
                       quant: case, step, concepts, data (datasets copied to ./data for the run),
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

To add a problem, copy a folder, edit the files and reload the page — problems are read from
disk on every request; `python3 server.py --check` tells you if a field is missing.
In `tests.py`, `args` is a function returning the arguments **in the function's parameter order**;
leave `expected` out to have it computed by `solution.py`.
