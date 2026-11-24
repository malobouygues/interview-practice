#!/usr/bin/env python3
"""End-to-end checks of the question banks and the app — run before trusting a change.

    python3 tools/check_all.py            everything (a couple of minutes)
    python3 tools/check_all.py --fast     skip the judge runs (sections 8 and 9)

What it verifies
  1. metadata of every problem is valid (same rules as  server.py --check)
  2. Past Interview Questions: one bank, 15 Millennium + 8 Glencore, no MCQ, global difficulty
     order with both sources interleaved, a source badge on every question, no source-based
     sections or navigation in the interface
  3. Quantitative Methods: four desk situations covering Gas & Power, Oil Products and Crude;
     contiguous steps; each project mixes data, exploratory and analytical work and moves from a
     technical first step to a desk judgement; every exercise opens with the desk's request
     (without giving the method away) and has a rubric that uses the dataset's numbers
  4. a concept-coverage matrix (each concept -> exercises -> evidence in their files); ACF,
     Durbin-Watson, White, HC3, HAC and out-of-sample validation allowed; HAC only where the
     overlap that justifies it is explained; excluded topics absent; KPSS absent everywhere
  5. plain reference code and temporal safety: no classes / lambdas / apply chains; no backward
     fill, interpolation or random split; every ffill has a limit; every merge_asof looks
     backward (on availability in Project 3); the out-of-sample split is 2019-2022 / 2023-2024
     with purged labels
  6. every derived data layer is exactly what the reference solutions return
  7. the numbers quoted by the teaching notes still hold on the data (all four projects)
  8. the tests reject typical mistakes: mutated reference solutions (random split, unpurged
     labels, forward-looking joins, unlimited ffill, first version kept, HAC without overlap...)
  9. every reference solution is ACCEPTED by the real judge, every starter is NOT, every
     "Test code" pad runs without error or warning, and the pads that plot produce charts
 10. the progress file loads; every recorded id is active, archived, carried over to a renamed
     exercise ("previous_ids") or listed as retired; a carried-over draft is visible
 11. the written-answer flow (draft -> submit -> self-review) works, on a scratch copy of the
     progress file (your real progress is never touched)

Exit code 0 when everything passes.
"""
import copy
import os
import re
import shutil
import sys
import tempfile
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import server  # noqa: E402

FAILURES = []


def check(cond, message):
    if not cond:
        FAILURES.append(message)
    return cond


def section(title):
    print("\n== " + title)


# ---------------------------------------------------------------------------
def check_metadata():
    section("1. metadata")
    issues = server.validate()
    for line in issues:
        check(False, "metadata: " + line)
    print("   %d problems, %d issue(s)" % (len(server.list_problems()), len(issues)))


def check_interview_track():
    section("2. Past Interview Questions")
    tracks = [t["id"] for t in server.list_tracks()]
    check(tracks == ["interview", "quant"], "expected exactly two tracks, got %s" % tracks)
    probs = [p for p in server.list_problems() if p["track"] == "interview"]
    mill = [p for p in probs if p["set"] == "millennium"]
    glen = [p for p in probs if p["set"] == "glencore"]
    check(len(mill) == 15, "expected 15 Millennium exercises, found %d" % len(mill))
    check(len(glen) == 8, "expected 8 Glencore exercises (6 code, 1 SQL, 1 written), found %d" % len(glen))
    kinds = sorted(p["type"] for p in glen)
    check(kinds == ["code"] * 6 + ["open", "sql"], "Glencore types are %s" % kinds)
    check(not [p for p in probs if p["type"] == "mcq"], "an MCQ is still active")
    archive = os.path.join(ROOT, "archive", "glencore-mcq")
    archived = [a for a in sorted(os.listdir(archive)) if os.path.isdir(os.path.join(archive, a))]
    check(len(archived) == 9, "expected 9 archived Glencore MCQs, found %d" % len(archived))
    for a in archived:
        meta = server.read_json(os.path.join(archive, a, "meta.json")) or {}
        check(meta.get("type") == "mcq", "archived %s is not an MCQ" % a)

    diffs = [p["difficulty"] for p in probs]
    check(diffs == sorted(diffs), "interview list is not ordered by difficulty: %s" % diffs)
    pattern = "".join("G" if p["set"] == "glencore" else "M" for p in probs)
    first_level = {p["set"] for p in probs if p["difficulty"] == 1}
    check(first_level == {"glencore", "millennium"}, "level 1 should contain both sources")
    check("GM" in pattern[:10] and "MG" in pattern[:10], "sources are not interleaved: %s" % pattern)
    for p in probs:
        check(p.get("source") in ("Glencore", "Millennium × AmplifyME"), "%s: source %r" % (p["id"], p.get("source")))
        check(bool(p.get("difficulty_why")), "%s: no difficulty rationale" % p["id"])
    order = {p["id"]: i for i, p in enumerate(probs)}
    check(order["glencore/q17-ai-follow-up-question"] > order["glencore/q16-loyal-and-satisfied-employees"],
          "Q17 must come after the SQL query it defends")

    # the interface: one ranked list, grouped by level, never by source
    app_js = server.read_text(os.path.join(ROOT, "web", "app.js"))
    check("drawLevels" in app_js, "the interview list is not rendered by difficulty level")
    check("data.sets.forEach" not in app_js, "app.js still renders one section per source")
    check('seg("source"' not in app_js, "the source filter is still a tab-like segmented control")
    check("p.group" not in app_js, "the problem page still shows the original book's section")
    print("   Millennium %d · Glencore %d · archived MCQs %d" % (len(mill), len(glen), len(archived)))
    print("   ranking: %s" % " ".join(s + str(d) for s, d in zip(pattern, diffs)))


# ---------------------------------------------------------------------------
# Quantitative Methods: structure, progression, coverage, scope
# ---------------------------------------------------------------------------
QUANT = os.path.join(ROOT, "problems", "quant")
DATA_DIR = os.path.join(QUANT, "data")
AREAS = {"p1": "Gas & Power", "p2": "Oil Products", "p3": "Crude", "p4": "Crude"}
STAGES = ["technical", "mixed", "desk"]
# PDF architectures grouped by kind of work: every project needs all three
WORK = {"data": {"A01", "A02", "A03", "A04"}, "exploratory": {"A05"},
        "analytical": {"A06", "A07", "A08", "A09", "A10", "A11"}}


def quant_problems():
    return [p for p in server.list_problems() if p["track"] == "quant"]


def quant_text(pid, names=("statement.md", "solution.py", "test_code.py", "solution.md", "meta.json")):
    _meta, path = server.load_meta(pid)
    return "\n".join(server.read_text(os.path.join(path, n)) for n in names)


