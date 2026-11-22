#!/usr/bin/env python3
"""End-to-end checks of the question banks and the app — run before trusting a change.

    python3 tools/check_all.py            everything (takes a minute or two)
    python3 tools/check_all.py --fast     skip running the judge on every problem

What it verifies
  1. metadata of every problem is valid (same rules as  server.py --check)
  2. Past Interview Questions: 15 Millennium + 8 Glencore problems, no MCQ, globally
     ordered by difficulty, every problem has an identifiable source
  3. Quantitative Methods: cases ordered, steps contiguous, difficulty non-decreasing
     inside each case, every written question has a rubric
  4. none of the excluded topics appears in the Quantitative Methods material
  5. every reference solution is ACCEPTED by the real judge, every starter is NOT,
     and every "Test code" pad runs without error against the reference solution
  6. the progress file loads, and every id recorded in it is either an active problem
     or an archived MCQ (nothing lost)
  7. the written-answer flow (draft -> submit -> self-review) works, on a scratch copy
     of the progress file (your real progress is never touched)

Exit code 0 when everything passes.
"""
import copy
import json
import os
import re
import shutil
import sys
import tempfile

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
    probs = [p for p in server.list_problems() if p["track"] == "interview"]
    by_set = {}
    for p in probs:
        by_set.setdefault(p["set"], []).append(p)
    mill, glen = by_set.get("millennium", []), by_set.get("glencore", [])
    check(len(mill) == 15, "expected 15 Millennium exercises, found %d" % len(mill))
    check(len(glen) == 8, "expected 8 Glencore exercises (6 code, 1 SQL, 1 written), found %d" % len(glen))
    kinds = sorted(p["type"] for p in glen)
    check(kinds == ["code"] * 6 + ["open", "sql"], "Glencore types are %s" % kinds)
    check(not [p for p in probs if p["type"] == "mcq"], "an MCQ is still active")
    archived = sorted(os.listdir(os.path.join(ROOT, "archive", "glencore-mcq")))
    archived = [a for a in archived if os.path.isdir(os.path.join(ROOT, "archive", "glencore-mcq", a))]
    check(len(archived) == 9, "expected 9 archived Glencore MCQs, found %d" % len(archived))
    for a in archived:
        meta = server.read_json(os.path.join(ROOT, "archive", "glencore-mcq", a, "meta.json")) or {}
        check(meta.get("type") == "mcq", "archived %s is not an MCQ" % a)
    diffs = [p["difficulty"] for p in probs]
    check(diffs == sorted(diffs), "interview list is not ordered by difficulty: %s" % diffs)
    check(len({p["set"] for p in probs[:10]}) == 2, "the two sources are not interleaved in the first levels")
    for p in probs:
        check(p.get("source") in ("Glencore", "Millennium × AmplifyME"), "%s: source %r" % (p["id"], p.get("source")))
        check(bool(p.get("difficulty_why")), "%s: no difficulty rationale" % p["id"])
    follows = {p["id"]: i for i, p in enumerate(probs)}
    q17 = follows.get("glencore/q17-ai-follow-up-question")
    q16 = follows.get("glencore/q16-loyal-and-satisfied-employees")
    check(q16 is not None and q17 is not None and q17 > q16, "Q17 must come after the SQL query it follows")
    print("   Millennium %d · Glencore %d · archived MCQs %d · levels %s" % (len(mill), len(glen), len(archived), diffs))


def check_quant_track():
    section("3. Quantitative Methods")
    probs = [p for p in server.list_problems() if p["track"] == "quant"]
    cases = [c["id"] for c in server.list_cases() if c["track"] == "quant"]
    order = [cases.index(p["case"]) for p in probs]
    check(order == sorted(order), "quant problems are not ordered by case")
    for c in cases:
        mine = [p for p in probs if p["case"] == c]
        steps = [p["step"] for p in mine]
        check(steps == list(range(1, len(mine) + 1)), "%s: steps are %s" % (c, steps))
        diffs = [p["difficulty"] for p in mine]
        check(diffs == sorted(diffs), "%s: difficulty decreases inside the case: %s" % (c, diffs))
        check(mine and mine[-1]["type"] == "open", "%s should end with a written debrief" % c)
        print("   %s: %d steps, levels %s" % (c, len(mine), diffs))
    for p in probs:
        meta, _ = server.load_meta(p["id"])
        if meta["type"] == "open":
            check(len(meta.get("rubric", [])) >= 4, "%s: rubric too short" % p["id"])
        else:
            check(bool((meta.get("explain") or {}).get("rubric")), "%s: code exercise without explanation rubric" % p["id"])
    print("   %d cases, %d exercises (%d code, %d written)" % (
        len(cases), len(probs), sum(p["type"] == "code" for p in probs), sum(p["type"] == "open" for p in probs)))


