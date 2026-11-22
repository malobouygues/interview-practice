# Archived — Glencore multiple-choice questions

These nine questions (Q1–Q7, Q14, Q15 of the Glencore CoderPad book) were removed from
the active application when Glencore and Millennium were merged into the single
**Past Interview Questions** bank. They are kept here unchanged — statement, options,
answer key and corrigé — so nothing from the original book is lost.

The server only loads problems from `problems/`, so nothing in this folder appears in
the app. Your progress file is untouched: any attempt you made on these questions is
still recorded in `data/progress.json` under its original id (for example
`glencore/q01-type-of-a-literal`).

To bring one back, move its folder to `problems/glencore/`, change `"type"` in its
`meta.json` only if you want it as something other than a multiple-choice question,
and add `"difficulty"` (1–5) and `"sequence"` like the other problems
(`python3 server.py --check` reports anything missing). Note that the checker refuses
multiple-choice questions in the interview track by design.

| Folder | Question |
|---|---|
| q01-type-of-a-literal | Q1 — Type of a literal |
| q02-iterate-over-a-list | Q2 — Iterate over a list |
| q03-colors-and-numbers | Q3 — Colors and numbers |
| q04-args-and-kwargs | Q4 — `*args` and `**kwargs` |
| q05-creating-an-exception | Q5 — Creating an exception |
| q06-key-parameter-of-min-max | Q6 — The key parameter of min / max |
| q07-execution-order-with-main | Q7 — Execution order with `__main__` |
| q14-clause-order | Q14 — Clause order (SQL) |
| q15-what-can-be-said-about-this-join | Q15 — What can be said about this JOIN? (SQL) |

The original Word documents are in `sources/`.