def check_quant_structure():
    section("3. Quantitative Methods: four desk situations, progression from code to desk")
    qset = server.read_json(os.path.join(QUANT, "set.json"))
    projects = qset["projects"]
    check([p["id"] for p in projects] == ["p1", "p2", "p3", "p4"], "expected exactly four projects p1-p4")
    areas = {p["id"]: p.get("area") for p in projects}
    check(areas == AREAS, "project areas %s" % areas)
    check({"Gas & Power", "Oil Products", "Crude"} <= set(areas.values()), "a commodity area is missing")
    for p in projects:
        check(p.get("question", "").startswith("“"), "%s: the project must open with the trader's question" % p["id"])
    probs = quant_problems()
    check(19 <= len(probs) <= 24, "expected about 19-23 exercises, found %d" % len(probs))
    for proj in projects:
        items = sorted([p for p in probs if p["project"] == proj["id"]], key=lambda p: p["step"])
        steps = [p["step"] for p in items]
        check(steps == list(range(1, len(items) + 1)), "%s: steps %s not contiguous" % (proj["id"], steps))
        check(5 <= len(items) <= 7, "%s: %d exercises" % (proj["id"], len(items)))
        levels = [p.get("level") for p in items]
        check(all(l in STAGES for l in levels), "%s: unknown level in %s" % (proj["id"], levels))
        check(levels[0] == "technical", "%s: the project should start with a technical step" % proj["id"])
        check(levels[-1] == "desk", "%s: the project should end with a desk judgement" % proj["id"])
        ranks = [STAGES.index(l) for l in levels if l in STAGES]
        check(ranks == sorted(ranks), "%s: the progression goes back from desk to technical: %s" % (proj["id"], levels))
        archs = set()
        for p in items:
            archs |= set(p.get("architectures", []))
        for kind, group in WORK.items():
            check(archs & group, "%s: no %s work (architectures %s)" % (proj["id"], kind, sorted(archs)))
        for p in items:
            meta, _ = server.load_meta(p["id"])
            rubric = meta.get("rubric") or (meta.get("explain") or {}).get("rubric") or []
            check(len(rubric) >= 5, "%s: rubric with %d points" % (p["id"], len(rubric)))
            if p["level"] in ("mixed", "desk"):
                with_numbers = [r for r in rubric if re.search(r"\d", r)]
                check(len(with_numbers) >= 3, "%s: an interpretation rubric must use the dataset's numbers" % p["id"])
            statement = server.read_text(os.path.join(server.problem_dir(p["id"]), "statement.md"))
            check("### The desk asks" in statement, "%s: the statement does not start from the desk's request" % p["id"])
            first_line = statement.split("### The desk asks", 1)[-1].strip().split("\n")[0]
            for method in ("merge_asof", "ADF", "HAC", "White", "HC3", "OLS", "z-score", "ffill"):
                check(method not in first_line, "%s: the request gives the method away (%s)" % (p["id"], method))
            notes = server.read_text(os.path.join(server.problem_dir(p["id"]), "solution.md"))
            for part in ("### A.", "### D.", "### E.", "### F.", "### G.") if p["type"] == "code" else ("### Reference answer",):
                check(part in notes, "%s: teaching note without section %s" % (p["id"], part))
        print("   %s %-13s %d exercises  %s" % (proj["id"], areas[proj["id"]], len(items),
                                                " -> ".join("%s:%s" % (p["number"], p["level"][0]) for p in items)))


# concept -> exercises that teach it, each with a piece of evidence that must be in its files
COVERAGE = {
    "read_csv / inspection (head, info, describe)": [("p1-1-delivery-hours", r"\.info\(\)"), ("p2-1-cracks", r"\.head\(")],
    "types and datetime parsing": [("p1-1-delivery-hours", r"%z"), ("p3-1-five-dates", r"tz_localize\(NEW_YORK\)")],
    "UTC vs local market time, DST days": [("p1-1-delivery-hours", r"tz_convert\(MARKET_TZ\)"), ("p1-3-degree-days", r"hours_in_day")],
    "duplicate rows vs duplicate keys / revisions": [("p1-1-delivery-hours", r'keep="last"'), ("p2-1-cracks", r"duplicated\(subset")],
    "units and currencies": [("p2-1-cracks", r"BARRELS_PER_TONNE")],
    "long vs wide": [("p2-1-cracks", r"\.pivot\("), ("p2-3-imports-and-outages", r"\.pivot\(")],
    "groupby": [("p1-3-degree-days", r"groupby\(\[\"zone\""), ("p2-3-imports-and-outages", r"groupby\(\[\"month\", \"importer\"\]")],
    "resample / to_period monthly alignment": [("p2-3-imports-and-outages", r"to_period\(\"M\"\)"), ("p1-3-degree-days", r'floor\("h"\)')],
    "missingness: structural vs failure": [("p1-2-gaps-and-stale-data", r"solar_missing")],
    "genuine zero vs non-reporting": [("p2-3-imports-and-outages", r"positive_origins")],
    "stale values, limited ffill and age flag": [("p1-2-gaps-and-stale-data", r"ffill\(limit=48\)"), ("p2-1-cracks", r"run_length")],
    "data-quality assertions": [("p2-1-cracks", r"assert "), ("p3-2-merge-asof", r"assert ")],
    "time series / differences / returns": [("p4-1-levels-and-returns", r"np\.log"), ("p1-5-price-patterns", r"\.diff\(\)")],
    "histogram / density": [("p1-5-price-patterns", r"\.hist\("), ("p4-1-levels-and-returns", r"\.hist\(")],
    "boxplot": [("p1-5-price-patterns", r"boxplot"), ("p2-2-extremes", r"boxplot")],
    "seasonal plot": [("p4-2-stationarity", r"seasonal plot")],
    "scatter plot": [("p1-3-degree-days", r"scatter"), ("p2-4-crack-regression", r"scatter")],
    "rolling mean / volatility": [("p1-5-price-patterns", r"rolling\(30\)"), ("p4-1-levels-and-returns", r"rolling\(60\)")],
    "ACF": [("p1-5-price-patterns", r"acf\("), ("p4-2-stationarity", r"acf\("), ("p3-5-reaction-and-drift", r"plot_acf")],
    "correlation matrix, Pearson vs Spearman": [("p4-1-levels-and-returns", r"spearman"), ("p1-6-spike-investigation", r"spearman")],
    "sub-period comparison / event annotation": [("p4-4-engle-granger", r"periods"), ("p1-6-spike-investigation", r"scatter\(part\.index")],
    "descriptive stats: mean vs median, skewness, kurtosis": [("p4-1-levels-and-returns", r"\.kurt\("), ("p1-5-price-patterns", r"\.skew\(")],
    "OLS coefficients, SEs, confidence intervals": [("p1-4-weather-adjusted-load", r"conf_int\(\)"), ("p2-4-crack-regression", r"\.bse")],
    "multicollinearity (VIF)": [("p2-4-crack-regression", r"variance_inflation_factor")],
    "heteroskedasticity: White test": [("p2-4-crack-regression", r"het_white")],
    "HC3 robust standard errors": [("p2-4-crack-regression", r'cov_type="HC3"')],
    "HAC / Newey-West": [("p3-5-reaction-and-drift", r'cov_type="HAC"')],
    "Durbin-Watson": [("p4-3-spurious-regression", r"durbin_watson"), ("p3-5-reaction-and-drift", r"durbin_watson")],
    "stationarity, ADF with n / c / ct, I(0) / I(1)": [("p4-2-stationarity", r"adfuller")],
    "deterministic vs stochastic trend, detrending": [("p4-2-stationarity", r"detrended")],
    "first and seasonal differences, log returns": [("p4-2-stationarity", r"diff\(12\)")],
    "spurious regression": [("p4-3-spurious-regression", r"spurious")],
    "Engle-Granger with the right critical values": [("p4-3-spurious-regression", r"coint\("), ("p4-4-engle-granger", r"coint\(")],
    "structural change, Chow test": [("p4-4-engle-granger", r"chow_f")],
    "HDD / CDD with zone bases": [("p1-3-degree-days", r"hdd_base_c")],
    "load ~ HDD + CDD regression": [("p1-4-weather-adjusted-load", r'\["hdd", "cdd", "is_weekend"\]')],
    "weather-adjusted load vs a reference weather": [("p1-4-weather-adjusted-load", r"normal_hdd")],
    "five timestamps, publication lag, release calendar": [("p3-1-five-dates", r"publication_lag_days")],
    "merge_asof backward on availability, tolerance": [("p3-2-merge-asof", r'direction="backward"')],
    "vintages, pseudo vs genuine point-in-time": [("p3-3-vintages", r"vintage_date")],
    "truncation test": [("p3-4-truncation-test", r"truncated")],
    "no-lookahead assertions": [("p3-2-merge-asof", r"assert no_future")],
    "chronological train / test split, frozen model": [("p3-6-out-of-sample", r"TRAIN_END")],
    "in-sample vs out-of-sample errors (MAE, RMSE)": [("p3-6-out-of-sample", r"mae_out")],
    "baselines": [("p3-6-out-of-sample", r"mae_zero")],
    "expanding-window walk-forward": [("p3-6-out-of-sample", r"DateOffset\(months=3\)")],
    "outliers: z / modified z / IQR, error vs event": [("p2-2-extremes", r"modified_z")],
    "residual load, merit order, margin": [("p1-6-spike-investigation", r"margin_mw")],
    "economic mechanism before cointegration": [("p4-4-engle-granger", r"arbitrage")],
}


