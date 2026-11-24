#!/usr/bin/env python3
"""Judge process. Started by server.py for every Run / Submit, never imported.

    runner.py <mode> <problem_dir> <code_file> <result_file> [<scratch_file>]

mode = run     execute the code (plus the scratch "test code"), print output
mode = submit  run the problem's test cases, write a JSON verdict to <result_file>

Only the Python standard library is required here; pandas / numpy / statsmodels
are imported by the problems that need them. Datasets listed in a problem's
meta.json ("data") are copied by the server into ./data/ of the working
directory, so code and tests read them with a relative path: "data/<file>.csv".

A test case may use "raises": "ValueError" instead of "expected" when the
function must refuse its input.
"""
import base64
import contextlib
import copy
import datetime
import io
import json
import linecache
import math
import os
import pprint
import signal
import sqlite3
import sys
import time
import traceback
import warnings

USER_FILE = "solution.py"
SCRATCH_FILE = "test_code.py"
TEST_TIMEOUT_S = 6          # same limit as the original screens ("Timeout: 6 seconds")
MAX_TEXT = 6000             # cap for any single displayed value / captured output


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def clip(text, limit=MAX_TEXT):
    text = str(text)
    if len(text) > limit:
        return text[:limit] + "\n… (truncated)"
    return text


def register_source(filename, code):
    """Let tracebacks show the user's own source lines."""
    linecache.cache[filename] = (len(code), None, code.splitlines(True), filename)


def user_traceback(exc):
    """Traceback restricted to the user's own frames (not the judge / pandas internals)."""
    if isinstance(exc, SyntaxError):
        return "".join(traceback.format_exception_only(type(exc), exc)).rstrip()
    frames = traceback.extract_tb(exc.__traceback__)
    mine = [f for f in frames if f.filename in (USER_FILE, SCRATCH_FILE)]
    lines = ["Traceback (most recent call last):\n"]
    lines += traceback.format_list(mine if mine else frames[-2:])
    lines += traceback.format_exception_only(type(exc), exc)
    return "".join(lines).rstrip()


class TestTimeout(Exception):
    pass


@contextlib.contextmanager
def time_limit(seconds):
    if not hasattr(signal, "SIGALRM"):      # Windows: the server's hard timeout still applies
        yield
        return

    def handler(signum, frame):
        raise TestTimeout("Time limit exceeded (%ss)" % seconds)

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


# ----------------------------------------------------------------------------
# value comparison / formatting (duck-typed so numpy & pandas stay optional)
# ----------------------------------------------------------------------------
def _mod(x):
    return type(x).__module__ or ""


def is_df(x):
    return type(x).__name__ == "DataFrame" and _mod(x).startswith("pandas")


def is_series(x):
    return type(x).__name__ == "Series" and _mod(x).startswith("pandas")


def unwrap(x):
    """numpy scalars -> plain Python values."""
    if _mod(x).startswith("numpy") and hasattr(x, "item") and getattr(x, "ndim", 1) == 0:
        return x.item()
    return x


def is_missing(x):
    if x is None:
        return False
    if isinstance(x, float):
        return math.isnan(x)
    return type(x).__name__ in ("NAType", "NaTType")


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


ABS_TOL = 1e-9      # default absolute tolerance; a test can override it with "abs_tol"


def close(a, e, tol):
    if math.isnan(a) or math.isnan(e):
        return math.isnan(a) and math.isnan(e)
    return abs(a - e) <= max(ABS_TOL, tol * abs(e))


