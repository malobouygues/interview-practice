#!/usr/bin/env python3
"""Interview Practice — a small local judge.

    python3 server.py            start on http://127.0.0.1:8790 and open the browser
    python3 server.py --port N   use another port
    python3 server.py --no-browser
    python3 server.py --check    validate every problem's metadata and files, then exit
    python3 server.py --data DIR keep progress in DIR/progress.json instead of ./data

Everything stays on this machine: the server only listens on 127.0.0.1, problems
are read from ./problems and your progress is written to ./data/progress.json.
Standard library only (pandas / numpy / statsmodels are needed by the exercises
that use them, not by the server).

Problems live in ./problems/<folder>/<problem>/. Each <folder> has a set.json that
says which learning track it belongs to ("interview" or "quant") and which source
it comes from; the tracks themselves are described in ./problems/tracks.json.
A problem's id is "<folder>/<problem>" — ids never change, so progress survives
any re-ordering.
"""
import argparse
import copy
import datetime
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(ROOT, "web")
PROBLEMS = os.path.join(ROOT, "problems")
TRACKS_FILE = os.path.join(PROBLEMS, "tracks.json")
DATA = os.path.join(ROOT, "data")
PROGRESS_FILE = os.path.join(DATA, "progress.json")
RUNNER = os.path.join(ROOT, "judge", "runner.py")