def check_coverage_and_scope():
    section("4. concept coverage, allowed techniques, excluded topics, KPSS")
    missing = 0
    by_project = {}
    for concept, evidence in sorted(COVERAGE.items()):
        for folder, pattern in evidence:
            pid = "quant/" + folder
            ok = server.problem_dir(pid) is not None and re.search(pattern, quant_text(pid))
            missing += 0 if ok else 1
            check(ok, "coverage: %s — no evidence %r in %s" % (concept, pattern, folder))
            by_project.setdefault(folder[:2], set()).add(concept)
    print("   %d concepts, %d evidence links missing; concepts per project: %s" % (
        len(COVERAGE), missing, {k: len(v) for k, v in sorted(by_project.items())}))

    # techniques this curriculum deliberately allows must not be caught by the exclusion list
    for allowed in ["ACF", "plot_acf", "Durbin-Watson", "White", "het_white", "HC3", "HAC", "Newey-West",
                    "walk-forward", "MAE", "RMSE", "out of sample"]:
        check(not any(re.search(p, allowed) for p in EXCLUDED), "the allowed technique %r is excluded" % allowed)

    # HAC appears only where overlap (its reason) is explained, together with what it does not fix
    for p in quant_problems():
        text = quant_text(p["id"], ("solution.py", "test_code.py"))
        if 'cov_type="HAC"' in text:
            notes = quant_text(p["id"], ("statement.md", "solution.md"))
            check("overlap" in notes and "not" in notes, "%s: HAC used without explaining why" % p["id"])

    # KPSS: nowhere in the track, the interface, the judge, the server or the documentation
    hits = []
    targets = [os.path.join(ROOT, f) for f in ("README.md", "server.py", "start.command")]
    for folder in (QUANT, os.path.join(ROOT, "web"), os.path.join(ROOT, "judge")):
        for base, _dirs, files in os.walk(folder):
            targets += [os.path.join(base, f) for f in files if f.endswith((".md", ".py", ".json", ".js", ".html"))]
    for path in targets:
        if re.search(r"kpss", server.read_text(path), re.I):
            hits.append(os.path.relpath(path, ROOT))
    check(not hits, "KPSS mentioned in %s" % hits)
    print("   KPSS mentions: %d" % len(hits))

    found = 0
    for base, _dirs, files in os.walk(QUANT):
        for name in files:
            if not name.endswith((".md", ".py", ".json")):
                continue
            path = os.path.join(base, name)
            text = server.read_text(path)
            for pattern in EXCLUDED:
                for m in re.finditer(pattern, text):
                    found += 1
                    line = text[:m.start()].count("\n") + 1
                    check(False, "excluded term %r in %s:%d" % (m.group(0), os.path.relpath(path, ROOT), line))
    print("   excluded terms found: %d" % found)


# out of scope: other model families, other tests, ML, operational calculations
EXCLUDED = [
    r"\bAR\(", r"\bMA\(", r"\bARMA\b", r"\bARIMA\b", r"\bSARIMAX?\b", r"[Ee]xponential [Ss]moothing",
    r"\bHolt\b", r"Holt-Winters", r"\bETS\b", r"\bVAR\b", r"\bVECM\b",
    r"\bRidge\b", r"\bLasso\b", r"[Ee]lastic [Nn]et", r"[Qq]uantile regression", r"[Rr]andom [Ff]orest",
    r"[Gg]radient [Bb]oosting", r"XGB", r"\bKNN\b", r"\bSVM\b", r"[Kk]-means", r"[Nn]eural", r"\b[Ll]ogit\b",
    r"\b[Pp]robit\b", r"\b[Tt]obit\b", r"\bCAPM\b", r"\bAPT\b", r"Zakoian", r"GARCH",
    r"KPSS", r"kpss", r"Phillips", r"Johansen", r"Zivot", r"Bai-Perron", r"CUSUM", r"\bPACF\b", r"plot_pacf",
    r"Ljung", r"Breusch", r"\bARCH\b", r"het_arch", r"Diebold",
    r"[Nn]ested cross-validation", r"KFold", r"[Hh]yperparameter", r"train_test_split", r"[Gg]rid search",
    r"[Rr]ecursive forecast", r"[Mm]ulti-output", r"\bMAPE\b", r"\bWAPE\b", r"\bMASE\b", r"\bMSE\b",
    r"[Pp]rediction interval", r"[Nn]etback", r"[Bb]oil-off", r"[Bb]reak-even", r"\bFOB\b", r"\bDES\b",
    r"[Ff]reight", r"DuckDB",
]