# Terms that must never appear in the learning path (see the README: scope of the track).
EXCLUDED = [
    r"\bAR\(", r"\bMA\(", r"\bARMA\b", r"\bARIMA\b", r"\bSARIMAX?\b", r"[Ee]xponential [Ss]moothing",
    r"\bHolt\b", r"Holt-Winters", r"\bETS\b", r"\bVAR\b", r"\bVECM\b", r"multiple (linear )?regression",
    r"\bRidge\b", r"\bLasso\b", r"[Ee]lastic [Nn]et", r"[Qq]uantile regression", r"[Rr]andom [Ff]orest",
    r"[Gg]radient [Bb]oosting", r"XGB", r"\bKNN\b", r"\bSVM\b", r"[Kk]-means", r"[Nn]eural", r"\b[Ll]ogit\b",
    r"\b[Pp]robit\b", r"\b[Tt]obit\b", r"\bCAPM\b", r"\bAPT\b", r"[Ll]everage effect", r"Zakoian",
    r"Phillips", r"Johansen", r"Zivot", r"Bai-Perron", r"CUSUM", r"\bACF\b", r"\bPACF\b", r"plot_acf",
    r"Ljung", r"Breusch", r"ARCH", r"Diebold", r"Durbin",
    r"[Ww]alk-forward", r"[Ee]xpanding window", r"[Rr]olling window", r"[Hh]oldout", r"\.rolling\(",
    r"\bMAE\b", r"\bMSE\b", r"\bRMSE\b", r"\bMAPE\b", r"\bWAPE\b", r"\bMASE\b", r"[Ff]orecast skill",
    r"[Pp]rediction interval", r"[Nn]etback", r"[Bb]oil-off", r"[Bb]reak-even", r"[Pp]oint-in-[Tt]ime",
    r"\bPIT\b", r"[Vv]intage", r"[Pp]ublication lag", r"[Tt]runcation test", r"[Ff]eature engineering",
    r"\b[Ll]ag features?\b", r"[Cc]alendar features?", r"[Ss]caler\b", r"[Mm]in-max", r"[Zz]-score",
    r"\bIQR\b", r"[Ww]insor", r"DuckDB", r"\bSQL\b",
]


def check_exclusions():
    section("4. excluded topics in Quantitative Methods")
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


# ---------------------------------------------------------------------------
def judge_submit(meta, path, code):
    return server.judge("submit", meta, path, code)