RUN_TIMEOUT_S = 20
SUBMIT_TIMEOUT_S = 90
MAX_OUTPUT = 200000
MAX_SUBMISSIONS_KEPT = 25
EXT = {"code": "py", "sql": "sql"}
TYPES = ("code", "sql", "open", "mcq")
DIFFICULTY_LABELS = {1: "Warm-up", 2: "Foundations", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
APP_VERSION = 3          # bump together with APP_VERSION in web/app.js and the ?v= in web/index.html


# ----------------------------------------------------------------------------
# problems (re-read from disk on every request, so edits show up immediately)
# ----------------------------------------------------------------------------
def read_text(path, default=""):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return default


def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def list_tracks():
    data = read_json(TRACKS_FILE) or {}
    tracks = data.get("tracks") or [{"id": "interview", "title": "Problems", "ordering": "difficulty"}]
    for i, t in enumerate(tracks):
        t.setdefault("order", i + 1)
        t.setdefault("ordering", "difficulty")
    tracks.sort(key=lambda t: t["order"])
    return tracks


def list_sets():
    sets = []
    for name in sorted(os.listdir(PROBLEMS)):
        info = read_json(os.path.join(PROBLEMS, name, "set.json"))
        if info is None:
            continue
        info["id"] = name
        info.setdefault("track", "interview")
        info.setdefault("source", info.get("title", name))
        sets.append(info)
    sets.sort(key=lambda s: (s.get("order", 99), s["id"]))
    return sets


def list_projects():
    """Ordered research projects of every set (the Quantitative Methods track)."""
    projects = []
    for s in list_sets():
        for project in s.get("projects", []):
            item = dict(project)
            item["set"] = s["id"]
            item["track"] = s["track"]
            projects.append(item)
    return projects


def sort_key(meta, track, project_rank):
    if track.get("ordering") == "project":
        return (project_rank.get(meta.get("project"), 999), meta.get("step", 999), meta["id"])
    return (meta.get("difficulty", 9), meta.get("sequence", 999), meta["id"])


def list_problems():
    """Every active problem, in display order: track by track, then by the track's ordering
    (global difficulty for interview questions, project then step for Quantitative Methods)."""
    tracks = list_tracks()
    track_rank = {t["id"]: i for i, t in enumerate(tracks)}
    track_by_id = {t["id"]: t for t in tracks}
    project_rank = {p["id"]: i for i, p in enumerate(list_projects())}
    problems = []
    for s in list_sets():
        base = os.path.join(PROBLEMS, s["id"])
        for folder in sorted(os.listdir(base)):
            meta = read_json(os.path.join(base, folder, "meta.json"))
            if meta is None:
                continue
            meta["id"] = "%s/%s" % (s["id"], folder)
            meta["set"] = s["id"]
            meta["track"] = s["track"]
            meta.setdefault("source", s["source"])
            problems.append(meta)
    problems.sort(key=lambda m: (track_rank.get(m["track"], 99),
                                 sort_key(m, track_by_id.get(m["track"], {}), project_rank)))
    return problems


def problem_dir(pid):
    """Resolve an id like 'glencore/q08-is-foo' to its folder, refusing path tricks."""
    parts = pid.split("/")
    if len(parts) != 2 or any(p in ("", ".", "..") or "\\" in p for p in parts):
        return None
    path = os.path.join(PROBLEMS, parts[0], parts[1])
    return path if os.path.isfile(os.path.join(path, "meta.json")) else None


def load_meta(pid):
    path = problem_dir(pid)
    if not path:
        return None, None
    meta = read_json(os.path.join(path, "meta.json"))
    if meta is None:
        return None, None
    info = read_json(os.path.join(PROBLEMS, pid.split("/")[0], "set.json")) or {}
    meta["id"] = pid
    meta["set"] = pid.split("/")[0]
    meta["track"] = info.get("track", "interview")
    meta.setdefault("source", info.get("source", info.get("title", meta["set"])))
    return meta, path


def public_meta(meta):
    """What the list / problem views may see (never the answer key nor the rubric)."""
    hidden = ("answer", "rubric")
    out = {k: v for k, v in meta.items() if k not in hidden}
    if isinstance(meta.get("explain"), dict):
        out["explain"] = {"prompt": meta["explain"].get("prompt", "")}
    return out


def data_file(path, name):
    """A dataset named in meta.json: looked up next to the problem, then in the set's data/."""
    name = os.path.basename(name)
    for candidate in (os.path.join(path, name), os.path.join(os.path.dirname(path), "data", name)):
        if os.path.isfile(candidate):
            return candidate
    return None


# ----------------------------------------------------------------------------
# metadata validation (python3 server.py --check, also printed at start-up)
# ----------------------------------------------------------------------------
def validate():
    """Return a list of human-readable problems with the problem metadata / files."""
    issues = []
    tracks = {t["id"]: t for t in list_tracks()}
    project_ids = {p["id"] for p in list_projects()}
    seen_sequence = {}
    for s in list_sets():
        if s["track"] not in tracks:
            issues.append("%s/set.json: unknown track %r" % (s["id"], s["track"]))
    for meta in list_problems():
        pid, path = meta["id"], problem_dir(meta["id"])
        track = tracks.get(meta["track"], {})

        def bad(msg):
            issues.append("%s: %s" % (pid, msg))

        kind = meta.get("type")
        if kind not in TYPES:
            bad("type must be one of %s (got %r)" % (", ".join(TYPES), kind))
            continue
        for key in ("number", "title"):
            if not meta.get(key):
                bad("missing %r" % key)
        diff = meta.get("difficulty")
        if not isinstance(diff, int) or isinstance(diff, bool) or not 1 <= diff <= 5:
            bad("difficulty must be an integer from 1 to 5 (got %r)" % (diff,))
        if track.get("ordering") == "project":
            if meta.get("project") not in project_ids:
                bad("project %r is not declared in set.json" % (meta.get("project"),))
            if not meta.get("architectures"):
                bad("list the architectures of the source document the exercise covers (e.g. [\"A01\"])")
            if not isinstance(meta.get("step"), int):
                bad("step must be an integer")
        else:
            seq = meta.get("sequence")
            if not isinstance(seq, (int, float)) or isinstance(seq, bool):
                bad("sequence must be a number (tie-break inside a difficulty level)")
            elif (meta["track"], seq) in seen_sequence:
                bad("sequence %r already used by %s" % (seq, seen_sequence[(meta["track"], seq)]))
            else:
                seen_sequence[(meta["track"], seq)] = pid
        if kind == "mcq" and meta["track"] == "interview":
            bad("multiple-choice questions are archived, not part of the active interview track")
        needed = ["statement.md", "solution.md"]
        if kind == "code":
            needed += ["starter.py", "tests.py", "solution.py"]
        elif kind == "sql":
            needed += ["starter.sql", "solution.sql", "dataset.sql"]
        for name in needed:
            if not os.path.isfile(os.path.join(path, name)):
                bad("missing file %s" % name)
        if kind == "open" and meta["track"] == "quant" and not meta.get("rubric"):
            bad("written questions of the learning path need a rubric")
        if "rubric" in meta and not (isinstance(meta["rubric"], list) and all(isinstance(r, str) for r in meta["rubric"])):
            bad("rubric must be a list of strings")
        explain = meta.get("explain")
        if explain is not None and not (isinstance(explain, dict) and explain.get("prompt")):
            bad("explain must be an object with a prompt (and an optional rubric)")
        for name in meta.get("data", []):
            if not data_file(path, name):
                bad("dataset %s not found" % name)
        if meta.get("follows") and not problem_dir(meta["follows"]):
            bad("follows an unknown problem %r" % meta["follows"])
    return issues


# ----------------------------------------------------------------------------
# progress
# ----------------------------------------------------------------------------
_lock = threading.Lock()


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def load_progress():
    data = read_json(PROGRESS_FILE)
    if not isinstance(data, dict) or not isinstance(data.get("problems"), dict):
        data = {"version": 1, "problems": {}}
    carry_over_progress(data)
    return data


def carry_over_progress(data):
    """An exercise that was renamed lists its old ids in meta.json ("previous_ids").
    If it has no progress yet, the progress recorded under an old id is COPIED to the new id
    (the old entry is kept untouched). The copy is written to disk with the next save.
    Your code, explanation, answers and submissions are copied; the "Test code" pad is not,
    because it belongs to the old exercise and may read data files that no longer exist."""
    for meta in list_problems():
        if meta["id"] in data["problems"]:
            continue
        for old_id in meta.get("previous_ids", []):
            if old_id in data["problems"]:
                entry = copy.deepcopy(data["problems"][old_id])
                entry.get("draft", {}).pop("scratch", None)
                data["problems"][meta["id"]] = entry
                break


def save_progress(data):
    os.makedirs(DATA, exist_ok=True)
    tmp = PROGRESS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, PROGRESS_FILE)