def check_code_style():
    section("5. plain reference code and temporal safety rules")
    rules = [(r"^\s*class\s", "a class"), (r"\blambda\b", "a lambda"), (r"functools|reduce\(|(?<!\.)\bmap\(", "functional tricks"),
             (r"\[[^\]]*\bfor\b[^\]]*\[[^\]]*\bfor\b", "a nested comprehension"), (r"\.pipe\(|\.apply\(", "pipe/apply chains"),
             (r"\.assign\(", "assign chains"),
             (r"\.bfill\(|fillna\(method=", "a backward fill (uses the future)"),
             (r"\.interpolate\(", "an interpolation (uses the next value)"),
             (r"\.sample\(|shuffle|train_test_split", "a random split")]
    files = 0
    for p in quant_problems():
        path = os.path.join(server.problem_dir(p["id"]), "solution.py")
        if not os.path.isfile(path):
            continue
        files += 1
        text = server.read_text(path)
        rel = os.path.relpath(path, ROOT)
        for pattern, label in rules:
            check(not re.search(pattern, text, re.M), "%s: %s" % (rel, label))
        functions = len(re.findall(r"^def ", text, re.M))
        check(functions <= 2, "%s: %d functions (one logical operation per exercise)" % (rel, functions))
        long_lines = [i + 1 for i, line in enumerate(text.splitlines()) if len(line) > 120]
        check(not long_lines, "%s: lines longer than 120 characters %s" % (rel, long_lines))
        for line in text.splitlines():
            for m in re.finditer(r"\.ffill\(([^)]*)\)", line):
                # carrying a TIMESTAMP forward (to measure the age of the last value) is not a data fill
                carries_a_time = re.search(r"\w+(_time|_at|_date)\s*=\s*\w+(_time|_at|_date)\.ffill", line)
                check("limit=" in m.group(1) or carries_a_time, "%s: ffill without a limit: %s" % (rel, line.strip()))
        for m in re.finditer(r"merge_asof\((.*?)\)\n", text, re.S):
            check('direction="backward"' in m.group(1), "%s: merge_asof must look backward" % rel)
        if p["project"] == "p3" and "merge_asof" in text:
            check('right_on="available_at"' in text, "%s: point-in-time joins must use the availability time" % rel)
    p36 = server.read_text(os.path.join(QUANT, "p3-6-out-of-sample", "solution.py"))
    check('TRAIN_END = pd.Timestamp("2022-12-31")' in p36 and 'TEST_START = pd.Timestamp("2023-01-01")' in p36,
          "3.6: the split must be 2019-2022 / 2023-2024")
    check('table["target_end_date"] <= TRAIN_END' in p36, "3.6: training labels must be purged at the split")
    check('table["target_end_date"] < origin' in p36, "3.6: walk-forward must only use labels known at the origin")
    print("   %d reference solutions scanned" % files)


# ---------------------------------------------------------------------------
# 6. derived layers and 7. results quoted by the notes
# ---------------------------------------------------------------------------
def load_solution(folder, function):
    namespace = {"__name__": "check"}
    path = os.path.join(QUANT, folder, "solution.py")
    exec(compile(server.read_text(path), path, "exec"), namespace)
    return namespace[function]


def csv(name, **kwargs):
    import pandas as pd
    return pd.read_csv(os.path.join(DATA_DIR, name), **kwargs)


def same_frame(a, b, label):
    import pandas as pd
    try:
        pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True), check_dtype=False,
                                      check_exact=False, check_names=False, rtol=1e-6, atol=1e-6)
        return True
    except AssertionError as exc:
        check(False, "%s differs from what the reference solution returns: %s" % (label, str(exc)[:300]))
        return False


def check_derived_layers():
    import pandas as pd
    section("6. derived layers = what the reference solutions return")
    old = os.getcwd()
    os.chdir(DATA_DIR)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            clean = load_solution("p1-1-delivery-hours", "load_market_hours")("p1_power_hourly_vendor_synthetic.csv")
            stored = csv("p1_power_hourly_clean_synthetic.csv")
            same_frame(clean.reset_index().assign(delivery_start_utc=lambda f: f["delivery_start_utc"].astype(str))
                       .drop(columns="local_date"), stored.drop(columns="local_date").assign(
                           delivery_start_utc=lambda f: pd.to_datetime(f["delivery_start_utc"], utc=True).astype(str)),
                       "p1 clean layer")
            hours = stored.copy()
            hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
            hours["local_date"] = pd.to_datetime(hours["local_date"])
            treated = load_solution("p1-2-gaps-and-stale-data", "treat_gaps")(hours.set_index("delivery_start_utc"))
            stored_t = csv("p1_power_hourly_treated_synthetic.csv")
            same_frame(treated.reset_index(drop=True).drop(columns="local_date"),
                       stored_t.drop(columns=["delivery_start_utc", "local_date"]), "p1 treated layer")
            daily = load_solution("p1-3-degree-days", "daily_zone_table")(
                csv("p1_zone_temperature_obs_synthetic.csv"), csv("p1_zone_load_hourly_synthetic.csv"),
                csv("p1_zones_reference_synthetic.csv"))
            stored_d = csv("p1_zone_daily_synthetic.csv", parse_dates=["local_date"])
            same_frame(daily, stored_d, "p1 daily zone table")
            wide = load_solution("p2-1-cracks", "build_daily_table")(csv("p2_products_daily_long_synthetic.csv"))
            stored_w = csv("p2_products_wide_synthetic.csv", index_col="date", parse_dates=["date"])
            same_frame(wide.reset_index(), stored_w.reset_index(), "p2 wide table")
            repaired = load_solution("p2-2-extremes", "investigate_extremes")(stored_w, csv("p2_market_events_synthetic.csv"))["prices"]
            stored_r = csv("p2_products_repaired_synthetic.csv", index_col="date", parse_dates=["date"])
            same_frame(repaired.reset_index(), stored_r[repaired.columns].reset_index(), "p2 repaired prices")
            monthly = load_solution("p2-3-imports-and-outages", "monthly_table")(
                csv("p2_diesel_imports_monthly_synthetic.csv"), csv("p2_refinery_outages_synthetic.csv"),
                csv("p2_distillate_fundamentals_monthly_synthetic.csv"), stored_r)
            stored_m = csv("p2_monthly_table_synthetic.csv")
            same_frame(monthly.reset_index(drop=True), stored_m.drop(columns="month"), "p2 monthly table")
            # P3 pipeline tables agree with the reference solutions of 3.1 (surprise) and 3.3 (demand as known)
            stocks = load_solution("p3-1-five-dates", "add_availability")(csv("p3_us_crude_stocks_weekly_synthetic.csv"))
            events = csv("p3_release_events_synthetic.csv")
            merged = events.merge(stocks.assign(week_ending=lambda f: f["week_ending"].dt.strftime("%Y-%m-%d")),
                                  on="week_ending", suffixes=("", "_ref"))
            check(len(merged) == len(events) and ((merged["surprise_mbbl"] - merged["surprise_mbbl_ref"]).abs()
                                                  .fillna(0) < 1e-6).all(), "p3 events: surprise differs from 3.1")
            table = csv("p3_decision_table_daily_synthetic.csv")
            sample = table.iloc[::97].dropna(subset=["demand_growth_known_pct"])
            known = load_solution("p3-3-vintages", "known_at")(csv("p3_us_oil_demand_vintages_synthetic.csv"), sample["date"])
            check(((known["growth_known_pct"].values - sample["demand_growth_known_pct"].values) ** 2).max() < 1e-8,
                  "p3 decision table: demand growth differs from 3.3")
            aligned = load_solution("p3-2-merge-asof", "align_stocks")(csv("p3_wti_daily_synthetic.csv"), stocks)
            check(((aligned["surprise_mbbl"].fillna(-99).values - table["surprise_mbbl"].fillna(-99).values) ** 2).max() < 1e-8,
                  "p3 decision table: surprise differs from the 3.2 join")
    finally:
        os.chdir(old)
    print("   P1 clean / treated / daily, P2 wide / repaired / monthly, P3 events / decision table: checked")