def check_judge():
    section("5. judge: reference solutions, starters, test-code pads")
    for p in server.list_problems():
        meta, path = server.load_meta(p["id"])
        kind = meta["type"]
        if kind not in ("code", "sql"):
            continue
        ext = server.EXT[kind]
        solution = server.read_text(os.path.join(path, "solution." + ext))
        starter = server.read_text(os.path.join(path, "starter." + ext))
        res = judge_submit(meta, path, solution)
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
        res_starter = judge_submit(meta, path, starter)
        check(res_starter.get("status") != "accepted", "%s: the starter already passes the tests" % p["id"])
        line = "   %-55s solution %s" % (p["id"], "accepted" if ok else "REJECTED")
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
def check_quant_outcomes():
    """The teaching notes quote results (a verdict, a p-value side of 5 %, a sign). Check that the
    synthetic data still produce them, so that regenerating the data cannot silently break a lesson."""
    section("5b. Quantitative Methods: the outcomes the notes rely on")
    import warnings
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

        def persistent(n, phi, seed):
            e = np.random.default_rng(seed).normal(size=n)
            u = np.zeros(n)
            for t in range(n):
                u[t] = (phi * u[t - 1] if t else 0.0) + e[t]
            return pd.Series(u)

        ttf = pd.read_csv("data/ttf_daily_synthetic.csv", parse_dates=["date"], index_col="date")["ttf"]
        dem = pd.read_csv("data/diesel_demand_monthly_synthetic.csv", parse_dates=["month"], index_col="month")["demand_kbd"]
        cr = pd.read_csv("data/crude_daily_synthetic.csv", parse_dates=["date"], index_col="date")
        hist = pd.read_csv("data/crude_history_synthetic.csv", parse_dates=["date"], index_col="date")
        lb, lw, lc = np.log(cr["brent"]), np.log(cr["wti"]), np.log(cr["coffee"])
        e = np.random.default_rng(0).normal(size=500)
        trend_stat = pd.Series(0.05 * np.arange(500) + e)

        s = fn("case1-1-first-look", "summary_stats")
        lvl, ret = s(ttf), s(np.log(ttf).diff())
        check(lvl["mean"] > lvl["median"] and lvl["skew"] > 1, "1.1: TTF level should be right-skewed")
        check(ret["excess_kurtosis"] > 3, "1.1: TTF returns should be fat-tailed")
        adf = fn("case1-4-adf", "adf_report")
        check(not adf(ttf)["reject_unit_root"] and adf(np.log(ttf).diff())["reject_unit_root"], "1.4: TTF level / returns")
        check(not adf(trend_stat, "c")["reject_unit_root"] and adf(trend_stat, "ct")["reject_unit_root"], "1.4: c vs ct")
        check(not adf(persistent(40, 0.8, 0))["reject_unit_root"], "1.4: low-power example")
        check(not adf(persistent(600, 0.5, 1) + 2.0 * (np.arange(600) >= 300))["reject_unit_root"], "1.4: level shift")
        sv = fn("case1-5-kpss", "stationarity_verdict")
        expect = [(ttf, "c", "unit root"), (np.log(ttf).diff(), "c", "stationary"), (trend_stat, "c", "unit root"),
                  (trend_stat, "ct", "stationary"), (persistent(2000, 0.97, 1), "c", "conflict"),
                  (persistent(40, 0.8, 0), "c", "inconclusive")]
        for series, reg, verdict in expect:
            got = sv(series, reg)["verdict"]
            check(got == verdict, "1.5: expected %r, got %r" % (verdict, got))
        check(sv(persistent(40, 0.8, 3), "c", 0.05)["verdict"] == "inconclusive"
              and sv(persistent(40, 0.8, 3), "c", 0.10)["verdict"] == "stationary", "1.5: alpha example")
        tr = fn("case1-6-trend-or-random-walk", "trend_or_random_walk")
        d1, d2 = tr(dem), tr(ttf.resample("MS").mean())
        check(d1["decision"] == "detrend" and d1["std_differenced"] > d1["std_detrended"], "1.6: demand")
        check(d2["decision"] == "difference" and d2["std_detrended"] > d2["std_differenced"], "1.6: TTF monthly")
        cor = fn("case2-2-correlation", "correlation_report")(cr, "brent", "coffee")
        check(cor["pearson_levels"] > 0.6 and abs(cor["pearson_returns"]) < 0.1, "2.2: spurious level correlation")
        lv = fn("case2-4-spurious-regression", "levels_vs_differences")
        check(lv(lc, lb)["verdict"] == "spurious" and lv(lw, lb)["verdict"] == "co-moving", "2.4: verdicts")
        io = fn("case3-1-integration-order", "integration_order")
        check([io(lb)["order"], io(lw)["order"], io(lb - lw)["order"]] == [1, 1, 0], "3.1: orders")
        eg = fn("case3-2-engle-granger", "engle_granger")
        g1, g2 = eg(lw, lb), eg(lc, lb)
        check(g1["cointegrated"], "3.2: WTI~Brent should be cointegrated")
        check(g2["naive_pvalue"] < 0.05 < g2["eg_pvalue"], "3.2: the naive-vs-EG trap on coffee must be visible")
        ecm = fn("case3-3-ecm", "fit_ecm")(lw, lb)
        check(-0.2 < ecm["alpha"] < -0.05 and ecm["alpha_tstat"] < -3, "3.3: alpha negative and significant")
        rc = fn("case4-1-regimes", "regime_comparison")(hist, "2016-01-01")
        check(rc["full_eg_pvalue"] > 0.05 and rc["pre"]["eg_pvalue"] < 0.05 and rc["post"]["eg_pvalue"] < 0.05,
              "4.1: the break must hide cointegration on the full sample only")
        check(rc["pre"]["mean_spread"] > rc["post"]["mean_spread"] and rc["pre"]["return_beta"] < rc["post"]["return_beta"],
              "4.1: regime differences")
        chow = fn("case4-2-chow", "chow_test")
        hb, hw = np.log(hist["brent"]), np.log(hist["wti"])
        post, pre = hist.index >= "2016-07-01", hist.index < "2016-01-01"
        check(chow(hw.diff(), hb.diff(), "2016-01-01")["reject"], "4.2: break should be detected")
        check(not chow(hw[post].diff(), hb[post].diff(), "2018-01-01")["reject"], "4.2: placebo 2018")
        check(not chow(hw[pre].diff(), hb[pre].diff(), "2014-01-01")["reject"], "4.2: placebo 2014")
        check(chow(hw[post], hb[post], "2018-01-01")["reject"], "4.2: the levels pitfall must be visible")
        print("   all quoted outcomes hold")
    finally:
        os.chdir(here)