def update_progress(pid, fn):
    with _lock:
        data = load_progress()
        entry = data["problems"].setdefault(pid, {})
        fn(entry)
        save_progress(data)
        return entry


def summary(entry):
    entry = entry or {}
    return {"status": entry.get("status", "todo"),
            "attempts": entry.get("attempts", 0),
            "solved_at": entry.get("solved_at"),
            "last_at": entry.get("last_at")}


def record_submission(pid, accepted, detail, payload):
    def apply(entry):
        entry["attempts"] = entry.get("attempts", 0) + 1
        entry["last_at"] = now()
        if accepted:
            entry["status"] = "solved"
            entry.setdefault("solved_at", entry["last_at"])
        elif entry.get("status") != "solved":
            entry["status"] = "attempted"
        item = {"at": entry["last_at"], "accepted": accepted, "detail": detail}
        item.update(payload)
        entry["submissions"] = ([item] + entry.get("submissions", []))[:MAX_SUBMISSIONS_KEPT]
    return update_progress(pid, apply)


# ----------------------------------------------------------------------------
# judge
# ----------------------------------------------------------------------------
def run_capped(cmd, cwd, timeout):
    """Run a child process, keep at most MAX_OUTPUT chars of merged output, kill on timeout."""
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
               PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    chunks, size = [], [0]

    def pump():
        for chunk in iter(lambda: proc.stdout.read(8192), b""):
            if size[0] < MAX_OUTPUT:
                chunks.append(chunk)
                size[0] += len(chunk)

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()
    timed_out = False
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        proc.wait()
    reader.join(timeout=2)
    text = b"".join(chunks).decode("utf-8", "replace")
    if len(text) >= MAX_OUTPUT:
        text = text[:MAX_OUTPUT] + "\n… (output truncated)"
    return proc.returncode, text, timed_out


def stage_data(meta, path, workdir):
    """Copy the problem's datasets into <workdir>/data/ so code reads 'data/<file>'."""
    names = meta.get("data", [])
    if not names:
        return
    target = os.path.join(workdir, "data")
    os.makedirs(target, exist_ok=True)
    for name in names:
        src = data_file(path, name)
        if src:
            shutil.copyfile(src, os.path.join(target, os.path.basename(name)))


