/* Practice — local judge UI (vanilla JS, no build step) */
(function () {
  "use strict";

  var APP_VERSION = 4;         // must match APP_VERSION in server.py (a stale tab or an old server is detected)
  // where an exercise sits between "know how to code" (level 1) and "know how to work on a desk" (level 2)
  var STAGE = { technical: "Level 1: code it", mixed: "Level 1 → 2: code it, then read it", desk: "Level 2: desk judgement" };
  var app = document.getElementById("app");
  var listCache = null;       // last /api/problems payload
  var envCache = null;
  var view = null;            // state of the open problem page
  var filters = { q: "", track: null, source: "all", type: "all", status: "all" };

  // ------------------------------------------------------------------ helpers
  function h(tag, attrs) {
    var el = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v == null || v === false) return;
        if (k === "class") el.className = v;
        else if (k === "html") el.innerHTML = v;
        else if (k.slice(0, 2) === "on") el.addEventListener(k.slice(2), v);
        else el.setAttribute(k, v === true ? "" : v);
      });
    }
    for (var i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  }
  function append(el, kid) {
    if (kid == null || kid === false) return;
    if (Array.isArray(kid)) kid.forEach(function (k) { append(el, k); });
    else el.appendChild(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

  function get(path) { return fetch(path).then(function (r) { return r.json(); }); }
  function post(path, body) {
    return fetch(path, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body)
    }).then(function (r) { return r.json(); });
  }

  function store(key, value) {
    try {
      if (value === undefined) return window.localStorage.getItem(key);
      window.localStorage.setItem(key, value);
    } catch (e) { /* storage unavailable: preferences just do not persist */ }
    return null;
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }
  function currentTheme() { return document.documentElement.getAttribute("data-theme"); }
  function themeButton() {
    return h("button", {
      class: "btn ghost", title: "Switch light / dark", onclick: function () {
        var next = currentTheme() === "dark" ? "light" : "dark";
        applyTheme(next); store("practice-theme", next);
      }
    }, h("span", { class: "theme-ico" }));
  }

  var MODES = { python: { name: "python", version: 3 }, sql: "text/x-sqlite" };
  function highlight(root) {
    root.querySelectorAll("pre code").forEach(function (el) {
      var m = /language-(\w+)/.exec(el.className || "");
      var mode = m && MODES[m[1]];
      if (!mode) return;
      var text = el.textContent.replace(/\n$/, "");
      CodeMirror.runMode(text, mode, el);
    });
  }
  function md(text) {
    var div = h("div", { class: "prose", html: window.marked.parse(text || "") });
    highlight(div);
    return div;
  }
  function codeBlock(code, lang) {
    var codeEl = h("code", { class: "language-" + lang }, code);
    var pre = h("pre", null, codeEl);
    highlight(pre);
    return pre;
  }
  function inlineMd(text) {
    return h("span", { html: window.marked.parseInline(text || "") });
  }

  function kindOf(p) {
    if (p.type === "mcq") return "qcm";
    if (p.type === "sql") return "sql";
    if (p.type === "open") return "written";
    return p.debug ? "debug" : "code";
  }
  var KIND_LABEL = { qcm: "QCM", sql: "SQL", written: "Written", debug: "Debug", code: "Python" };
  var LEVELS = { 1: "Warm-up", 2: "Foundations", 3: "Intermediate", 4: "Advanced", 5: "Expert" };

  function levelTag(p) {
    if (typeof p.difficulty !== "number") return null;
    return h("span", { class: "tag lvl lvl-" + p.difficulty, title: "Level " + p.difficulty + " — " + LEVELS[p.difficulty] },
      h("i", { class: "pips" }, [1, 2, 3, 4, 5].map(function (i) { return h("b", { class: i <= p.difficulty ? "on" : "" }); })),
      "L" + p.difficulty);
  }
  function sourceTag(p) {
    if (p.track !== "interview") return null;
    var cls = p.set === "glencore" ? " src-g" : (p.set === "millennium" ? " src-m" : "");
    return h("span", { class: "tag src" + cls, title: "Source: " + p.source + (p.number ? " · originally " + p.number : "") },
      p.source, p.number ? h("span", { class: "orig" }, p.number) : null);
  }
  function tagsFor(p, opts) {
    var kind = kindOf(p);
    var out = [];
    if (!(opts && opts.noSource)) out.push(sourceTag(p));
    out.push(h("span", { class: "tag" + (kind === "debug" ? " debug" : "") + (kind === "written" ? " written" : "") }, KIND_LABEL[kind]));
    if (p.explain) out.push(h("span", { class: "tag written", title: "Code + a written explanation" }, "+ Explain"));
    out.push(levelTag(p));
    if (p.time_limit_min) out.push(h("span", { class: "tag" }, p.time_limit_min + " min"));
    return out;
  }
  function shortDate(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    return d.toLocaleDateString(undefined, { day: "numeric", month: "short" });
  }
  function longDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString(undefined, { day: "numeric", month: "short" }) + ", " +
      d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  }
  function clock(s) {
    s = Math.max(0, Math.floor(s));
    var hh = Math.floor(s / 3600), mm = Math.floor((s % 3600) / 60), ss = s % 60;
    return (hh ? hh + ":" + (mm < 10 ? "0" : "") : "") + mm + ":" + (ss < 10 ? "0" : "") + ss;
  }

  function trackList(data) { return (data && data.tracks) || []; }
  function currentTrack(data) {
    var tracks = trackList(data);
    var id = filters.track || store("practice-track") || (tracks[0] && tracks[0].id);
    var t = tracks.filter(function (x) { return x.id === id; })[0] || tracks[0] || { id: "interview", title: "Problems" };
    filters.track = t.id;
    return t;
  }
  function projectOf(data, p) {
    return (data.projects || []).filter(function (c) { return c.id === p.project; })[0] || null;
  }

  // ------------------------------------------------------------------ routing
  var navToken = 0;           // ignore responses that arrive after the user moved on
  function route() {
    leavePage();
    navToken += 1;
    var hash = decodeURIComponent(window.location.hash.replace(/^#\/?/, ""));
    if (hash.indexOf("p/") === 0) openProblem(hash.slice(2));
    else showHome();
  }
  function linkTo(id) { return "#/p/" + id; }

  // ------------------------------------------------------------------ home
  function showHome() {
    var token = navToken;
    Promise.all([get("/api/problems"), envCache || get("/api/env")]).then(function (res) {
      if (token !== navToken) return;
      listCache = res[0]; envCache = res[1];
      document.title = "Practice";
      renderHome();
    }).catch(fail);
  }

  function fail(err) {
    clear(app).appendChild(h("p", { class: "boot" },
      "Could not reach the local server. Is it still running? (" + err + ")"));
  }

  function renderHome() {
    var data = listCache;
    var track = currentTrack(data);
    var problems = data.problems.filter(function (p) { return p.track === track.id; });
    var rank = {};
    problems.forEach(function (p, i) { rank[p.id] = i + 1; });
    var solved = problems.filter(function (p) { return p.progress.status === "solved"; }).length;
    var next = problems.filter(function (p) { return p.progress.status !== "solved"; })[0];

    var top = h("header", { class: "top" },
      h("a", { class: "brand", href: "#/" }, h("i"), "Practice"),
      h("span", { class: "grow" }),
      h("span", { class: "meta" }, track.title + " · ", h("b", null, solved), " / " + problems.length + " solved"),
      next ? h("a", { class: "btn primary", href: linkTo(next.id) }, solved ? "Continue" : "Start", " →") : null,
      themeButton());

    var listBox = h("div");
    var cards = h("div", { class: "cards tracks" });

    trackList(data).forEach(function (t) {
      var mine = data.problems.filter(function (p) { return p.track === t.id; });
      var done = mine.filter(function (p) { return p.progress.status === "solved"; }).length;
      var tried = mine.filter(function (p) { return p.progress.status === "attempted"; }).length;
      cards.appendChild(h("button", {
        class: "card" + (t.id === track.id ? " on" : ""),
        onclick: function () {
          if (t.id === track.id) return;
          filters.track = t.id; filters.source = "all"; filters.type = "all";
          store("practice-track", t.id);
          renderHome();
        }
      },
        h("h3", null, t.title), h("p", null, t.subtitle || ""),
        h("div", { class: "row" },
          h("div", { class: "bar" }, h("i", { style: "width:" + (mine.length ? 100 * done / mine.length : 0) + "%" })),
          h("span", null, h("b", null, done), " / " + mine.length + (tried ? " · " + tried + " in progress" : "")))));
    });

    function seg(key, options) {
      var box = h("div", { class: "seg" });
      options.forEach(function (o) {
        box.appendChild(h("button", {
          class: filters[key] === o[0] ? "on" : "",
          onclick: function () {
            filters[key] = o[0];
            box.querySelectorAll("button").forEach(function (b) { b.className = ""; });
            this.className = "on";
            drawList();
          }
        }, o[1]));
      });
      return box;
    }

    function itemRow(p, label) {
      var pr = p.progress;
      var when = pr.status === "solved" ? "Solved " + shortDate(pr.solved_at)
        : pr.attempts ? pr.attempts + (pr.attempts > 1 ? " attempts" : " attempt") : "";
      return h("a", { class: "item", href: linkTo(p.id) },
        h("span", { class: "dot " + pr.status, title: pr.status }),
        h("span", { class: "num" }, label),
        h("span", { class: "title" }, p.title),
        h("span", { class: "tags" }, tagsFor(p)),
        h("span", { class: "when" }, when));
    }

    function drawList() {
      clear(listBox);
      var q = filters.q.trim().toLowerCase();
      var shown = problems.filter(function (p) {
        if (track.id === "interview" && filters.source !== "all" && p.set !== filters.source) return false;
        if (filters.type !== "all" && kindOf(p) !== filters.type) return false;
        if (filters.status !== "all" && p.progress.status !== filters.status) return false;
        var hay = [p.number, p.title, p.source, (p.concepts || []).join(" ")].join(" ").toLowerCase();
        if (q && hay.indexOf(q) < 0) return false;
        return true;
      });
      if (!shown.length) {
        listBox.appendChild(h("p", { class: "empty" }, "No problem matches these filters."));
        return;
      }
      if (track.ordering === "project") drawProjects(shown);
      else drawLevels(shown);
    }

    function drawLevels(shown) {
      [1, 2, 3, 4, 5].forEach(function (lvl) {
        var mine = shown.filter(function (p) { return p.difficulty === lvl; });
        if (!mine.length) return;
        listBox.appendChild(h("div", { class: "set-title" },
          h("h2", null, "Level " + lvl + " — " + LEVELS[lvl]),
          h("span", null, mine.length + (mine.length > 1 ? " problems" : " problem"))));
        var box = h("div", { class: "list" });
        mine.forEach(function (p) { box.appendChild(itemRow(p, "#" + rank[p.id])); });
        listBox.appendChild(box);
      });
      var other = shown.filter(function (p) { return typeof p.difficulty !== "number"; });
      if (other.length) {
        var box = h("div", { class: "list" });
        other.forEach(function (p) { box.appendChild(itemRow(p, p.number)); });
        listBox.appendChild(box);
      }
    }

    function drawProjects(shown) {
      (data.projects || []).filter(function (c) { return c.track === track.id; }).forEach(function (c) {
        var all = problems.filter(function (p) { return p.project === c.id; });
        var mine = shown.filter(function (p) { return p.project === c.id; });
        if (!mine.length) return;
        var done = all.filter(function (p) { return p.progress.status === "solved"; }).length;
        listBox.appendChild(h("div", { class: "case-head" },
          h("div", { class: "case-top" },
            h("span", { class: "case-num" }, c.number || c.id),
            h("h2", null, c.title),
            h("span", { class: "grow" }),
            h("span", { class: "case-prog" }, h("b", null, done), " / " + all.length)),
          c.question ? h("p", { class: "case-q" }, c.question) : null,
          c.area ? h("p", { class: "case-data" }, h("b", null, "Desk · "), c.area) : null,
          c.commodity ? h("p", { class: "case-data" }, h("b", null, "Market · "), c.commodity) : null,
          c.data_focus ? h("p", { class: "case-data" }, h("b", null, "Data work · "), c.data_focus) : null,
          c.data ? h("p", { class: "case-data" }, h("b", null, "Files · "), c.data) : null,
          c.concepts ? h("div", { class: "chips" }, c.concepts.map(function (x) { return h("span", { class: "chip" }, x); })) : null));
        var box = h("div", { class: "list" });
        mine.forEach(function (p) { box.appendChild(itemRow(p, p.number)); });
        listBox.appendChild(box);
      });
    }

    var search = h("input", {
      class: "search", type: "search", placeholder: track.ordering === "project" ? "Search exercises or concepts…" : "Search problems…",
      value: filters.q, oninput: function () { filters.q = this.value; drawList(); }
    });

    var env = envCache || {};
    var notice = null;
    if (data.app_version !== APP_VERSION) {
      notice = h("div", { class: "notice" },
        h("b", null, "This page and the local server come from different versions of the app. "),
        "Stop the server (Ctrl+C or close its window), start it again with start.command, then reload this page (⌘R).");
    } else if (!(env.pandas && env.numpy)) {
      notice = h("div", { class: "notice" },
        h("b", null, "pandas / numpy are not installed for this Python. "),
        "The Millennium cases and the Quantitative Methods track need them. In a terminal: ",
        h("code", null, (env.executable || "python3") + " -m pip install pandas numpy statsmodels matplotlib"),
        " — then restart the app.");
    } else if (track.id === "quant" && !env.statsmodels) {
      notice = h("div", { class: "notice" },
        h("b", null, "statsmodels is not installed for this Python. "),
        "The Quantitative Methods exercises need it (OLS, ADF, robust standard errors). In a terminal: ",
        h("code", null, (env.executable || "python3") + " -m pip install statsmodels matplotlib"),
        " — then restart the app.");
    } else if (track.id === "quant" && !env.matplotlib) {
      notice = h("div", { class: "notice" },
        h("b", null, "matplotlib is not installed for this Python. "),
        "Every exercise still runs and is judged, but the charts drawn by the Test code pads will not appear. In a terminal: ",
        h("code", null, (env.executable || "python3") + " -m pip install matplotlib"),
        " — then restart the app.");
    }

    var typeOptions = track.id === "interview"
      ? [["all", "All"], ["code", "Python"], ["debug", "Debug"], ["sql", "SQL"], ["written", "Written"]]
      : [["all", "All"], ["code", "Python"], ["written", "Written"]];
    // Source is metadata: an optional, discreet filter — the default view is always the one ranked list.
    var sourceSelect = null;
    if (track.id === "interview") {
      sourceSelect = h("select", {
        class: "select", title: "Optional: show only one source (the ranking stays global)",
        onchange: function () { filters.source = this.value; drawList(); }
      }, h("option", { value: "all" }, "Source: all"));
      (data.sets || []).filter(function (s) { return s.track === "interview"; }).forEach(function (s) {
        sourceSelect.appendChild(h("option", { value: s.id }, "Source: " + s.source));
      });
      sourceSelect.value = filters.source;
    }

    var body = h("main", { class: "home" },
      h("h1", null, "Interview practice"),
      h("p", { class: "lede" }, "Two learning tracks: the questions you met in real screens, and the quantitative methods behind commodity research. Write the answer, run it against the tests, then defend it."),
      notice, cards,
      track.intro ? h("p", { class: "track-intro" }, track.intro) : null,
      h("div", { class: "filters" }, search,
        seg("type", typeOptions),
        seg("status", [["all", "All"], ["todo", "To do"], ["attempted", "In progress"], ["solved", "Solved"]]),
        sourceSelect),
      listBox,
      h("div", { class: "foot" },
        h("span", null, "Python " + (env.python || "?") + (env.pandas ? " · pandas " + env.pandas : "") +
          (env.numpy ? " · numpy " + env.numpy : "") + (env.statsmodels ? " · statsmodels " + env.statsmodels : "") +
          (env.matplotlib ? " · matplotlib " + env.matplotlib : "") +
          " · everything runs on this computer"),
        h("button", {
          class: "btn ghost small", onclick: function () {
            if (!window.confirm("Erase progress, saved code and submissions for the " + problems.length +
              " problems of “" + track.title + "”? The other track is not touched.")) return;
            post("/api/reset", { ids: problems.map(function (p) { return p.id; }) }).then(showHome);
          }
        }, "Reset this track")));

    clear(app); app.appendChild(top); app.appendChild(body);
    drawList();
  }

  // ------------------------------------------------------------------ problem page
  function leavePage() {
    if (!view) return;
    window.clearInterval(view.tick);
    window.clearTimeout(view.saveTimer);
    document.removeEventListener("keydown", view.onKey, true);
    if (view.dirty) saveDraft();
    view = null;
  }

  function openProblem(id) {
    var token = navToken;
    Promise.all([get("/api/problem?id=" + encodeURIComponent(id)), listCache || get("/api/problems")])
      .then(function (res) {
        if (token !== navToken) return;
        var p = res[0]; listCache = res[1];
        if (p.error) {
          clear(app).appendChild(h("p", { class: "boot" }, "Unknown problem. ", h("a", { href: "#/" }, "Back to the list")));
          return;
        }
        renderProblem(p);
      }).catch(fail);
  }

  function renderProblem(p) {
    var mates = listCache.problems.filter(function (x) { return x.track === p.track; });
    var order = mates.map(function (x) { return x.id; });
    var at = order.indexOf(p.id);
    var trackInfo = trackList(listCache).filter(function (t) { return t.id === p.track; })[0] || {};
    var caseInfo = projectOf(listCache, p);
    var caseSteps = caseInfo ? mates.filter(function (x) { return x.project === p.project; }).length : 0;
    document.title = p.number + " · " + p.title + " — Practice";
    if (filters.track !== p.track) { filters.track = p.track; store("practice-track", p.track); }

    var v = view = {
      p: p, leftTab: "desc",
      revealed: p.progress.status === "solved" || (p.type === "open" && (p.submissions || []).length > 0),
      solution: null, submissions: p.submissions || [], elapsed: p.elapsed_s || 0,
      running: p.progress.status !== "solved", dirty: false, busy: false,
      rubric: (p.draft && p.draft.rubric) || [], revealHooks: []
    };
    v.reveal = function () {
      if (v.revealed) return;
      v.revealed = true;
      v.revealHooks.forEach(function (fn) { fn(); });
    };

    // ---- header
    var statusDot = h("span", { class: "dot " + p.progress.status, title: p.progress.status });
    var clockEl = h("button", { class: "btn ghost small clock", title: "Pause / resume the timer" });
    var timerEl = h("span", { class: "timer" }, clockEl,
      h("button", {
        class: "btn ghost small", title: "Reset the timer",
        onclick: function () { v.elapsed = 0; v.running = true; v.dirty = true; drawClock(); }
      }, "↺"));
    clockEl.addEventListener("click", function () { v.running = !v.running; drawClock(); });
    function drawClock() {
      clockEl.textContent = clock(v.elapsed) + (p.time_limit_min ? " / " + p.time_limit_min + ":00" : "");
      timerEl.className = "timer" + (v.running ? "" : " paused") +
        (p.time_limit_min && v.elapsed > p.time_limit_min * 60 ? " over" : "");
    }
    drawClock();
    v.tick = window.setInterval(function () {
      if (!v.running || document.hidden) return;
      v.elapsed += 1; drawClock();
      if (v.elapsed % 20 === 0) saveDraft();
    }, 1000);

    function setStatus(progress) {
      p.progress = progress;
      statusDot.className = "dot " + progress.status;
      statusDot.title = progress.status;
      listCache = null;                         // the list must be re-read next time
      get("/api/problems").then(function (d) { listCache = d; });
    }

    var head = h("header", { class: "phead" },
      h("a", { class: "btn ghost", href: "#/", title: "All problems" }, "← " + (trackInfo.title || "Problems")),
      statusDot,
      h("span", { class: "crumb" }, p.track === "interview" ? "#" + (at + 1) : p.number),
      h("h1", null, p.title),
      tagsFor(p),
      h("span", { class: "grow" }),
      (p.type === "code" || p.type === "sql") ? timerEl : null,
      h("a", { class: "btn ghost", title: "Previous problem", href: at > 0 ? linkTo(order[at - 1]) : null, style: at > 0 ? null : "visibility:hidden" }, "‹"),
      h("a", { class: "btn ghost", title: "Next problem", href: at < order.length - 1 ? linkTo(order[at + 1]) : null, style: at < order.length - 1 ? null : "visibility:hidden" }, "›"),
      themeButton());

    // ---- left pane: description / solution / submissions
    var leftBody = h("div", { class: "scroll" });
    var leftTabs = h("div", { class: "tabs" });
    function drawLeftTabs() {
      clear(leftTabs);
      [["desc", "Description"], ["solution", "Solution"], ["subs", "Submissions"]].forEach(function (t) {
        leftTabs.appendChild(h("button", {
          class: "tab" + (v.leftTab === t[0] ? " on" : ""),
          onclick: function () { v.leftTab = t[0]; drawLeft(); }
        }, t[1], t[0] === "subs" && v.submissions.length ? h("span", { class: "count" }, v.submissions.length) : null));
      });
    }
    function kicker() {
      if (p.track === "interview") {
        return h("div", null,
          h("div", { class: "kicker" },
            sourceTag(p),
            h("span", { class: "src" }, "#" + (at + 1) + " of " + order.length + " in the global ranking")),
          p.difficulty_why ? h("p", { class: "why-level" },
            h("b", null, "Level " + p.difficulty + " — " + LEVELS[p.difficulty] + ". "), p.difficulty_why) : null);
      }
      if (caseInfo) {
        return h("div", { class: "case-banner" },
          h("div", { class: "cb-top" },
            h("span", { class: "case-num" }, caseInfo.number), h("b", null, caseInfo.title),
            h("span", { class: "cb-step" }, "Step " + p.step + " of " + caseSteps +
              (STAGE[p.level] ? " · " + STAGE[p.level] : ""))),
          caseInfo.question ? h("p", null, caseInfo.question) : null);
      }
      return null;
    }
    function drawLeft() {
      drawLeftTabs();
      clear(leftBody);
      var pad = h("div", { class: "pad" });
      leftBody.appendChild(pad);
      leftBody.scrollTop = 0;
      if (v.leftTab === "desc") {
        pad.appendChild(kicker());
        pad.appendChild(md(p.statement));
      } else if (v.leftTab === "solution") {
        drawSolution(pad);
      } else {
        drawSubmissions(pad);
      }
    }
    v.drawLeft = drawLeft;

    function loadSolution(then) {
      if (v.solution) { then(v.solution); return; }
      get("/api/solution?id=" + encodeURIComponent(p.id)).then(function (s) { v.solution = s; then(s); });
    }
    v.loadSolution = loadSolution;

    function drawSolution(pad) {
      if (!v.revealed) {
        var what = p.type === "open" ? "Submit your answer to see the reference answer and the key points of a strong answer."
          : "The solution is hidden until you solve the problem.";
        pad.appendChild(h("div", { class: "locked" },
          h("p", null, what),
          h("button", { class: "btn", onclick: function () { v.reveal(); drawLeft(); } }, "Show it anyway")));
        return;
      }
      if (!v.solution) {
        pad.appendChild(h("p", { class: "placeholder" }, "Loading…"));
        loadSolution(function () { if (view === v && v.leftTab === "solution") drawLeft(); });
        return;
      }
      var s = v.solution, notes = s.notes || "";
      if (s.code) {
        var fence = "```" + s.language + "\n" + s.code.replace(/\n+$/, "") + "\n```";
        notes = notes.indexOf("{{code}}") >= 0 ? notes.replace("{{code}}", fence)
          : "### Solution\n\n" + fence + "\n\n" + notes;
        pad.appendChild(h("div", { class: "kicker" },
          h("button", {
            class: "btn small", onclick: function () {
              var btn = this;
              navigator.clipboard.writeText(s.code).then(function () {
                btn.textContent = "Copied"; window.setTimeout(function () { btn.textContent = "Copy the code"; }, 1200);
              });
            }
          }, "Copy the code")));
      }
      pad.appendChild(md(notes));
      if (s.rubric && s.rubric.length) {
        pad.appendChild(h("div", { class: "prose rubric-ref" },
          h("h3", null, p.type === "open" ? "Key points of a strong answer" : "Key points of a strong explanation"),
          h("ol", null, s.rubric.map(function (r) { return h("li", null, inlineMd(r)); }))));
      }
    }

    function drawSubmissions(pad) {
      if (!v.submissions.length) {
        pad.appendChild(h("p", { class: "placeholder" }, "No submission yet."));
        return;
      }
      v.submissions.forEach(function (s) {
        var extra = h("div");
        var label = s.accepted ? (p.type === "open" ? "Mastered" : "Accepted")
          : (p.type === "open" ? (s.reviewed ? "Review again" : "Submitted") : "Not accepted");
        var row = h("div", { class: "sub" },
          h("div", { class: "line" },
            h("b", { class: s.accepted ? "ok" : (p.type === "open" ? "pending" : "ko") }, label),
            h("span", null, s.detail || ""),
            h("span", { class: "grow" }),
            h("span", { class: "at" }, longDate(s.at)),
            s.code != null ? h("button", {
              class: "btn small", onclick: function () {
                if (extra.firstChild) { clear(extra); return; }
                extra.appendChild(codeBlock(s.code, p.type === "sql" ? "sql" : "python"));
                extra.appendChild(h("button", {
                  class: "btn small", onclick: function () {
                    if (v.editor) { v.editor.setValue(s.code); v.editor.focus(); }
                  }
                }, "Load into the editor"));
              }
            }, "Code") : null),
          s.answer ? h("div", { class: "at" }, "Answer: " + (s.answer.join(", ") || "—")) : null,
          s.text ? h("div", { class: "sub-text" }, s.text) : null,
          s.explanation ? h("div", { class: "sub-text" }, h("b", null, "Explanation: "), s.explanation) : null,
          extra);
        pad.appendChild(h("div", { class: "prose" }, row));
      });
    }

    // ---- drafts
    var savedEl = h("span", { class: "saved" });
    function touch() {
      v.dirty = true;
      savedEl.textContent = "";
      window.clearTimeout(v.saveTimer);
      v.saveTimer = window.setTimeout(saveDraft, 700);
    }
    v.touch = touch;
    v.savedEl = savedEl;

    // ---- right pane
    var right = h("section", { class: "pane" });
    if (p.type === "mcq") buildMcq(right, v, setStatus, drawLeft);
    else if (p.type === "open") buildOpen(right, v, setStatus, drawLeft);
    else buildCode(right, v, setStatus, drawLeft);

    // ---- layout
    var split = h("div", { class: "split" });
    var gutter = h("div", { class: "gutter", title: "Drag to resize" });
    split.appendChild(h("section", { class: "pane" }, leftTabs, leftBody));
    split.appendChild(gutter);
    split.appendChild(right);
    var saved = store("practice-left");
    if (saved) split.style.setProperty("--left", saved);
    drag(gutter, function (e) {
      var r = split.getBoundingClientRect();
      var px = Math.min(Math.max(e.clientX - r.left, 280), r.width - 360);
      split.style.setProperty("--left", px + "px");
      store("practice-left", px + "px");
      if (v.editor) v.editor.refresh();
    });

    clear(app).appendChild(h("div", { class: "page" }, head, split));
    drawLeft();
    if (v.editor) { v.editor.refresh(); v.editor.focus(); }
    if (v.scratch) v.scratch.refresh();

    v.onKey = function (e) {
      if (!(e.metaKey || e.ctrlKey) || e.key !== "Enter") return;
      e.preventDefault(); e.stopPropagation();
      if (e.shiftKey || !v.run) { if (v.submit) v.submit(); }
      else v.run();
    };
    document.addEventListener("keydown", v.onKey, true);
  }

  function drag(handle, onMove) {
    handle.addEventListener("pointerdown", function (e) {
      e.preventDefault();
      handle.classList.add("drag");
      handle.setPointerCapture(e.pointerId);
      function move(ev) { onMove(ev); }
      function up() {
        handle.classList.remove("drag");
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", up);
      }
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", up);
    });
  }

  function saveDraft() {
    var v = view;
    if (!v) return Promise.resolve();
    var p = v.p, body = { id: p.id, elapsed_s: v.elapsed };
    if (v.editor) {
      body.code = v.editor.getValue();
      body.touched = body.code.trim() !== (p.starter || "").trim();
    }
    if (v.scratch) body.scratch = v.scratch.getValue();
    if (v.getAnswer) { body.answer = v.getAnswer(); body.touched = body.answer.length > 0; }
    if (v.getText) { body.text = v.getText(); body.touched = body.text.trim().length > 0; }
    if (v.getExplanation) { body.explanation = v.getExplanation(); if (body.explanation.trim()) body.touched = true; }
    if (v.rubricTouched) body.rubric = v.rubric;
    v.dirty = false;
    return post("/api/draft", body).then(function () {
      if (view === v && v.savedEl) v.savedEl.textContent = "Saved";
    }).catch(function () { /* the next edit retries */ });
  }

  // ------------------------------------------------------------------ rubric checklist (self-review, never auto-graded)
  function rubricChecklist(v, items, onChange) {
    var box = h("div", { class: "rubric" });
    items.forEach(function (text, i) {
      var input = h("input", { type: "checkbox" });
      input.checked = v.rubric.indexOf(i) >= 0;
      input.addEventListener("change", function () {
        var set = v.rubric.filter(function (x) { return x !== i; });
        if (input.checked) set.push(i);
        v.rubric = set.sort(function (a, b) { return a - b; });
        v.rubricTouched = true;
        label.classList.toggle("on", input.checked);
        if (onChange) onChange();
      });
      var label = h("label", { class: "opt" + (input.checked ? " on" : "") }, input,
        h("span", { class: "key" }, String(i + 1)), h("div", { class: "txt" }, h("p", null, inlineMd(text))));
      box.appendChild(label);
    });
    return box;
  }

  // ------------------------------------------------------------------ code / sql
  function makeEditor(parent, value, mode, extra) {
    var options = {
      value: value, mode: mode, lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
      matchBrackets: true, autoCloseBrackets: true, styleActiveLine: true,
      extraKeys: {
        Tab: function (cm) {
          if (cm.somethingSelected()) cm.indentSelection("add");
          else cm.replaceSelection("    ", "end");
        },
        "Shift-Tab": function (cm) { cm.indentSelection("subtract"); },
        "Cmd-/": "toggleComment", "Ctrl-/": "toggleComment"
      }
    };
    Object.keys(extra || {}).forEach(function (k) { options[k] = extra[k]; });
    return CodeMirror(parent, options);
  }

  function buildCode(right, v, setStatus, drawLeft) {
    var p = v.p, isSql = p.type === "sql";
    var mac = /Mac/.test(navigator.platform || "");
    var mod = mac ? "⌘" : "Ctrl+";

    var runBtn = h("button", { class: "btn", title: "Run your code" + (isSql ? "" : " and the test code") },
      "Run ", h("kbd", null, mod + "↵"));
    var submitBtn = h("button", { class: "btn primary", title: "Run every test case" },
      "Submit ", h("kbd", null, mod + "⇧↵"));
    var resetBtn = h("button", { class: "btn ghost small", title: "Put the original code back" }, "Reset code");

    var editorBox = h("div", { class: "editor" });
    var draftCode = (v.p.draft && v.p.draft.code != null) ? v.p.draft.code : p.starter;
    v.editor = makeEditor(editorBox, draftCode, isSql ? MODES.sql : MODES.python);
    v.editor.on("change", v.touch);

    // dock
    var panes = {};
    var dockTabs = h("div", { class: "tabs" });
    var dockBody = h("div", { class: "body" });
    var names = isSql ? [["output", "Query result"], ["result", "Verdict"]]
      : [["tests", "Test code"], ["output", "Output"], ["result", "Tests"]];
    if (p.explain) names.push(["explain", "Explain"]);
    var dockTab = names[0][0];
    names.forEach(function (n) {
      panes[n[0]] = h("div", { hidden: n[0] !== dockTab });
      dockBody.appendChild(panes[n[0]]);
    });
    function drawDockTabs() {
      clear(dockTabs);
      names.forEach(function (n) {
        dockTabs.appendChild(h("button", {
          class: "tab" + (dockTab === n[0] ? " on" : "") + (n[0] === "explain" ? " explain-tab" : ""),
          onclick: function () { showDock(n[0]); }
        }, n[1]));
      });
      dockTabs.appendChild(h("span", { class: "grow" }));
      if (dockTab === "tests") dockTabs.appendChild(h("span", { class: "hint" }, "runs after your code when you press Run"));
      if (dockTab === "explain") dockTabs.appendChild(h("span", { class: "hint" }, "saved as you type"));
    }
    function showDock(name) {
      dockTab = name;
      names.forEach(function (n) { panes[n[0]].hidden = n[0] !== name; });
      drawDockTabs();
      if (name === "tests" && v.scratch) v.scratch.refresh();
    }

    if (!isSql) {
      panes.tests.style.cssText = "position:absolute;inset:0";
      var scratchText = (p.draft && p.draft.scratch != null) ? p.draft.scratch : (p.test_code || "");
      v.scratch = makeEditor(panes.tests, scratchText, MODES.python, { lineNumbers: false, styleActiveLine: false });
      v.scratch.on("change", v.touch);
    }
    panes.output.appendChild(h("p", { class: "placeholder" }, isSql
      ? "Press Run to execute your query on the local employees table."
      : "Press Run to execute your code, followed by the test code."));
    panes.result.appendChild(h("p", { class: "placeholder" }, "Press Submit to check your answer against the test cases."));

    if (p.explain) buildExplain(panes.explain, v);

    function busy(on, label) {
      v.busy = on;
      runBtn.disabled = submitBtn.disabled = on;
      if (on) {
        var target = panes[label === "run" ? "output" : "result"];
        clear(target).appendChild(h("p", { class: "placeholder" }, label === "run" ? "Running…" : "Running the tests…"));
        showDock(label === "run" ? "output" : "result");
      }
    }

    v.run = function () {
      if (v.busy) return;
      busy(true, "run");
      saveDraft();
      post("/api/run", { id: p.id, code: v.editor.getValue(), scratch: v.scratch ? v.scratch.getValue() : "" })
        .then(function (r) { if (view === v) { busy(false); drawOutput(panes.output, r); } })
        .catch(function (e) { if (view === v) { busy(false); drawCrash(panes.output, String(e)); } });
    };
    v.submit = function () {
      if (v.busy) return;
      busy(true, "submit");
      saveDraft();
      var code = v.editor.getValue();
      var explanation = v.getExplanation ? v.getExplanation() : "";
      post("/api/submit", { id: p.id, code: code, explanation: explanation })
        .then(function (r) {
          if (view !== v) return;
          busy(false);
          drawResult(panes.result, r);
          if (r.progress) {
            setStatus(r.progress);
            var accepted = r.status === "accepted";
            v.submissions.unshift({
              at: r.progress.last_at, accepted: accepted, code: code, explanation: explanation || undefined,
              detail: r.kind === "tests" && !r.load_error ? r.passed + " / " + r.total + " tests passed"
                : (accepted ? "Result matches" : (r.reason || "Error"))
            });
            if (accepted) { v.running = false; v.reveal(); }
            drawLeft();
          }
        })
        .catch(function (e) { if (view === v) { busy(false); drawCrash(panes.result, String(e)); } });
    };
    runBtn.addEventListener("click", v.run);
    submitBtn.addEventListener("click", v.submit);
    resetBtn.addEventListener("click", function () {
      if (!window.confirm("Replace your code with the original starter code?")) return;
      v.editor.setValue(p.starter || "");
      if (v.scratch) v.scratch.setValue(p.test_code || "");
      v.editor.focus();
    });

    var dock = h("div", { class: "dock" }, dockTabs, dockBody);
    var savedDock = store("practice-dock");
    if (savedDock) dock.style.setProperty("--dock", savedDock);
    var gutter = h("div", { class: "gutter h", title: "Drag to resize" });
    var work = h("div", { class: "work" },
      h("div", { class: "editor-bar" },
        h("span", { class: "lang" }, isSql ? "SQL (SQLite)" : "Python 3"),
        v.savedEl, h("span", { class: "grow" }), resetBtn, runBtn, submitBtn),
      editorBox, gutter, dock);
    drag(gutter, function (e) {
      var r = work.getBoundingClientRect();
      var px = Math.min(Math.max(r.bottom - e.clientY, 90), r.height - 160);
      dock.style.setProperty("--dock", px + "px");
      store("practice-dock", px + "px");
      v.editor.refresh();
    });
    right.appendChild(work);
    drawDockTabs();
  }

  // The "Explain" tab of a code exercise: a written interpretation next to the code.
  function buildExplain(pane, v) {
    var p = v.p;
    pane.style.cssText = "position:absolute;inset:0;overflow:auto";
    var area = h("textarea", { class: "explain-area", placeholder: "Your interpretation, in a few sentences, as you would say it in an interview…" });
    area.value = (p.draft && p.draft.explanation) || "";
    area.addEventListener("input", v.touch);
    v.getExplanation = function () { return area.value; };
    var review = h("div");
    function drawReview() {
      clear(review);
      if (!v.revealed) {
        review.appendChild(h("p", { class: "placeholder small" },
          "Once the tests pass (or you reveal the solution), the key points of a strong explanation appear here so you can check your answer against them."));
        return;
      }
      v.loadSolution(function (s) {
        if (view !== v) return;
        clear(review);
        if (!s.rubric || !s.rubric.length) return;
        review.appendChild(h("h2", null, "Self-check — tick what your explanation covers"));
        review.appendChild(rubricChecklist(v, s.rubric, function () {
          count.textContent = v.rubric.length + " / " + s.rubric.length + " key points covered";
          v.touch();
        }));
        var count = h("p", { class: "rubric-count" }, v.rubric.length + " / " + s.rubric.length + " key points covered");
        review.appendChild(count);
      });
    }
    v.revealHooks.push(drawReview);
    pane.appendChild(h("div", { class: "pad" }, h("div", { class: "answer" },
      h("div", { class: "explain-prompt" }, md(p.explain.prompt)),
      area, review)));
    drawReview();
  }

  function drawCrash(box, message) {
    clear(box);
    box.appendChild(h("div", { class: "verdict ko" }, h("strong", null, "Error")));
    box.appendChild(h("pre", { class: "console err" }, message));
  }

  function table(columns, rows) {
    var t = h("table", { class: "result" });
    t.appendChild(h("tr", null, columns.map(function (c) { return h("th", null, c); })));
    rows.forEach(function (r) { t.appendChild(h("tr", null, r.map(function (c) { return h("td", null, c); }))); });
    return h("div", { class: "tablewrap" }, t);
  }

  function drawOutput(box, r) {
    clear(box);
    if (r.kind === "console") {
      box.appendChild(r.output ? h("pre", { class: "console" + (r.exit_code ? " err" : "") }, r.output)
        : (r.figures && r.figures.length ? h("span")
          : h("p", { class: "placeholder" }, "No output. Print something from the test code to see it here.")));
      (r.figures || []).forEach(function (png, i) {
        box.appendChild(h("figure", { class: "chart" },
          h("img", { src: "data:image/png;base64," + png, alt: "Chart " + (i + 1) + " drawn by your test code" })));
      });
      if (r.figures_not_shown) box.appendChild(h("p", { class: "placeholder" },
        r.figures_not_shown + " more chart(s) not shown — at most 6 per run."));
      box.appendChild(h("div", { class: "status-line" }, r.timed_out ? "Stopped: time limit exceeded."
        : (r.exit_code ? "Finished with an error" : "Finished") + " in " + r.elapsed_ms + " ms"));
    } else if (r.kind === "sql" && r.status !== "error") {
      box.appendChild(h("div", { class: "status-line", style: "border-top:0;border-bottom:1px solid var(--line)" },
        r.row_count + (r.row_count === 1 ? " row" : " rows") + " · " + r.elapsed_ms + " ms"));
      box.appendChild(h("div", { style: "padding:12px 16px" }, table(r.columns, r.rows)));
    } else {
      drawCrash(box, r.error || r.output || "Something went wrong.");
    }
  }

  var ORIGIN = {
    source: ["Book", "Input and expected output come from your documents"],
    rebuilt: ["Rebuilt", "Named or partly shown in your documents — the missing values were reconstructed"],
    extra: ["Added", "Extra case, checked against the reference solution"]
  };

  function drawResult(box, r) {
    clear(box);
    if (r.kind === "crash") { drawCrash(box, r.error + (r.output ? "\n\n" + r.output : "")); return; }
    var ok = r.status === "accepted";

    if (r.kind === "sql") {
      box.appendChild(h("div", { class: "verdict " + (ok ? "ok" : "ko") },
        h("strong", null, ok ? "Accepted" : (r.error ? "Error" : "Wrong answer")),
        h("span", null, ok ? "Your result matches the expected rows, columns and order." : (r.error || r.reason))));
      if (r.columns && r.columns.length) {
        box.appendChild(h("div", { class: "grid2" },
          h("div", null, h("h4", null, "Your result · " + r.row_count + " rows"), table(r.columns, r.rows)),
          h("div", null, h("h4", null, "Expected · " + r.expected_row_count + " rows"), table(r.expected_columns, r.expected_rows))));
      }
      return;
    }

    if (r.load_error) {
      box.appendChild(h("div", { class: "verdict ko" }, h("strong", null, "Error"),
        h("span", null, "Your code could not be loaded, so no test ran.")));
      box.appendChild(h("pre", { class: "console err" }, r.load_error));
      if (r.load_output) box.appendChild(h("pre", { class: "console" }, r.load_output));
      return;
    }

    box.appendChild(h("div", { class: "verdict " + (ok ? "ok" : "ko") },
      h("strong", null, ok ? "Accepted" : "Wrong answer"),
      h("span", null, r.passed + " / " + r.total + " tests passed · " + r.elapsed_ms + " ms")));

    var opened = false;
    r.tests.forEach(function (t) {
      var d = h("details", { class: "test " + (t.passed ? "pass" : "fail") });
      if (!t.passed && !opened) { d.open = true; opened = true; }
      var o = ORIGIN[t.origin] || ORIGIN.extra;
      d.appendChild(h("summary", null,
        h("span", { class: "mark" }, t.passed ? "✓" : "✗"),
        h("span", { class: "name" }, t.name),
        h("span", { class: "origin " + t.origin, title: o[1] }, o[0]),
        h("span", { class: "ms" }, t.time_ms + " ms")));
      var io = h("dl", { class: "io" });
      function line(label, text, bad) {
        io.appendChild(h("dt", null, label));
        io.appendChild(h("dd", null, h("pre", { class: bad ? "bad" : "" }, text)));
      }
      if (t.input.length) {
        var multiline = t.input.some(function (a) { return a.value.indexOf("\n") >= 0; });
        line("Input", t.input.map(function (a) {
          return a.name + " =" + (a.value.indexOf("\n") >= 0 ? "\n" : " ") + a.value;
        }).join(multiline ? "\n\n" : "\n"));
      }
      if (t.expected) line("Expected", t.expected);
      if (t.actual) line("Your output", t.actual, !t.passed);
      if (t.error) line("Error", t.error, true);
      if (t.stdout) line("Printed", t.stdout);
      d.appendChild(h("div", { class: "detail" },
        t.note ? h("p", { class: "note" }, t.note) : null,
        t.reason ? h("p", { class: "why" }, t.reason) : null,
        io));
      box.appendChild(d);
    });
    if (r.load_output) box.appendChild(h("pre", { class: "console" }, r.load_output));
  }

  // ------------------------------------------------------------------ QCM (kept for archived material)
  function buildMcq(right, v, setStatus, drawLeft) {
    var p = v.p;
    var chosen = (p.draft && p.draft.answer) || [];
    var feedback = h("div");
    var list = h("div");
    var lang = p.option_language || "python";

    p.options.forEach(function (o) {
      var input = h("input", { type: p.multi ? "checkbox" : "radio", name: "opt", value: o.key });
      input.checked = chosen.indexOf(o.key) >= 0;
      var txt = h("div", { class: "txt" });
      if (o.code) {
        var code = h("code", { class: "language-" + lang }, o.code);
        var pre = h("pre", null, code);
        highlight(pre);
        txt.appendChild(pre);
      }
      if (o.text) txt.appendChild(h("p", null, inlineMd(o.text)));
      var label = h("label", { class: "opt" + (input.checked ? " on" : "") }, input, h("span", { class: "key" }, o.key), txt);
      input.addEventListener("change", function () {
        list.querySelectorAll(".opt").forEach(function (el) {
          el.classList.toggle("on", el.querySelector("input").checked);
        });
        clear(feedback);
        v.touch();
      });
      list.appendChild(label);
    });

    v.getAnswer = function () {
      return Array.prototype.map.call(list.querySelectorAll("input:checked"), function (i) { return i.value; });
    };
    v.submit = function () {
      var answer = v.getAnswer();
      if (!answer.length) {
        clear(feedback).appendChild(h("div", { class: "feedback ko" }, "Pick an answer first."));
        return;
      }
      post("/api/submit", { id: p.id, answer: answer }).then(function (r) {
        if (view !== v) return;
        setStatus(r.progress);
        v.submissions.unshift({ at: r.progress.last_at, accepted: r.correct, detail: r.correct ? "Correct" : "Incorrect", answer: answer });
        clear(feedback);
        if (r.correct) {
          v.reveal();
          feedback.appendChild(h("div", { class: "feedback ok" }, "Correct."));
          feedback.appendChild(h("div", { style: "margin-top:16px" }, md(r.notes)));
        } else {
          feedback.appendChild(h("div", { class: "feedback ko" },
            p.multi ? "Not quite — the set of ticked answers must match exactly. Try again." : "Not quite. Try again."));
        }
        drawLeft();
      });
    };

    right.appendChild(h("div", { class: "scroll" }, h("div", { class: "pad" }, h("div", { class: "answer" },
      h("h2", null, p.instruction || (p.multi ? "Select all answers that apply" : "One answer")),
      list,
      h("div", { class: "actions" },
        h("button", { class: "btn primary", onclick: function () { v.submit(); } }, "Submit")),
      feedback))));
  }

  // ------------------------------------------------------------------ written answer
  // 1. write (autosaved)  2. submit  3. read the reference answer  4. tick the rubric  5. mastered / review again
  function buildOpen(right, v, setStatus, drawLeft) {
    var p = v.p;
    var area = h("textarea", { placeholder: "Write your answer here, as you would in the interview…" });
    area.value = (p.draft && p.draft.text) || "";
    area.addEventListener("input", function () { v.touch(); clear(feedback); });
    v.getText = function () { return area.value; };
    var feedback = h("div");
    var reviewBox = h("div", { class: "review" });
    var latest = function () { return v.submissions[0] || null; };

    function showFeedback(kind, text) {
      clear(feedback).appendChild(h("div", { class: "feedback " + kind }, text));
    }

    function submitAnswer() {
      if (!area.value.trim()) { showFeedback("ko", "Write an answer before submitting it."); return; }
      saveDraft();
      post("/api/submit", { id: p.id, text: area.value }).then(function (r) {
        if (view !== v) return;
        if (r.error) { showFeedback("ko", r.error); return; }
        setStatus(r.progress);
        v.submissions.unshift(r.submission);
        v.reveal(); v.leftTab = "solution";
        drawLeft(); drawReview();
        showFeedback("ok", "Answer submitted. Read the reference answer on the left, then review yours below.");
      });
    }
    v.submit = submitAnswer;

    function sendReview(mastered) {
      var sub = latest();
      if (!sub) { showFeedback("ko", "Submit your answer first."); return; }
      post("/api/review", { id: p.id, rubric: v.rubric, mastered: mastered }).then(function (r) {
        if (view !== v) return;
        if (r.error) { showFeedback("ko", r.error); return; }
        setStatus(r.progress);
        v.submissions[0] = r.submission;
        drawLeft(); drawReview();
        showFeedback(mastered ? "ok" : "ko", mastered ? "Marked as mastered." : "Kept in your review list.");
      });
    }

    function drawReview() {
      clear(reviewBox);
      if (!v.revealed) return;
      v.loadSolution(function (s) {
        if (view !== v) return;
        clear(reviewBox);
        var items = s.rubric || [];
        var sub = latest();
        reviewBox.appendChild(h("h2", null, "Self-review"));
        reviewBox.appendChild(h("p", { class: "hint-text" }, sub
          ? "Compare your submitted answer with the reference answer (Solution tab) and tick the key points it actually covers. Nothing is graded automatically — you decide whether it is interview-ready."
          : "You revealed the reference answer without submitting. Write and submit your own answer to record a self-review."));
        if (items.length) {
          var count = h("p", { class: "rubric-count" });
          var setCount = function () { count.textContent = v.rubric.length + " / " + items.length + " key points covered"; };
          reviewBox.appendChild(rubricChecklist(v, items, function () { setCount(); v.touch(); }));
          setCount();
          reviewBox.appendChild(count);
        }
        reviewBox.appendChild(h("div", { class: "actions" },
          h("button", { class: "btn primary", disabled: !sub, onclick: function () { sendReview(true); } }, "Mark as mastered"),
          h("button", { class: "btn", disabled: !sub, onclick: function () { sendReview(false); } }, "Review again later"),
          sub && sub.reviewed ? h("span", { class: "saved" }, "Last review: " + (sub.detail || "")) : null));
      });
    }
    v.revealHooks.push(drawReview);

    var previous = null;
    if (p.follows) {
      previous = h("div", { class: "readonly-code" },
        h("div", { class: "label" }, "Your submitted query (read-only)"),
        p.follows_code ? h("div", { class: "prose" }, codeBlock(p.follows_code, "sql"))
          : h("div", { class: "label" }, "Nothing yet — solve the previous question first to see your query here."));
    }

    right.appendChild(h("div", { class: "scroll" }, h("div", { class: "pad" }, h("div", { class: "answer" },
      previous,
      h("h2", null, "Your answer"),
      area,
      h("div", { class: "actions" },
        h("button", { class: "btn primary", onclick: submitAnswer }, "Submit answer"),
        h("button", {
          class: "btn ghost", onclick: function () { v.reveal(); v.leftTab = "solution"; drawLeft(); }
        }, "Show the reference answer"),
        v.savedEl),
      feedback,
      reviewBox))));
    drawReview();
  }

  // ------------------------------------------------------------------ start
  var theme = store("practice-theme");
  if (!theme) theme = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  applyTheme(theme);
  window.addEventListener("hashchange", route);
  window.addEventListener("beforeunload", function () { if (view && view.dirty) saveDraft(); });
  route();
})();