def near(value, target, tol, label):
    ok = value is not None and abs(float(value) - target) <= tol
    check(ok, "%s: %s, the notes say %s" % (label, value, target))
    return ok


def check_outcomes():
    import numpy as np
    import pandas as pd
    section("7. the numbers quoted by the notes still hold")
    old = os.getcwd()
    os.chdir(DATA_DIR)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            outcomes_p1(np, pd)
            outcomes_p2(np, pd)
            outcomes_p3(np, pd)
            outcomes_p4(np, pd)
    finally:
        os.chdir(old)


def p1_hours(pd, name):
    hours = csv(name)
    hours["delivery_start_utc"] = pd.to_datetime(hours["delivery_start_utc"], utc=True)
    hours["local_date"] = pd.to_datetime(hours["local_date"])
    return hours.set_index("delivery_start_utc")


def outcomes_p1(np, pd):
    raw = csv("p1_power_hourly_vendor_synthetic.csv")
    check(len(raw) == 17553 and raw.duplicated().sum() == 6, "1.1: raw rows / exact copies")
    check(raw.duplicated(subset=["delivery_start_local"]).sum() == 11, "1.1: local-time dedup should hit 11 rows")
    clean = p1_hours(pd, "p1_power_hourly_clean_synthetic.csv")
    check(len(clean) == 17544, "1.1: 17,544 delivery hours")
    check(clean.groupby("local_date").size().value_counts().to_dict() == {24: 727, 23: 2, 25: 2}, "1.1: day lengths")
    near(clean.loc["2023-11-21 17:00", "price_eur_mwh"], 77.25, 1e-9, "1.1: corrected 772.50 print")
    treated = p1_hours(pd, "p1_power_hourly_treated_synthetic.csv")
    check(clean["solar_mw"].isna().sum() == 8850 and int(treated["solar_missing"].sum()) == 5, "1.2: solar blanks")
    check(int(treated["wind_missing"].sum()) == 15 and treated["price_eur_mwh"].isna().sum() == 2, "1.2: wind / price gaps")
    check(treated["available_capacity_mw"].isna().sum() == 95 and int(treated["capacity_is_stale"].sum()) == 144,
          "1.2: capacity carried 48 h")
    daily = csv("p1_zone_daily_synthetic.csv")
    by_zone = {z: g.dropna() for z, g in daily.groupby("zone")}
    near(by_zone["SOUTH"]["load_avg_mw"].corr(by_zone["SOUTH"]["temp_mean_c"]), -0.041, 0.005, "1.3: SOUTH load vs temperature")
    near(by_zone["SOUTH"]["load_avg_mw"].corr(by_zone["SOUTH"]["cdd"]), 0.531, 0.005, "1.3: SOUTH load vs CDD")
    weather = load_solution("p1-4-weather-adjusted-load", "weather_adjusted_load")(daily, csv("p1_weather_normals_synthetic.csv"))
    coef = weather["coefficients"].set_index("zone")
    near(coef.loc["NORTH", "b_hdd"], 261.0, 0.5, "1.4: NORTH MW per HDD")
    near(coef.loc["SOUTH", "b_cdd"], 321.0, 0.5, "1.4: SOUTH MW per CDD")
    for zone, weekend, dw in [("NORTH", -1067, 0.72), ("CENTRAL", -1665, 0.61), ("SOUTH", -822, 0.78)]:
        near(coef.loc[zone, "b_weekend"], weekend, 1, "1.4: %s weekend" % zone)
        near(coef.loc[zone, "durbin_watson"], dw, 0.01, "1.4: %s Durbin-Watson" % zone)
    check(coef.loc["NORTH", "b_cdd_low"] < 0 < coef.loc["NORTH", "b_cdd_high"] and coef.loc["NORTH", "cdd_days"] == 4,
          "1.4: NORTH cooling coefficient should not be identified")
    winter = weather["winter_comparison"]
    for zone in ["NORTH", "CENTRAL", "SOUTH"]:
        check(winter.loc[(zone, 2024), "load_avg_mw"] > winter.loc[(zone, 2023), "load_avg_mw"], "1.4: %s actual load up" % zone)
        check(winter.loc[(zone, 2024), "load_adjusted_mw"] < winter.loc[(zone, 2023), "load_adjusted_mw"],
              "1.4: %s adjusted load down" % zone)
    patterns = load_solution("p1-5-price-patterns", "price_patterns")(treated)
    near(patterns["change_stats"]["excess_kurtosis"], 1010, 5, "1.5: kurtosis of price changes")
    near(patterns["acf_load"][24], 0.931, 0.002, "1.5: load ACF at 24 h")
    near(patterns["load_solar_correlation"]["raw"], 0.141, 0.002, "1.5: raw load-solar correlation")
    near(patterns["load_solar_correlation"]["within_hour"], -0.447, 0.002, "1.5: within-hour correlation")
    spikes = load_solution("p1-6-spike-investigation", "explain_spikes")(treated, daily)
    drivers = spikes["spike_days"]["driver"].value_counts().to_dict()
    check(drivers == {"cold and still": 10, "low available capacity": 4}, "1.6: spike attribution %s" % drivers)
    near(spikes["rank_correlations"]["min_margin_mw"], -0.796, 0.002, "1.6: margin rank correlation")
    near(spikes["rank_correlations"]["hdd"], 0.391, 0.002, "1.6: HDD rank correlation")
    print("   P1: hours, gaps, degree days, weather sensitivities, adjusted winters, patterns, spikes — ok")