def compare(actual, expected, tol=1e-6, path="result"):
    """Return None when equal, otherwise a short human-readable reason."""
    a, e = unwrap(actual), unwrap(expected)

    if is_df(e):
        return compare_df(a, e, tol, path)
    if is_series(e):
        return compare_series(a, e, tol, path)
    if e is None:
        return None if a is None else "%s: expected None, got %s" % (path, short(a))
    if isinstance(e, bool):
        if not isinstance(a, bool):
            return "%s: expected a bool (%r), got %s" % (path, e, short(a))
        return None if a == e else "%s: expected %r, got %r" % (path, e, a)
    if is_missing(e):
        return None if is_missing(a) else "%s: expected NaN, got %s" % (path, short(a))
    if is_num(e):
        if not is_num(a):
            return "%s: expected a number (%r), got %s" % (path, e, short(a))
        return None if close(float(a), float(e), tol) else "%s: expected %r, got %r" % (path, e, a)
    if isinstance(e, str):
        if not isinstance(a, str):
            return "%s: expected a str (%r), got %s" % (path, e, short(a))
        return None if a == e else "%s: expected %r, got %r" % (path, e, a)
    if isinstance(e, dict):
        if not isinstance(a, dict):
            return "%s: expected a dict, got %s" % (path, short(a))
        missing = [k for k in e if k not in a]
        extra = [k for k in a if k not in e]
        if missing or extra:
            msg = "%s: keys differ" % path
            if missing:
                msg += " — missing %r" % missing
            if extra:
                msg += " — unexpected %r" % extra
            return msg
        for k in e:
            why = compare(a[k], e[k], tol, "%s[%r]" % (path, k))
            if why:
                return why
        return None
    if isinstance(e, (list, tuple)):
        if is_series(a) or (_mod(a).startswith("numpy") and hasattr(a, "tolist")):
            a = a.tolist()
        if not isinstance(a, (list, tuple)):
            return "%s: expected a list, got %s" % (path, short(a))
        if len(a) != len(e):
            return "%s: expected %d items, got %d" % (path, len(e), len(a))
        for i, (x, y) in enumerate(zip(a, e)):
            why = compare(x, y, tol, "%s[%d]" % (path, i))
            if why:
                return why
        return None
    if isinstance(e, datetime.date) and not isinstance(e, datetime.datetime):
        if isinstance(a, datetime.datetime) or not isinstance(a, datetime.date):
            return "%s: expected a datetime.date (%r), got %s" % (path, e, short(a))
        return None if a == e else "%s: expected %r, got %r" % (path, e, a)
    try:
        same = bool(a == e)
    except Exception:
        same = False
    return None if same else "%s: expected %s, got %s" % (path, short(e), short(a))


def compare_index(a, e, path):
    """A RangeIndex in the expected value means 'reset the index'; any other index
    (dates, labels) must be reproduced exactly."""
    if list(e.index) == list(range(len(e))):
        if list(a.index) != list(range(len(a))):
            return "%s: index is not reset to 0..n-1 (got %r)" % (path, list(a.index)[:8])
        return None
    if not a.index.equals(e.index):
        for i, (x, y) in enumerate(zip(a.index, e.index)):
            if x != y:
                return "%s: index differs at position %d: expected %r, got %r" % (path, i, y, x)
        return "%s: index differs (expected %r…)" % (path, list(e.index)[:3])
    return None


def compare_cell(x, y, tol):
    x, y = unwrap(x), unwrap(y)
    if is_missing(y) or y is None:
        return is_missing(x) or x is None
    if is_num(y):
        return is_num(x) and not is_missing(x) and close(float(x), float(y), tol)
    return x == y or str(x) == str(y)


def compare_df(a, e, tol, path):
    if not is_df(a):
        return "%s: expected a DataFrame, got %s" % (path, short(a))
    if list(a.columns) != list(e.columns):
        return "%s: columns are %r, expected %r" % (path, list(a.columns), list(e.columns))
    if len(a) != len(e):
        return "%s: %d rows, expected %d" % (path, len(a), len(e))
    why = compare_index(a, e, path)
    if why:
        return why
    for col in e.columns:
        av, ev = a[col].tolist(), e[col].tolist()
        for i, (x, y) in enumerate(zip(av, ev)):
            if not compare_cell(x, y, tol):
                return "%s: row %d (%r), column %r: expected %r, got %r" % (
                    path, i, e.index[i], col, unwrap(y), unwrap(x))
    return None


def compare_series(a, e, tol, path):
    if not is_series(a):
        return "%s: expected a pandas Series, got %s" % (path, short(a))
    if len(a) != len(e):
        return "%s: %d values, expected %d" % (path, len(a), len(e))
    why = compare_index(a, e, path)
    if why:
        return why
    for i, (x, y) in enumerate(zip(a.tolist(), e.tolist())):
        if not compare_cell(x, y, tol):
            return "%s: value %d (%r): expected %r, got %r" % (path, i, e.index[i], unwrap(y), unwrap(x))
    return None