def check_progress():
    section("6. progress file")
    data = server.load_progress()
    active = {p["id"] for p in server.list_problems()}
    archived = {"glencore/" + d for d in os.listdir(os.path.join(ROOT, "archive", "glencore-mcq"))}
    for pid in data["problems"]:
        check(pid in active or pid in archived, "progress entry %s matches no active or archived problem" % pid)
    listing = server.api_problems({}, None)
    shown = {p["id"]: p["progress"]["status"] for p in listing["problems"]}
    for pid, entry in data["problems"].items():
        if pid in active:
            check(shown[pid] == entry.get("status", "todo"), "%s: status not shown in the list" % pid)
            detail = server.api_problem({"id": [pid]}, None)
            check(detail.get("draft") == entry.get("draft", {}), "%s: draft not returned" % pid)
    quant = [p for p in listing["problems"] if p["track"] == "quant"]
    print("   %d recorded problem(s): %s" % (len(data["problems"]), ", ".join(
        "%s=%s" % (k, v.get("status")) for k, v in data["problems"].items())))
    print("   quant problems with progress: %d (expected clean start)" % sum(
        p["progress"]["status"] != "todo" for p in quant))


def check_written_flow():
    section("7. written answers: draft -> submit -> self-review (scratch progress file)")
    tmp = tempfile.mkdtemp(prefix="practice-check-")
    saved = server.PROGRESS_FILE, server.DATA
    try:
        server.DATA = tmp
        server.PROGRESS_FILE = os.path.join(tmp, "progress.json")
        if os.path.exists(saved[0]):
            shutil.copyfile(saved[0], server.PROGRESS_FILE)
        before = copy.deepcopy(server.load_progress())
        for pid in ("glencore/q17-ai-follow-up-question", "quant/case1-7-debrief"):
            meta, _ = server.load_meta(pid)
            public = server.api_problem({"id": [pid]}, None)
            check("rubric" not in public, "%s: rubric leaked before submission" % pid)
            server.api_draft({}, {"id": pid, "text": "draft answer", "touched": True})
            check(server.api_problem({"id": [pid]}, None)["draft"]["text"] == "draft answer", "%s: draft not saved" % pid)
            empty = server.api_submit({}, {"id": pid, "text": "   "})
            check(isinstance(empty, tuple) and empty[0] == 400, "%s: an empty answer was accepted" % pid)
            sub = server.api_submit({}, {"id": pid, "text": "My answer: AND is an intersection."})
            check(sub["progress"]["status"] in ("attempted", "solved"), "%s: submit did not record" % pid)
            sol = server.api_solution({"id": [pid]}, None)
            check(len(sol["rubric"]) == len(meta["rubric"]) and sol["notes"], "%s: solution / rubric missing" % pid)
            partial = server.api_review({}, {"id": pid, "rubric": [0, 2], "mastered": False})
            check(partial["progress"]["status"] == "attempted", "%s: 'review again' changed the status" % pid)
            check(partial["submission"]["rubric"] == [0, 2], "%s: rubric ticks not saved" % pid)
            done = server.api_review({}, {"id": pid, "rubric": list(range(len(meta["rubric"]))), "mastered": True})
            check(done["progress"]["status"] == "solved", "%s: 'mastered' did not solve the problem" % pid)
            entry = server.load_progress()["problems"][pid]
            check(entry["submissions"][0]["text"].startswith("My answer"), "%s: answer text not kept" % pid)
            check(len(entry["submissions"]) == 1, "%s: the self-review should update, not duplicate, the submission" % pid)
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
    check_quant_outcomes()
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
