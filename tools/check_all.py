#!/usr/bin/env python3
"""End-to-end checks of the question banks and the app — run before trusting a change.

    python3 tools/check_all.py            everything (about a minute)
    python3 tools/check_all.py --fast     skip running the judge on every problem

What it verifies
  1. metadata of every problem is valid (same rules as  server.py --check)
  2. Past Interview Questions: one bank, 15 Millennium + 8 Glencore, no MCQ, global difficulty
     order with both sources interleaved, a source badge on every question, no source-based
     sections or navigation in the interface
  3. Quantitative Methods: exactly four projects, contiguous steps, difficulty non-decreasing
     inside each project, written debriefs with rubrics, architectures A01-A05 (+A06, A07) covered,
     ADF used and tested, KPSS absent everywhere
  4. excluded models / tests / forecasting topics are absent from the Quantitative Methods material
  5. the reference solutions of the track are written in plain, explicit style (no classes,
     lambdas, nested comprehensions or framework-like helpers)
  6. the results quoted by the teaching notes still hold on the data (clean layers reproduced,
     errors vs events, truncation tests, point-in-time effects, ADF / OLS / Engle-Granger / Chow)
  7. every reference solution is ACCEPTED by the real judge, every starter is NOT, and every
     "Test code" pad runs without error against the reference solution
  8. the progress file loads; every recorded id is active, archived, or carried over to a renamed
     exercise ("previous_ids"), and a carried-over draft is visible under the new id
  9. the written-answer flow (draft -> submit -> self-review) works, on a scratch copy of the
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


def check_quant_track():
    section("3. Quantitative Methods")
    probs = [p for p in server.list_problems() if p["track"] == "quant"]
    projects = [c["id"] for c in server.list_projects() if c["track"] == "quant"]
    check(projects == ["p1", "p2", "p3", "p4"], "expected exactly four projects, got %s" % projects)
    covered = set()
    for c in projects:
        mine = [p for p in probs if p["project"] == c]
        steps = [p["step"] for p in mine]
        check(steps == list(range(1, len(mine) + 1)), "%s: steps are %s" % (c, steps))
        diffs = [p["difficulty"] for p in mine]
        check(diffs == sorted(diffs), "%s: difficulty decreases inside the project: %s" % (c, diffs))
        check(bool(mine) and mine[-1]["type"] == "open", "%s should end with a written debrief" % c)
        arch = sorted({a for p in mine for a in p.get("architectures", [])})
        covered.update(arch)
        print("   %s: %2d exercises (%d code, %d written), levels %s, architectures %s" % (
            c, len(mine), sum(p["type"] == "code" for p in mine), sum(p["type"] == "open" for p in mine),
            diffs, ",".join(arch)))
    for needed in ["A01", "A02", "A03", "A04", "A05", "A06", "A07"]:
        check(needed in covered, "architecture %s is not covered by any exercise" % needed)
    focus = {"p1": "A02", "p2": "A03", "p3": "A04", "p4": "A06"}
    for project, arch in focus.items():
        mine = [p for p in probs if p["project"] == project]
        share = sum(arch in p.get("architectures", []) for p in mine)
        check(share >= 3, "%s should focus on %s (only %d exercises)" % (project, arch, share))
    for p in probs:
        meta, _ = server.load_meta(p["id"])
        if meta["type"] == "open":
            check(len(meta.get("rubric", [])) >= 5, "%s: rubric too short" % p["id"])
        else:
            check(len((meta.get("explain") or {}).get("rubric", [])) >= 5, "%s: explanation rubric missing" % p["id"])

    base = os.path.join(ROOT, "problems", "quant")
    uses_adf = [f for f in os.listdir(base) if "adfuller" in server.read_text(os.path.join(base, f, "solution.py"))]
    check(len(uses_adf) >= 3, "ADF should be implemented in several exercises (found %s)" % uses_adf)
    check(any("adf" in f for f in uses_adf), "no dedicated ADF exercise")
    kpss_hits = []
    for folder in [os.path.join(ROOT, "problems"), os.path.join(ROOT, "web"), os.path.join(ROOT, "judge")]:
        for path, _dirs, files in os.walk(folder):
            for name in files:
                if name.endswith((".md", ".py", ".json", ".js", ".csv")) and re.search(
                        r"kpss", server.read_text(os.path.join(path, name)), re.I):
                    kpss_hits.append(os.path.relpath(os.path.join(path, name), ROOT))
    for name in ["README.md", "server.py", "start.command"]:
        if re.search(r"kpss", server.read_text(os.path.join(ROOT, name)), re.I):
            kpss_hits.append(name)
    check(not kpss_hits, "KPSS still mentioned in: %s" % kpss_hits)
    print("   ADF used in: %s · KPSS mentions: %d" % (", ".join(sorted(uses_adf)), len(kpss_hits)))


# Models, tests and forecasting topics that must never appear in the track. Data-engineering
# topics (point-in-time, vintages, publication lags, truncation tests, features, rolling and
# calendar features, outlier scores, basic SQL) are part of the curriculum and are NOT listed.
EXCLUDED = [
    r"\bAR\(", r"\bMA\(", r"\bARMA\b", r"\bARIMA\b", r"\bSARIMAX?\b", r"[Ee]xponential [Ss]moothing",
    r"\bHolt\b", r"Holt-Winters", r"\bETS\b", r"\bVAR\b", r"\bVECM\b",
    r"\bRidge\b", r"\bLasso\b", r"[Ee]lastic [Nn]et", r"[Qq]uantile regression", r"[Rr]andom [Ff]orest",
    r"[Gg]radient [Bb]oosting", r"XGB", r"\bKNN\b", r"\bSVM\b", r"[Kk]-means", r"[Nn]eural", r"\b[Ll]ogit\b",
    r"\b[Pp]robit\b", r"\b[Tt]obit\b", r"\bCAPM\b", r"\bAPT\b", r"[Ll]everage effect", r"Zakoian", r"GARCH",
    r"KPSS", r"kpss", r"Phillips", r"Johansen", r"Zivot", r"Bai-Perron", r"CUSUM", r"\bACF\b", r"\bPACF\b",
    r"plot_acf", r"Ljung", r"Breusch", r"ARCH", r"Diebold", r"Durbin",
    r"[Ww]alk-forward", r"[Ee]xpanding[- ]window validation", r"[Rr]olling[- ]window validation",
    r"[Rr]ecursive forecast", r"[Dd]irect forecast", r"[Mm]ulti-output", r"[Hh]oldout",
    r"\bMAE\b", r"\bMSE\b", r"\bRMSE\b", r"\bMAPE\b", r"\bWAPE\b", r"\bMASE\b", r"[Ff]orecast skill",
    r"[Pp]rediction interval", r"[Nn]etback", r"[Bb]oil-off", r"[Bb]reak-even", r"\bFOB\b", r"\bDES\b",
    r"[Ff]reight", r"DuckDB",
]


def check_exclusions():
    section("4. excluded models and tests in Quantitative Methods")
    base = os.path.join(ROOT, "problems", "quant")
    hits = 0
    for folder, _dirs, files in os.walk(base):
        for name in files:
            if not name.endswith((".md", ".py", ".json")):
                continue
            path = os.path.join(folder, name)
            text = server.read_text(path)
            for pattern in EXCLUDED:
                for m in re.finditer(pattern, text):
                    hits += 1
                    line = text[:m.start()].count("\n") + 1
                    check(False, "excluded term %r in %s:%d" % (m.group(0), os.path.relpath(path, ROOT), line))
    print("   %d forbidden term(s) found" % hits)


def check_code_style():
    section("5. plain, explicit reference solutions")
    base = os.path.join(ROOT, "problems", "quant")
    rules = [(r"^\s*class\s", "a class"), (r"\blambda\b", "a lambda"), (r"functools|reduce\(|\bmap\(", "functional tricks"),
             (r"\[[^\]]*\bfor\b[^\]]*\[[^\]]*\bfor\b", "a nested comprehension"), (r"\.pipe\(|\.apply\(", "pipe/apply chains"),
             (r"\.assign\(", "assign chains")]
    files = 0
    for folder in sorted(os.listdir(base)):
        path = os.path.join(base, folder, "solution.py")
        if not os.path.isfile(path):
            continue
        files += 1
        text = server.read_text(path)
        for pattern, label in rules:
            check(not re.search(pattern, text, re.M), "%s: %s" % (os.path.relpath(path, ROOT), label))
        functions = len(re.findall(r"^def ", text, re.M))
        check(functions <= 2, "%s: %d functions (one logical operation per exercise)" % (os.path.relpath(path, ROOT), functions))
        long_lines = [i + 1 for i, line in enumerate(text.splitlines()) if len(line) > 120]
        check(not long_lines, "%s: lines longer than 120 characters %s" % (os.path.relpath(path, ROOT), long_lines))
    print("   %d reference solutions scanned" % files)


# ---------------------------------------------------------------------------
def check_outcomes():
    """The teaching notes quote results. Check that the data still produce them."""
    section("6. results quoted by the teaching notes")
    import numpy as np
    import pandas as pd
    warnings.simplefilter("ignore")
    base = os.path.join(ROOT, "problems", "quant")
    here = os.getcwd()
    os.chdir(base)                       # solutions read data/<file>.csv
    try:
        def fn(folder, name):
            ns = {}
            exec(compile(server.read_text(os.path.join(base, folder, "solution.py")), folder, "exec"), ns)
            return ns[name]

        def csv(name, date_column=None):
            if date_column:
                return pd.read_csv("data/" + name, parse_dates=[date_column], index_col=date_column)
            return pd.read_csv("data/" + name)

        # ---- Project 1
        vendor = "data/p1_crude_prices_vendor_synthetic.csv"
        profile = fn("p1-1-profile-raw-file", "profile_raw_file")(pd.read_csv(vendor))
        check(profile["exact_duplicate_rows"] == 5 and profile["repeated_dates"] == 7, "1.1: duplicates")
        check(not profile["dates_in_order"], "1.1: the raw file should be out of order")
        loaded = fn("p1-2-load-prices", "load_crude_prices")(vendor)
        flags = fn("p1-3-quality-checks", "quality_checks")(loaded)
        check(list(flags["action"]) == ["keep and document", "set to NaN"], "1.3: one event kept, one error removed")
        clean = loaded.copy()
        for _, flag in flags.iterrows():
            if flag["action"] == "set to NaN":
                clean.loc[flag["date"], flag["series"]] = np.nan
        provided = csv("p1_crude_prices_clean_synthetic.csv", "date")
        check(np.allclose(clean.to_numpy(), provided.to_numpy(), equal_nan=True) and clean.index.equals(provided.index),
              "1.3: the committed clean layer is not reproduced by the reference rules")
        corr = fn("p1-7-correlation", "correlation_report")(provided, "brent", "wti")
        check(corr["pearson_changes"] < 0.5 < corr["spearman_changes"], "1.7: the event must separate Pearson and Spearman")

        # ---- Project 2
        raw = csv("p2_products_daily_synthetic.csv", "date")
        check(len(raw) - len(raw.drop_duplicates()) > raw.index.duplicated().sum(), "2.2: drop_duplicates pitfall")
        treated = fn("p2-2-gaps-and-stale-prices", "treat_gaps")(raw)["prices"]
        provided = csv("p2_products_treated_synthetic.csv", "date")
        check(np.allclose(treated.to_numpy(), provided.to_numpy(), equal_nan=True), "2.2: treated layer not reproduced")
        imports = fn("p2-3-zeros-or-missing", "total_imports")(csv("p2_diesel_imports_monthly_synthetic.csv"))
        check(np.isnan(imports.loc["2018-08-01", "total"]) and np.isnan(imports["total"].iloc[-1]), "2.3: non-reports")
        rbob = np.log(provided["rbob_usd_gal"].dropna()).diff()
        scores = fn("p2-4-outlier-scores", "outlier_scores")(rbob)
        check(abs(scores.loc["2017-08-28", "z"]) < 3 < abs(scores.loc["2017-08-28", "modified_z"]), "2.4: masking")
        usd = pd.DataFrame({"rbob": provided["rbob_usd_gal"] * 42, "ulsd": provided["ulsd_usd_gal"] * 42,
                            "gasoil": provided["gasoil_usd_t"] / 7.45}).dropna()
        decisions = fn("p2-5-error-or-event", "classify_extremes")(np.log(usd).diff().dropna(), "rbob")
        check(list(decisions["classification"]) == ["market event", "data error", "reversal of an error"],
              "2.5: classification is %s" % list(decisions["classification"]))
        cracks = pd.DataFrame({"diesel_crack": provided["ulsd_usd_gal"] * 42 - provided["brent_usd_bbl"],
                               "gasoil_crack": provided["gasoil_usd_t"] / 7.45 - provided["brent_usd_bbl"]})
        truncation = fn("p3-6-truncation-test", "truncation_test")
        build = fn("p2-6-features", "build_features")
        for cutoff in ["2017-12-29", "2018-06-29", "2019-03-29"]:
            check(truncation(build, cracks, cutoff) == [], "2.6: a feature changes when data after %s are removed" % cutoff)
        both = np.log(usd[["ulsd", "gasoil"]]).diff()
        lead = fn("p2-7-lead-lag", "lead_lag_table")(both["ulsd"], both["gasoil"], 2)
        check(lead.loc[1] > 0.25 and abs(lead.loc[-1]) < 0.1, "2.7: settlement-time lead")

        # ---- Project 3
        stocks = fn("p3-1-five-dates", "add_availability")(csv("p3_us_crude_stocks_weekly_synthetic.csv"))
        check(stocks["backfilled"].sum() > 100, "3.1: backfill")
        prices = csv("p3_wti_daily_synthetic.csv")
        aligned = fn("p3-2-merge-asof", "align_stocks")(prices, stocks)
        check(aligned["age_days"].min() >= 5, "3.2: a report used before its release")
        predictive = fn("p3-3-fake-predictability", "predictive_correlation")
        wrong = predictive(prices, stocks, "week_ending")["corr"]
        right = predictive(prices, stocks, "available_at")["corr"]
        check(wrong < -0.1 and abs(right) < 0.05, "3.3: fake predictability (%.3f vs %.3f)" % (wrong, right))
        vintages = csv("p3_us_oil_demand_vintages_synthetic.csv")
        check(fn("p3-4-vintages", "as_of")(vintages, "2016-06-15").index[-1] == pd.Timestamp("2016-03-01"), "3.4: as-of view")
        dates = list(pd.date_range("2016-03-31", "2019-12-31", freq="ME"))
        realtime = fn("p3-5-realtime-growth", "realtime_growth")(vintages, dates)
        crack = csv("p3_diesel_crack_monthly_synthetic.csv")
        crack["month"] = pd.to_datetime(crack["month"], format="%Y-%m")
        crack = crack.set_index("month")["diesel_crack_usd_bbl"]
        pit = np.corrcoef(crack.reindex(realtime.index.to_period("M").to_timestamp()).to_numpy(),
                          realtime["growth_realtime"])[0, 1]
        final = vintages.sort_values("vintage_date").groupby("obs_month")["demand_kbd"].last()
        final.index = pd.to_datetime(final.index, format="%Y-%m")
        pseudo = pd.concat([crack, final.pct_change(12) * 100], axis=1).dropna().corr().iloc[0, 1]
        check(pseudo - pit > 0.15, "3.5: pseudo point-in-time should overstate (%.2f vs %.2f)" % (pseudo, pit))

        # ---- Project 4
        p4 = csv("p4_crude_research_daily_synthetic.csv", "date")
        post = p4.loc["2016-07-01":]
        lb, lw, lc = np.log(post["brent"]), np.log(post["wti"]), np.log(post["coffee"])
        adf = fn("p4-4-adf", "adf_report")
        check(not adf(lb)["reject_unit_root"] and adf(lb.diff(), "n")["reject_unit_root"], "4.4: Brent I(1)")
        check(adf(lb - lw)["reject_unit_root"], "4.4: the spread should be I(0)")
        e = np.random.default_rng(0).normal(size=500)
        trend_stat = pd.Series(0.05 * np.arange(500) + e)
        check(not adf(trend_stat, "c")["reject_unit_root"] and adf(trend_stat, "ct")["reject_unit_root"], "4.4: c vs ct")
        trend = fn("p4-5-detrend-or-difference", "trend_or_random_walk")
        demand = csv("p4_diesel_demand_monthly_synthetic.csv", "month")["demand_kbd"]
        check(trend(demand)["decision"] == "detrend", "4.5: demand")
        check(trend(p4["brent"].resample("MS").mean())["decision"] == "difference", "4.5: Brent")
        table = fn("p4-3-model-selection", "compare_specifications")(np.log(post).diff().dropna())
        check(table["bic"].idxmin() == "brent", "4.3: BIC should prefer the Brent-only model")
        check(table.loc["brent + dubai", "brent_se"] > 2 * table.loc["brent", "brent_se"], "4.3: multicollinearity")
        spurious = fn("p4-6-spurious-regression", "levels_vs_differences")
        check(spurious(lc, lb)["verdict"] == "spurious" and spurious(lw, lb)["verdict"] == "co-moving", "4.6: verdicts")
        eg = fn("p4-7-engle-granger", "engle_granger")
        check(eg(lw, lb)["cointegrated"], "4.7: WTI~Brent cointegrated")
        trap = eg(lc, lb)
        check(trap["naive_pvalue"] < 0.05 < trap["eg_pvalue"], "4.7: the naive-vs-EG trap must be visible")
        ecm = fn("p4-8-ecm", "fit_ecm")(lw, lb)
        check(-0.2 < ecm["alpha"] < -0.05 and ecm["alpha_tstat"] < -3, "4.8: alpha")
        regimes = fn("p4-9-regimes", "regime_comparison")(p4[["brent", "wti"]], "2016-01-01")
        check(regimes["full_eg_pvalue"] > 0.05 > max(regimes["pre"]["eg_pvalue"], regimes["post"]["eg_pvalue"]),
              "4.9: the break must hide cointegration on the full sample only")
        chow = fn("p4-10-chow", "chow_test")
        hb, hw = np.log(p4["brent"]), np.log(p4["wti"])
        after, before = p4.index >= "2016-07-01", p4.index < "2016-01-01"
        check(chow(hw.diff(), hb.diff(), "2016-01-01")["reject"], "4.10: break")
        check(not chow(hw[after].diff(), hb[after].diff(), "2018-01-01")["reject"], "4.10: placebo 2018")
        check(not chow(hw[before].diff(), hb[before].diff(), "2014-01-01")["reject"], "4.10: placebo 2014")
        check(chow(hw[after], hb[after], "2018-01-01")["reject"], "4.10: the levels pitfall must be visible")
        print("   all quoted results hold")
    finally:
        os.chdir(here)


def check_judge():
    section("7. judge: reference solutions, starters, test-code pads")
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
            line += " · test code %s" % ("runs" if ran else "FAILS")
        print(line)


# ---------------------------------------------------------------------------
def check_progress():
    section("8. progress file")
    data = server.read_json(server.PROGRESS_FILE) or {"problems": {}}
    recorded = data.get("problems", {})
    active = {p["id"] for p in server.list_problems()}
    archived = {"glencore/" + d for d in os.listdir(os.path.join(ROOT, "archive", "glencore-mcq"))}
    renamed = {}
    for p in server.list_problems():
        for old in p.get("previous_ids", []):
            renamed[old] = p["id"]
    for pid in recorded:
        check(pid in active or pid in archived or pid in renamed,
              "progress entry %s matches no active, archived or renamed problem" % pid)
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
    section("9. written answers: draft -> submit -> self-review (scratch progress file)")
    tmp = tempfile.mkdtemp(prefix="practice-check-")
    saved = server.PROGRESS_FILE, server.DATA
    try:
        server.DATA = tmp
        server.PROGRESS_FILE = os.path.join(tmp, "progress.json")
        if os.path.exists(saved[0]):
            shutil.copyfile(saved[0], server.PROGRESS_FILE)
        before = copy.deepcopy(server.load_progress())
        for pid in ("glencore/q17-ai-follow-up-question", "quant/p1-8-debrief", "quant/p4-11-research-defence"):
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
    check_quant_track()
    check_exclusions()
    check_code_style()
    check_outcomes()
    if not fast:
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