def judge(mode, meta, path, code, scratch=""):
    ext = EXT.get(meta["type"], "txt")
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="practice-") as tmp:
        code_file = os.path.join(tmp, "solution." + ext)
        scratch_file = os.path.join(tmp, "test_code.py")
        result_file = os.path.join(tmp, "result.json")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(code)
        with open(scratch_file, "w", encoding="utf-8") as f:
            f.write(scratch or "")
        stage_data(meta, path, tmp)
        timeout = RUN_TIMEOUT_S if mode == "run" else SUBMIT_TIMEOUT_S
        returncode, output, timed_out = run_capped(
            [sys.executable, RUNNER, mode, path, code_file, result_file, scratch_file], tmp, timeout)
        result = read_json(result_file)
    elapsed = round((time.time() - started) * 1000)

    if result is None:          # plain "run" of Python code, or the judge itself died
        if mode == "run" and meta["type"] == "code":
            return {"kind": "console", "output": output, "exit_code": returncode,
                    "timed_out": timed_out, "elapsed_ms": elapsed}
        message = ("Time limit exceeded — the run was stopped after %ss." % timeout) if timed_out \
            else "The judge stopped unexpectedly."
        return {"kind": "crash", "status": "error", "error": message, "output": output,
                "elapsed_ms": elapsed}
    result["elapsed_ms"] = elapsed
    if output.strip():
        result["output"] = output
    return result


LIBS = ("pandas", "numpy", "statsmodels")


def environment():
    code = ("import sys, json\nout={'python': sys.version.split()[0], 'executable': sys.executable}\n"
            "for m in %r:\n"
            "    try:\n        out[m]=__import__(m).__version__\n"
            "    except Exception as e:\n        out[m]=None\n"
            "print(json.dumps(out))" % (LIBS,))
    try:
        raw = subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=60).stdout
        return json.loads(raw.decode("utf-8"))
    except Exception:
        out = {"python": sys.version.split()[0], "executable": sys.executable}
        out.update({m: None for m in LIBS})
        return out


_env_cache = {}


# ----------------------------------------------------------------------------
# API
# ----------------------------------------------------------------------------
LIST_FIELDS = ("id", "set", "track", "source", "number", "title", "type", "group", "difficulty",
               "book_difficulty", "debug", "time_limit_min", "project", "step", "sequence", "concepts",
               "architectures")


def api_problems(_query, _body):
    progress = load_progress()["problems"]
    items = []
    for meta in list_problems():
        item = {k: meta.get(k) for k in LIST_FIELDS}
        item["explain"] = bool(meta.get("explain"))
        item["progress"] = summary(progress.get(meta["id"]))
        items.append(item)
    return {"app_version": APP_VERSION, "tracks": list_tracks(), "sets": list_sets(),
            "projects": list_projects(), "difficulty_labels": DIFFICULTY_LABELS, "problems": items}


def api_problem(query, _body):
    pid = query.get("id", [""])[0]
    meta, path = load_meta(pid)
    if not meta:
        return 404, {"error": "Unknown problem"}
    progress = load_progress()["problems"]
    entry = progress.get(pid, {})
    ext = EXT.get(meta["type"])
    out = public_meta(meta)
    out["statement"] = read_text(os.path.join(path, "statement.md"))
    if ext:
        out["starter"] = read_text(os.path.join(path, "starter." + ext))
        out["test_code"] = read_text(os.path.join(path, "test_code.py"))
    out["progress"] = summary(entry)
    out["draft"] = entry.get("draft", {})
    out["submissions"] = entry.get("submissions", [])
    out["elapsed_s"] = entry.get("elapsed_s", 0)
    if meta.get("follows"):      # e.g. the follow-up question shows the query you submitted
        other = progress.get(meta["follows"], {})
        code = ""
        for sub in other.get("submissions", []):
            if sub.get("code"):
                code = sub["code"]
                break
        out["follows_code"] = code or other.get("draft", {}).get("code", "")
    return out


def api_solution(query, _body):
    pid = query.get("id", [""])[0]
    meta, path = load_meta(pid)
    if not meta:
        return 404, {"error": "Unknown problem"}
    ext = EXT.get(meta["type"])
    explain = meta.get("explain") if isinstance(meta.get("explain"), dict) else {}
    return {"answer": meta.get("answer"),
            "code": read_text(os.path.join(path, "solution." + ext)) if ext else "",
            "language": "sql" if meta["type"] == "sql" else "python",
            "notes": read_text(os.path.join(path, "solution.md")),
            "rubric": meta.get("rubric") or explain.get("rubric") or []}


def api_draft(_query, body):
    pid = body.get("id", "")
    meta, _path = load_meta(pid)
    if not meta:
        return 404, {"error": "Unknown problem"}

    def apply(entry):
        draft = entry.setdefault("draft", {})
        for key in ("code", "scratch", "answer", "text", "explanation", "rubric"):
            if key in body:
                draft[key] = body[key]
        if "elapsed_s" in body:
            entry["elapsed_s"] = body["elapsed_s"]
        if entry.get("status") is None and body.get("touched"):
            entry["status"] = "attempted"
    update_progress(pid, apply)
    return {"ok": True}