def outcomes_p2(np, pd):
    wide = csv("p2_products_wide_synthetic.csv", index_col="date", parse_dates=["date"])
    check(len(wide) == 1671 and wide["gasoil"].loc["2018-10-08":"2018-10-15"].isna().sum() == 5, "2.1: frozen run blanked")
    near((wide["gasoil"] - wide["brent"]).loc["2018-10"].mean(), 17.98, 0.01, "2.1: October 2018 crack, gaps left")
    near((wide["gasoil"].ffill() - wide["brent"]).loc["2018-10"].mean(), 18.56, 0.01, "2.1: October 2018 crack, ffill")
    result = load_solution("p2-2-extremes", "investigate_extremes")(wide, csv("p2_market_events_synthetic.csv"))
    counts = result["decisions"]["decision"].value_counts().to_dict()
    check(counts == {"keep_event": 11, "keep_market_move": 11, "correct_unit": 1, "set_missing": 1, "keep_doubtful": 1},
          "2.2: decisions %s" % counts)
    rbob = np.log(wide["rbob"].dropna()).diff().dropna()
    near(((rbob - rbob.mean()) / rbob.std())["2017-08-28"], 1.2, 0.05, "2.2: masked hurricane z-score")
    repaired = result["prices"]
    near((repaired["rbob"] - repaired["brent"]).loc["2019"].mean(), 10.1, 0.05, "2.2: RBOB 2019 crack after repair")
    near((wide["rbob"] - wide["brent"]).loc["2019"].mean(), 45.0, 0.05, "2.2: RBOB 2019 crack before repair")
    monthly = csv("p2_monthly_table_synthetic.csv").set_index("month")
    check(monthly.loc[["2018-08", "2019-04", "2022-08", "2023-06"], "imports_kbd"].isna().all(), "2.3: non-reported months blank")
    check((monthly.loc["2023-02":"2023-05", "imports_from_russia_kbd"] == 0).all(), "2.3: embargo zeros kept")
    near(monthly.loc["2017-09", "outages_kbd"], 1466.7, 0.1, "2.3: hurricane outage month")
    reg = load_solution("p2-4-crack-regression", "crack_regression")(csv("p2_monthly_table_synthetic.csv"))
    table = reg["coefficients"]
    near(table.loc["stocks_vs_5y_pct", "coef"], -1.093, 0.001, "2.4: stocks coefficient")
    check(reg["white_p"] < 0.01, "2.4: White test should reject")
    near(table.loc["stocks_vs_5y_pct", "se_hc3"] / table.loc["stocks_vs_5y_pct", "se"], 1.5, 0.05, "2.4: HC3 / OLS SE")
    check(table.loc["outages_kbd", "p"] < 0.05 < 0.2 < table.loc["outages_kbd", "p_hc3"], "2.4: outage p-values")
    near(reg["residuals_by_stocks"].loc["below -15%", "mean"], 0.99, 0.01, "2.4: residual curvature")
    print("   P2: units, frozen feed, decisions, masking, zeros, White / HC3 — ok")


def outcomes_p3(np, pd):
    stocks = load_solution("p3-1-five-dates", "add_availability")(csv("p3_us_crude_stocks_weekly_synthetic.csv"))
    check(stocks["publication_lag_days"].value_counts().to_dict() == {5: 278, 6: 35, 12: 1}, "3.1: publication lags")
    check(int(stocks["backfilled"].sum()) == 61, "3.1: backfilled records")
    prices = csv("p3_wti_daily_synthetic.csv")
    aligned = load_solution("p3-2-merge-asof", "align_stocks")(prices, stocks)
    wrong_side = stocks[["week_ending", "surprise_mbbl", "available_at"]].copy()
    wrong_side["key"] = wrong_side["week_ending"].dt.tz_localize("UTC")
    wrong = pd.merge_asof(aligned[["date", "decision_time"]], wrong_side.sort_values("key"),
                          left_on="decision_time", right_on="key", direction="backward")
    check(int((wrong["available_at"] > wrong["decision_time"]).sum()) == 929, "3.2: unpublished reports used")
    next_return = np.log(aligned["wti_settle_usd_bbl"]).diff().shift(-1)
    eve = aligned["date"].shift(-1).isin(set(pd.to_datetime(stocks["release_date"])))
    near(next_return[eve].corr(wrong["surprise_mbbl"][eve]), -0.245, 0.002, "3.2: fake predictability")
    near(next_return[eve].corr(aligned["surprise_mbbl"][eve]), -0.077, 0.002, "3.2: correct join")
    vintages = csv("p3_us_oil_demand_vintages_synthetic.csv")
    dates = pd.date_range("2019-01-15", "2024-12-15", freq="MS") + pd.Timedelta(days=14)
    known = load_solution("p3-3-vintages", "known_at")(vintages, dates)
    near((known["demand_final_kbd"] - known["demand_known_kbd"]).mean(), 126.9, 0.1, "3.3: mean revision")
    reaction = load_solution("p3-5-reaction-and-drift", "reaction_and_drift")(
        csv("p3_release_events_synthetic.csv"), csv("p3_decision_table_daily_synthetic.csv"))
    near(reaction["reaction"].loc["surprise_mbbl", "t"], -6.67, 0.01, "3.5: reaction t")
    near(reaction["drift"].loc["surprise_mbbl", "t"], -4.84, 0.01, "3.5: drift OLS t")
    near(reaction["drift"].loc["surprise_mbbl", "t_hac"], -2.86, 0.01, "3.5: drift HAC t")
    near(reaction["dw_drift"], 0.18, 0.01, "3.5: Durbin-Watson of overlapping windows")
    oos = load_solution("p3-6-out-of-sample", "validate_out_of_sample")(csv("p3_decision_table_daily_synthetic.csv"))
    fixed = oos["fixed"]
    check(fixed["n_train"] == 991 and fixed["n_test"] == 492, "3.6: sample sizes")
    near(fixed["mae_out"], 0.0621, 0.0001, "3.6: out-of-sample MAE")
    near(fixed["mae_zero"], 0.0598, 0.0001, "3.6: zero-forecast MAE")
    check(fixed["mae_out"] > fixed["mae_zero"] and oos["walk_forward_mae"] > fixed["mae_zero"],
          "3.6: the notes say the model loses to the zero forecast")
    path = oos["walk_forward_path"]
    check(path["coef_surprise"].iloc[-1] > path["coef_surprise"].iloc[0], "3.6: the coefficient should shrink")
    print("   P3: lags, backfill, fake predictability, revisions, reaction, HAC, out of sample — ok")