def short(x):
    text = fmt(x)
    first = text.splitlines()[0] if text else ""
    return (first[:80] + "…") if (len(first) > 80 or "\n" in text) else first


def fmt(x):
    """Readable text for inputs / outputs shown in the UI."""
    x = unwrap(x)
    try:
        if is_df(x):
            if len(x) == 0:
                return "Empty DataFrame — columns: %r" % list(x.columns)
            return clip(x.to_string(max_rows=60))
        if is_series(x):
            return clip(x.to_string(max_rows=60))
        if isinstance(x, (dict, list, tuple)):
            return clip(pprint.pformat(simplify(x), width=88, sort_dicts=False))
        return clip(repr(x))
    except Exception as exc:  # a broken __repr__ must not kill the judge
        return "<unprintable %s: %s>" % (type(x).__name__, exc)


def simplify(x):
    x = unwrap(x)
    if isinstance(x, dict):
        return {k: simplify(v) for k, v in x.items()}
    if isinstance(x, list):
        return [simplify(v) for v in x]
    if isinstance(x, tuple):
        return tuple(simplify(v) for v in x)
    return x


def snapshot_equal(before, after):
    """Used for 'do not mutate the input' checks."""
    if is_df(before):
        try:
            return bool(before.equals(after))
        except Exception:
            return False
    try:
        return bool(before == after)
    except Exception:
        return True


# ----------------------------------------------------------------------------
# loading code
# ----------------------------------------------------------------------------
def load_module(code, filename, name):
    register_source(filename, code)
    ns = {"__name__": name, "__file__": filename}
    exec(compile(code, filename, "exec"), ns)
    return ns


class AnswerProxy(object):
    """`Answer.my_function(...)` — the way the original CoderPad test code calls you."""

    def __init__(self, ns):
        object.__setattr__(self, "_ns", ns)

    def __getattr__(self, item):
        try:
            return self._ns[item]
        except KeyError:
            raise AttributeError("your code does not define %r" % item)


# ----------------------------------------------------------------------------
# python: run
# ----------------------------------------------------------------------------
MAX_FIGURES = 6
FIGURE_FILE = "figures.json"   # read back by server.py and shown under the output


def save_figures():
    """Save every open matplotlib figure as a PNG (base64) so the app can display it.

    Charts are optional: nothing happens if the code never imported matplotlib."""
    if "matplotlib.pyplot" not in sys.modules:
        return
    plt = sys.modules["matplotlib.pyplot"]
    images = []
    for number in plt.get_fignums()[:MAX_FIGURES]:
        figure = plt.figure(number)
        buf = io.BytesIO()
        figure.savefig(buf, format="png", dpi=90, bbox_inches="tight")
        images.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    extra = len(plt.get_fignums()) - len(images)
    plt.close("all")
    with open(FIGURE_FILE, "w", encoding="utf-8") as f:
        json.dump({"images": images, "not_shown": max(extra, 0)}, f)


def py_run(code, scratch):
    # Charts are drawn off-screen (no window pops up); plt.show() is then a silent no-op.
    os.environ["MPLBACKEND"] = "Agg"
    warnings.filterwarnings("ignore", message=".*non-interactive.*")
    warnings.filterwarnings("ignore", message=".*cannot be shown.*")
    try:
        ns = load_module(code, USER_FILE, "__main__")
        if scratch.strip():
            # The test code sees your names (and `Answer.<name>`), but lives in its own
            # namespace: an import made there does not leak into your solution.
            register_source(SCRATCH_FILE, scratch)
            scratch_ns = dict(ns)
            scratch_ns["Answer"] = AnswerProxy(ns)
            exec(compile(scratch, SCRATCH_FILE, "exec"), scratch_ns)
    except SystemExit:
        raise
    except BaseException as exc:
        sys.stdout.flush()
        sys.stderr.write(user_traceback(exc) + "\n")
        sys.stderr.flush()
        save_figures()
        return 1
    save_figures()
    return 0