def api_run(_query, body):
    meta, path = load_meta(body.get("id", ""))
    if not meta or meta["type"] not in EXT:
        return 404, {"error": "This problem has nothing to run"}
    return judge("run", meta, path, body.get("code", ""), body.get("scratch", ""))


def api_submit(_query, body):
    pid = body.get("id", "")
    meta, path = load_meta(pid)
    if not meta:
        return 404, {"error": "Unknown problem"}
    kind = meta["type"]

    if kind == "mcq":
        chosen = sorted(set(body.get("answer", [])))
        correct = chosen == sorted(meta["answer"])
        entry = record_submission(pid, correct, "Correct" if correct else "Incorrect", {"answer": chosen})
        out = {"kind": "mcq", "correct": correct, "progress": summary(entry)}
        if correct:
            out["notes"] = read_text(os.path.join(path, "solution.md"))
        return out

    if kind == "open":
        text = body.get("text", "")
        if "done" in body:       # one-step flow (older clients): done = mastered
            done = bool(body.get("done"))
            entry = record_submission(pid, done, "Marked as done" if done else "Marked for review",
                                      {"text": text})
        else:                    # submit the answer; the self-review comes next (/api/review)
            if not text.strip():
                return 400, {"error": "Write an answer before submitting it."}
            entry = record_submission(pid, False, "Answer submitted — self-review pending",
                                      {"text": text, "reviewed": False})
        return {"kind": "open", "progress": summary(entry),
                "submission": (entry.get("submissions") or [None])[0]}

    code = body.get("code", "")
    result = judge("submit", meta, path, code)
    accepted = result.get("status") == "accepted"
    if result.get("kind") == "tests":
        detail = "%d / %d tests passed" % (result.get("passed", 0), result.get("total", 0))
        if result.get("load_error"):
            detail = "Error before the tests could run"
    elif accepted:
        detail = "Result matches"
    else:
        detail = result.get("reason") or result.get("error") or "Wrong answer"
    payload = {"code": code}
    if body.get("explanation", "").strip():
        payload["explanation"] = body["explanation"]
    entry = record_submission(pid, accepted, detail, payload)
    result["progress"] = summary(entry)
    return result


def api_review(_query, body):
    """Self-review of a written answer against the rubric. Never graded automatically:
    the learner ticks the key points their answer covered and decides if it is mastered."""
    pid = body.get("id", "")
    meta, _path = load_meta(pid)
    if not meta or meta["type"] != "open":
        return 404, {"error": "Only written answers are self-reviewed"}
    rubric = meta.get("rubric") or []
    covered = sorted({int(i) for i in body.get("rubric", []) if str(i).isdigit() and int(i) < len(rubric)})
    mastered = bool(body.get("mastered"))
    detail = "Self-review: %d / %d key points%s" % (len(covered), len(rubric),
                                                    " · mastered" if mastered else " · review again")
    if not rubric:
        detail = "Self-review: " + ("mastered" if mastered else "review again")

    def apply(entry):
        subs = entry.get("submissions") or []
        if not subs:
            return
        sub = subs[0]
        sub.update({"reviewed": True, "rubric": covered, "accepted": mastered, "detail": detail,
                    "reviewed_at": now()})
        entry["last_at"] = sub["reviewed_at"]
        entry.setdefault("draft", {})["rubric"] = covered
        if mastered:
            entry["status"] = "solved"
            entry.setdefault("solved_at", sub["reviewed_at"])
        elif entry.get("status") != "solved":
            entry["status"] = "attempted"

    entry = update_progress(pid, apply)
    if not entry.get("submissions"):
        return 400, {"error": "Submit an answer first."}
    return {"progress": summary(entry), "submission": entry["submissions"][0]}


def api_reset(_query, body):
    """Forget progress for one problem ({"id": ...}), a list ({"ids": [...]}) or everything ({"all": true})."""
    with _lock:
        data = load_progress()
        if body.get("all"):
            data["problems"] = {}
        elif isinstance(body.get("ids"), list):
            for pid in body["ids"]:
                data["problems"].pop(pid, None)
        else:
            data["problems"].pop(body.get("id", ""), None)
        save_progress(data)
    return {"ok": True}