def outcomes_p4(np, pd):
    prices = csv("p4_crude_research_daily_synthetic.csv")
    basics = load_solution("p4-1-levels-and-returns", "levels_and_returns")(prices)
    near(basics["level_corr"]["wti_coffee"], 0.821, 0.002, "4.1: coffee level correlation")
    near(basics["return_corr"]["wti_coffee_pearson"], 0.006, 0.002, "4.1: coffee return correlation")
    near(basics["rolling_vol_60d"].max(), 0.477, 0.002, "4.1: peak rolling volatility")
    table = load_solution("p4-2-stationarity", "stationarity_table")(prices, csv("p4_diesel_demand_monthly_synthetic.csv"))
    near(table.loc[0, "p_value"], 0.758, 0.005, "4.2: ADF log Brent (c)")
    near(table.loc[3, "p_value"], 0.978, 0.005, "4.2: ADF demand (c)")
    check(table.loc[4, "p_value"] < 0.001, "4.2: ADF demand (ct) should reject")
    near(table.loc[6, "acf_long"], -0.485, 0.005, "4.2: over-differencing signature")
    spurious = load_solution("p4-3-spurious-regression", "spurious_check")(prices)
    near(spurious.loc[0, "t"], 68.65, 0.05, "4.3: spurious t")
    near(spurious.loc[0, "durbin_watson"], 0.016, 0.001, "4.3: DW of the spurious regression")
    near(spurious.loc[0, "residual_adf_p_naive"], 0.059, 0.002, "4.3: naive residual ADF p")
    near(spurious.loc[0, "engle_granger_p"], 0.168, 0.002, "4.3: Engle-Granger p")
    relation = load_solution("p4-4-engle-granger", "relationship_by_period")(prices)
    periods = relation["periods"]
    near(periods.loc["before 2016-01-01", "mean_spread_usd"], 15.86, 0.01, "4.4: pre-2016 discount")
    near(periods.loc["from 2016-01-01", "mean_spread_usd"], 2.85, 0.01, "4.4: post-2016 discount")
    near(relation["chow_f"], 113.3, 0.1, "4.4: Chow F")
    placebo = load_solution("p4-4-engle-granger", "relationship_by_period")(prices[prices["date"] >= "2016-01-01"], "2018-01-01")
    near(placebo["chow_f"], 0.07, 0.01, "4.4: placebo inside the post-2016 regime")
    print("   P4: levels vs returns, ADF table, spurious regression, Engle-Granger, Chow — ok")


# ---------------------------------------------------------------------------
# 8. the tests catch the typical errors (mutations of the reference solutions)
# ---------------------------------------------------------------------------
MUTATIONS = [
    ("p3-6-out-of-sample", 'train = table[table["target_end_date"] <= TRAIN_END]',
     'train = table[table["date"] <= TRAIN_END]', "labels not purged at the split"),
    ("p3-6-out-of-sample", 'train = table[table["target_end_date"] <= TRAIN_END]',
     'train = table.sample(frac=0.67, random_state=0)', "a random split"),
    ("p3-6-out-of-sample", 'known = table[table["target_end_date"] < origin]',
     'known = table[table["date"] < origin]', "walk-forward trained on labels not yet realised"),
    ("p3-2-merge-asof", 'direction="backward"', 'direction="nearest"', "a join that can look forward"),
    ("p3-4-truncation-test", 'stocks_then = stocks[stocks["available_at"] <= cutoff]', 'stocks_then = stocks',
     "a truncation that keeps the future"),
    ("p1-2-gaps-and-stale-data", '.ffill(limit=48)', '.ffill()', "an unlimited forward fill"),
    ("p1-2-gaps-and-stale-data", 'report_date < hours["local_date"]', 'hours["capacity_age_h"] >= 24',
     "a 24-hour age limit on the 25-hour day"),
    ("p1-1-delivery-hours", 'drop_duplicates(subset="delivery_start_utc", keep="last")',
     'drop_duplicates(subset="delivery_start_utc", keep="first")', "keeping the first version of a record"),
    ("p3-5-reaction-and-drift", '"maxlags": 9', '"maxlags": 0', "HAC without the overlap"),
    ("p4-4-engle-granger", 'changes = part.dropna()',
     'changes = part[["brent", "wti"]].diff().dropna().rename(columns={"brent": "d_brent", "wti": "d_wti"})',
     "a Chow test on different days"),
    ("p2-4-crack-regression", 'cov_type="HC3"', 'cov_type="nonrobust"', "conventional SEs reported as robust"),
]


def check_mutations():
    section("8. the tests reject typical mistakes (mutated reference solutions)")
    for folder, old, new, label in MUTATIONS:
        meta, path = server.load_meta("quant/" + folder)
        code = server.read_text(os.path.join(path, "solution.py"))
        if not check(old in code, "%s: mutation anchor %r not found" % (folder, old)):
            continue
        res = server.judge("submit", meta, path, code.replace(old, new, 1))
        rejected = res.get("status") != "accepted"
        check(rejected, "%s: the tests accept %s" % (folder, label))
        print("   %-28s %-48s %s" % (folder, label, "rejected" if rejected else "ACCEPTED (bad)"))