# ----------------------------------------------------------------------------
# python: submit
# ----------------------------------------------------------------------------
def py_submit(problem_dir, code):
    started = time.time()
    out = {"kind": "tests", "status": "error", "passed": 0, "total": 0, "tests": [],
           "load_error": None, "load_output": ""}

    # the problem's tests may import pandas / numpy
    try:
        tests_ns = load_module(read(os.path.join(problem_dir, "tests.py")), "tests.py", "tests")
    except ImportError as exc:
        out["load_error"] = ("This problem needs a package that is not installed for this "
                             "Python (%s).\nInstall it with:  %s -m pip install pandas numpy statsmodels"
                             % (exc, sys.executable))
        return out
    func_name = tests_ns["FUNCTION"]
    tests = tests_ns["TESTS"]
    out["total"] = len(tests)

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf), time_limit(TEST_TIMEOUT_S):
            user_ns = load_module(code, USER_FILE, "solution")
    except BaseException as exc:
        out["load_output"] = clip(buf.getvalue())
        out["load_error"] = user_traceback(exc)
        return out
    out["load_output"] = clip(buf.getvalue())

    func = user_ns.get(func_name)
    if not callable(func):
        out["load_error"] = ("Function `%s` was not found in your code.\n"
                             "Keep the original function name and signature." % func_name)
        return out

    reference = None

    def get_reference():
        nonlocal reference
        if reference is None:
            sink = io.StringIO()
            with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                ref_ns = load_module(read(os.path.join(problem_dir, "solution.py")),
                                     "reference_solution.py", "reference")
            reference = ref_ns[func_name]
        return reference

    for index, test in enumerate(tests):
        res = {"name": test.get("name", "Test %d" % (index + 1)),
               "origin": test.get("origin", "extra"),
               "note": test.get("note", ""),
               "passed": False, "input": [], "call": "", "expected": "", "actual": "",
               "stdout": "", "error": "", "reason": "", "time_ms": 0}
        try:
            args = test["args"]()
            pristine = copy.deepcopy(args)
            res["input"] = [{"name": k, "value": fmt(v)} for k, v in pristine.items()]
            res["call"] = "%s(%s)" % (func_name, ", ".join(args.keys()))

            if "raises" in test:            # the function must raise this exception type
                expected = None
            elif "expected" in test:
                expected = test["expected"]
                if callable(expected):
                    expected = expected()
            else:
                sink = io.StringIO()
                with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                    expected = get_reference()(*copy.deepcopy(pristine).values())
            res["expected"] = ("raises %s" % test["raises"]) if "raises" in test else fmt(expected)
        except BaseException as exc:
            res["error"] = "Judge error while preparing this test:\n" + "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__))
            out["tests"].append(res)
            continue

        buf = io.StringIO()
        t0 = time.time()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf), time_limit(TEST_TIMEOUT_S):
                actual = func(*args.values())
            res["time_ms"] = round((time.time() - t0) * 1000, 1)
            res["actual"] = fmt(actual)
            global ABS_TOL
            ABS_TOL = test.get("abs_tol", 1e-9)
            if "raises" in test:
                why = "expected the function to raise %s, but it returned a value" % test["raises"]
            else:
                why = compare(actual, expected, test.get("tol", 1e-6))
            if not why and test.get("check_no_mutation"):
                for key in pristine:
                    if not snapshot_equal(pristine[key], args[key]):
                        why = "the input `%s` was modified in place (work on a copy)" % key
                        break
            res["passed"] = why is None
            res["reason"] = why or ""
        except BaseException as exc:
            res["time_ms"] = round((time.time() - t0) * 1000, 1)
            wanted = test.get("raises")
            if (wanted and isinstance(exc, Exception) and not isinstance(exc, TestTimeout)
                    and any(k.__name__ == wanted for k in type(exc).__mro__)):
                res["passed"] = True
                res["actual"] = "raised %s: %s" % (type(exc).__name__, clip(exc, 300))
            else:
                res["error"] = user_traceback(exc)
                if wanted:
                    res["reason"] = "expected %s, got %s" % (wanted, type(exc).__name__)
        res["stdout"] = clip(buf.getvalue())
        out["tests"].append(res)

    out["passed"] = sum(1 for t in out["tests"] if t["passed"])
    out["status"] = "accepted" if out["passed"] == out["total"] and out["total"] else "wrong"
    out["runtime_ms"] = round((time.time() - started) * 1000)
    return out