def api_env(_query, _body):
    if not _env_cache:
        _env_cache.update(environment())
    return _env_cache


GET_ROUTES = {"/api/problems": api_problems, "/api/problem": api_problem,
              "/api/solution": api_solution, "/api/env": api_env}
POST_ROUTES = {"/api/draft": api_draft, "/api/run": api_run, "/api/submit": api_submit,
               "/api/review": api_review, "/api/reset": api_reset}


# ----------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "InterviewPractice/1.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):   # keep the terminal quiet
        pass

    # Only this machine's own browser tab may talk to the judge: it executes code.
    def trusted(self):
        port = self.server.server_address[1]
        hosts = ("127.0.0.1:%d" % port, "localhost:%d" % port)
        if self.headers.get("Host", "") not in hosts:
            return False
        origin = self.headers.get("Origin")
        return origin is None or origin in tuple("http://" + h for h in hosts)

    def send_json(self, payload, status=200):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def dispatch(self, routes, body):
        url = urlparse(self.path)
        handler = routes.get(url.path)
        if handler is None:
            return self.send_json({"error": "Not found"}, 404)
        try:
            result = handler(parse_qs(url.query), body)
        except Exception as exc:   # never take the server down because of one request
            return self.send_json({"error": "%s: %s" % (type(exc).__name__, exc)}, 500)
        if isinstance(result, tuple):
            return self.send_json(result[1], result[0])
        return self.send_json(result)

    def do_GET(self):
        if not self.trusted():
            return self.send_json({"error": "Forbidden"}, 403)
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            return self.dispatch(GET_ROUTES, None)
        self.serve_static(path)

    def do_POST(self):
        if not self.trusted():
            return self.send_json({"error": "Forbidden"}, 403)
        if "application/json" not in self.headers.get("Content-Type", ""):
            return self.send_json({"error": "JSON only"}, 415)
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except ValueError:
            return self.send_json({"error": "Bad JSON"}, 400)
        self.dispatch(POST_ROUTES, body)

    def serve_static(self, path):
        rel = "index.html" if path in ("", "/") else path.lstrip("/")
        full = os.path.normpath(os.path.join(WEB, rel))
        if not full.startswith(WEB + os.sep) or not os.path.isfile(full):
            return self.send_json({"error": "Not found"}, 404)
        with open(full, "rb") as f:
            raw = f.read()
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype.endswith(("javascript", "json")):
            ctype += "; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")     # never run yesterday's interface
        self.end_headers()
        self.wfile.write(raw)


def check():
    problems = list_problems()
    issues = validate()
    by_track = {}
    for p in problems:
        by_track.setdefault(p["track"], []).append(p)
    for t in list_tracks():
        print("%-28s %d problems" % (t["title"], len(by_track.get(t["id"], []))))
    if issues:
        print("\n%d issue(s):" % len(issues))
        for line in issues:
            print("  - " + line)
        return 1
    print("Metadata OK.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Local coding-practice judge")
    parser.add_argument("--port", type=int, default=8790)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--check", action="store_true", help="validate problems and exit")
    parser.add_argument("--data", help="folder holding progress.json (default: ./data) — handy for trying things out")
    args = parser.parse_args()
    if args.check:
        sys.exit(check())
    if args.data:
        global DATA, PROGRESS_FILE
        DATA = os.path.abspath(args.data)
        PROGRESS_FILE = os.path.join(DATA, "progress.json")

    httpd = None
    for port in range(args.port, args.port + 20):
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if httpd is None:
        sys.exit("No free port between %d and %d." % (args.port, args.port + 19))
    httpd.daemon_threads = True

    url = "http://127.0.0.1:%d" % httpd.server_address[1]
    env = environment()
    _env_cache.update(env)
    print("Interview Practice is running at  %s" % url)
    print("Python %s  ·  pandas %s  ·  numpy %s  ·  statsmodels %s" % (
        env["python"], env["pandas"] or "missing", env["numpy"] or "missing",
        env.get("statsmodels") or "missing"))
    missing = [m for m in LIBS if not env.get(m)]
    if missing:
        print("! Some exercises need %s:" % ", ".join(missing))
        print("    %s -m pip install %s" % (sys.executable, " ".join(missing)))
    issues = validate()
    if issues:
        print("! %d problem metadata issue(s) — run  python3 server.py --check  for details." % len(issues))
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