# ---------------------------------------------------------------------------
def check_judge():
    section("9. judge: reference solutions, starters, test-code pads")
    for p in server.list_problems():
        meta, path = server.load_meta(p["id"])
        kind = meta["type"]
        if kind not in ("code", "sql"):
            continue
        ext = server.EXT[kind]
        solution = server.read_text(os.path.join(path, "solution." + ext))
        starter = server.read_text(os.path.join(path, "starter." + ext))
        res = server.judge("submit", meta, path, solution)
        ok = res.get("status") == "accepted"
        detail = ""
        if not ok:
            if res.get("kind") == "tests":
                bad = [t for t in res.get("tests", []) if not t["passed"]]
                detail = res.get("load_error") or "; ".join(
                    "%s: %s%s" % (t["name"], t.get("reason", ""), t.get("error", "")[-300:]) for t in bad[:3])
            else:
                detail = res.get("reason") or res.get("error") or str(res)[:300]
        check(ok, "%s: reference solution not accepted — %s" % (p["id"], detail))
        res_starter = server.judge("submit", meta, path, starter)
        check(res_starter.get("status") != "accepted", "%s: the starter already passes the tests" % p["id"])
        line = "   %-48s solution %s" % (p["id"], "accepted" if ok else "REJECTED")
        if res.get("kind") == "tests":
            line += " (%d tests)" % res.get("total", 0)
        if kind == "code":
            scratch = server.read_text(os.path.join(path, "test_code.py"))
            run = server.judge("run", meta, path, solution, scratch)
            ran = run.get("kind") == "console" and run.get("exit_code") == 0 and not run.get("timed_out")
            check(ran, "%s: the Test code pad fails with the reference solution:\n%s" % (
                p["id"], (run.get("output") or run.get("error") or "")[-800:]))
            check("Warning" not in (run.get("output") or ""), "%s: the Test code pad prints a warning:\n%s" % (
                p["id"], (run.get("output") or "")[-600:]))
            if "matplotlib" in scratch:
                check(len(run.get("figures", [])) >= 1, "%s: the Test code pad plots but returned no chart" % p["id"])
            line += " · test code %s" % ("runs" if ran else "FAILS")
            if run.get("figures"):
                line += ", %d chart%s" % (len(run["figures"]), "" if len(run["figures"]) == 1 else "s")
        print(line)


# ---------------------------------------------------------------------------
def check_progress():
    section("10. progress file")
    data = server.read_json(server.PROGRESS_FILE) or {"problems": {}}
    recorded = data.get("problems", {})
    active = {p["id"] for p in server.list_problems()}
    archived = {"glencore/" + d for d in os.listdir(os.path.join(ROOT, "archive", "glencore-mcq"))}
    renamed = {}
    for p in server.list_problems():
        for old in p.get("previous_ids", []):
            renamed[old] = p["id"]
    retired = set(server.read_json(os.path.join(QUANT, "set.json")).get("retired_ids", []))
    check(not (retired & (active | set(renamed))), "a retired id is still active or renamed")
    for pid in recorded:
        check(pid in active or pid in archived or pid in renamed or pid in retired,
              "progress entry %s matches no active, archived, renamed or retired problem" % pid)
    # every exercise of the previous version is accounted for
    v2 = os.path.join(ROOT, "archive", "quant-v2", "quant")
    if os.path.isdir(v2):
        for folder in sorted(os.listdir(v2)):
            old_meta = server.read_json(os.path.join(v2, folder, "meta.json"))
            if not old_meta:
                continue
            for old in ["quant/" + folder] + old_meta.get("previous_ids", []):
                check(old in active or old in renamed or old in retired, "v2 id %s is neither carried over nor retired" % old)
    listing = server.api_problems({}, None)
    shown = {p["id"]: p["progress"]["status"] for p in listing["problems"]}
    for pid, entry in recorded.items():
        target = pid if pid in active else renamed.get(pid)
        if target is None:
            continue
        detail = server.api_problem({"id": [target]}, None)
        if target == pid:
            check(shown[pid] == entry.get("status", "todo"), "%s: status not shown in the list" % pid)
        if target == pid:
            check(detail.get("draft") == entry.get("draft", {}), "%s: draft not returned" % pid)
        elif target not in recorded:
            expected = {k: v for k, v in entry.get("draft", {}).items() if k != "scratch"}
            check(detail.get("draft") == expected, "%s: draft not carried over to %s" % (pid, target))
            check("scratch" not in detail.get("draft", {}), "%s: the old Test code pad was carried over" % pid)
    on_disk = server.read_json(server.PROGRESS_FILE) or {"problems": {}}
    check(on_disk == data, "reading progress must not modify the file")
    print("   %d recorded entr%s: %s" % (len(recorded), "y" if len(recorded) == 1 else "ies", ", ".join(
        "%s=%s%s" % (k, v.get("status"), (" -> " + renamed[k]) if k in renamed else "") for k, v in recorded.items())))


def check_written_flow():
    section("11. written answers: draft -> submit -> self-review (scratch progress file)")
    tmp = tempfile.mkdtemp(prefix="practice-check-")
    saved = server.PROGRESS_FILE, server.DATA
    try:
        server.DATA = tmp
        server.PROGRESS_FILE = os.path.join(tmp, "progress.json")
        if os.path.exists(saved[0]):
            shutil.copyfile(saved[0], server.PROGRESS_FILE)
        before = copy.deepcopy(server.load_progress())
        for pid in ("glencore/q17-ai-follow-up-question", "quant/p2-5-desk-decision", "quant/p3-7-debrief",
                    "quant/p4-5-research-defence"):
            meta, _ = server.load_meta(pid)
            public = server.api_problem({"id": [pid]}, None)
            check("rubric" not in public, "%s: rubric leaked before submission" % pid)
            server.api_draft({}, {"id": pid, "text": "draft answer", "touched": True})
            check(server.api_problem({"id": [pid]}, None)["draft"]["text"] == "draft answer", "%s: draft not saved" % pid)
            empty = server.api_submit({}, {"id": pid, "text": "   "})
            check(isinstance(empty, tuple) and empty[0] == 400, "%s: an empty answer was accepted" % pid)
            sub = server.api_submit({}, {"id": pid, "text": "My answer."})
            check(sub["progress"]["status"] in ("attempted", "solved"), "%s: submit did not record" % pid)
            sol = server.api_solution({"id": [pid]}, None)
            check(len(sol["rubric"]) == len(meta["rubric"]) and sol["notes"], "%s: solution / rubric missing" % pid)
            partial = server.api_review({}, {"id": pid, "rubric": [0, 2], "mastered": False})
            check(partial["progress"]["status"] == "attempted", "%s: 'review again' changed the status" % pid)
            done = server.api_review({}, {"id": pid, "rubric": list(range(len(meta["rubric"]))), "mastered": True})
            check(done["progress"]["status"] == "solved", "%s: 'mastered' did not solve the problem" % pid)
            entry = server.load_progress()["problems"][pid]
            check(len(entry["submissions"]) == 1, "%s: the self-review should update, not duplicate" % pid)
            print("   %s: draft, submit, rubric review, mastered — ok" % pid)
        after = server.load_progress()
        for pid, entry in before["problems"].items():
            check(after["problems"].get(pid) == entry, "%s: an unrelated progress entry changed" % pid)
    finally:
        server.PROGRESS_FILE, server.DATA = saved
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    fast = "--fast" in sys.argv
    check_metadata()
    check_interview_track()
    check_quant_structure()
    check_coverage_and_scope()
    check_code_style()
    check_derived_layers()
    check_outcomes()
    if not fast:
        check_mutations()
        check_judge()
    check_progress()
    check_written_flow()
    print()
    if FAILURES:
        print("FAILED — %d problem(s):" % len(FAILURES))
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