# ----------------------------------------------------------------------------
# sql
# ----------------------------------------------------------------------------
def sql_statements(script):
    """Split a script into complete statements (handles ';' inside strings/comments)."""
    statements, current = [], ""
    for line in script.splitlines(True):
        current += line
        if sqlite3.complete_statement(current):
            statements.append(current)
            current = ""
    if current.strip():
        statements.append(current)
    return statements


def sql_execute(problem_dir, query):
    conn = sqlite3.connect(":memory:")
    conn.executescript(read(os.path.join(problem_dir, "dataset.sql")))
    columns, rows = None, None
    for statement in sql_statements(query):
        cur = conn.execute(statement)
        if cur.description:
            columns = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchmany(2000)]
    conn.close()
    return columns, rows


def sql_display(columns, rows, formats):
    shown = []
    for row in rows:
        cells = []
        for col, value in zip(columns, row):
            pattern = formats.get(col.lower())
            if pattern and is_num(value):
                cells.append(pattern % value)
            elif value is None:
                cells.append("NULL")
            else:
                cells.append(str(value))
        shown.append(cells)
    return shown


def sql_judge(problem_dir, query, check):
    meta = json.loads(read(os.path.join(problem_dir, "meta.json")))
    formats = {k.lower(): v for k, v in meta.get("sql_formats", {}).items()}
    out = {"kind": "sql", "status": "error", "error": "", "reason": "",
           "columns": [], "rows": [], "row_count": 0}
    try:
        with time_limit(TEST_TIMEOUT_S):
            columns, rows = sql_execute(problem_dir, query)
    except BaseException as exc:
        out["error"] = "%s: %s" % (type(exc).__name__, exc)
        return out
    if columns is None:
        out["error"] = "Your script did not return any rows (no SELECT statement was executed)."
        return out
    out["columns"], out["row_count"] = columns, len(rows)
    out["rows"] = sql_display(columns, rows[:200], formats)
    if not check:
        out["status"] = "ran"
        return out

    exp_cols, exp_rows = sql_execute(problem_dir, read(os.path.join(problem_dir, "solution.sql")))
    out["expected_columns"] = exp_cols
    out["expected_rows"] = sql_display(exp_cols, exp_rows[:200], formats)
    out["expected_row_count"] = len(exp_rows)

    why = None
    if [c.lower() for c in columns] != [c.lower() for c in exp_cols]:
        why = "Columns are %s — expected %s, in that order." % (", ".join(columns), ", ".join(exp_cols))
    elif len(rows) != len(exp_rows):
        why = "Your query returns %d rows — expected %d." % (len(rows), len(exp_rows))
    else:
        for i, (got, exp) in enumerate(zip(rows, exp_rows)):
            if compare(got, exp, 1e-9) is not None:
                if sorted(map(repr, rows)) == sorted(map(repr, exp_rows)):
                    why = "Right rows, wrong order (first difference at row %d)." % (i + 1)
                else:
                    why = "Row %d differs: got %s — expected %s." % (
                        i + 1, sql_display(columns, [got], formats)[0],
                        sql_display(exp_cols, [exp], formats)[0])
                break
    out["status"] = "accepted" if why is None else "wrong"
    out["reason"] = why or ""
    return out


# ----------------------------------------------------------------------------
def main():
    mode, problem_dir, code_file, result_file = sys.argv[1:5]
    scratch = read(sys.argv[5]) if len(sys.argv) > 5 else ""
    code = read(code_file)
    meta = json.loads(read(os.path.join(problem_dir, "meta.json")))

    if meta["type"] == "sql":
        result = sql_judge(problem_dir, code, check=(mode == "submit"))
    elif mode == "run":
        return py_run(code, scratch)
    else:
        result = py_submit(problem_dir, code)

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
