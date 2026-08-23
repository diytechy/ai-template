+++
id = "WI-405"
title = "The refusal anchor trusts bar-shaped text embedded in step output (WI-398 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: three constructed shapes — a quoted FAIL row, a quoted mock banner, and a nested scaffold bar naming a different step, each printed INSIDE a step's own captured output — silently hijack _own_step_window onto a passing step's text; realistic here because failing tests print captured stub-bar stdout. THE REMEDY IS SCOPED SMALL, per the reviewer's own words and WI-398's scope guard (no parsing machinery, no log-management layer): a one-clause known-limit in _own_step_window's docstring naming the class and pointing at the kept full log (out/run-logs/refresh-refused-<branch>.log) as the backstop for the refresh path — plus, ONLY if it stays inside the existing shape, preferring the outermost banner when line-anchored matches nest (judge; do not build a parser). Tests: the reviewer's three shapes in docs/reviews/WI-398-REVIEW-A.md finding 1 are the fixture recipes — pin whichever behavior is chosen (documented limit or outermost-banner preference) so the choice is explicit, never folklore. Scope: agent_common.py docstring/one clause + tests; nothing else."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 28860c87. The documented-limit path was taken
and the outermost-banner preference DECLINED, per the spec's own fallback:
identifying the outermost banner among nested line-anchored matches means
knowing which lines sit inside another step's section — structural parsing,
which WI-398's scope guard forbids — and the parser-free approximation
(first-match to last-match-before-FAIL) merely mirrors the hole, breaking the
symmetric shape (a failing step whose banner a LATER passing step quotes)
that first-match handles, while shape 1's hijack sits in the FAIL-line anchor
itself, out of reach of any banner preference. So `_own_step_window`'s
docstring gained the one-clause known limit — both anchors trust line shape;
embedded bar-shaped text (quoted FAIL row, quoted banner, nested scaffold bar
naming another step) can misanchor the window onto a passing step's text; the
kept full log `out/run-logs/refresh-refused-<branch>.log` is the refresh
path's authority — and the reviewer's three shapes are pinned as fixtures in
`tests/test_agent_common_harness.py`, each WATCHED via a scratch drive before
any assertion was written, asserting CURRENT behavior exactly: the quoted
FAIL row yields the passing quoter's section with zero bytes of the real
`F401`; the quoted mock banner yields the quoting step's `fixture tail`
(never `REAL ERROR`, though the appended anchoring row names the right step);
the nested bar naming `format` yields the passing format step's output plus
the nested `  FAIL  format` row, the truly failing step never named. The
section comment states the pins mark the KNOWN LIMIT, not designed behavior.
No new LLR/TC rows (private helpers inside already-cited suites, the WI-398
registration judgment extended); `agent_common.py` ratchet re-stamped
1784 -> 1792 (eight docstring lines, zero code tokens), reason in the
baseline comment.

Watched on 28860c87: harness module 20 passed in 0.02s
<!-- fig: cmd="python -m pytest -q -p no:xdist tests/test_agent_common_harness.py" rev=28860c87 -->;
smoke 621 passed / 6 skipped in 9.92s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=28860c87 -->;
full suite 1880 passed / 10 skipped in 0:04:39
<!-- fig: cmd="python -m pytest -q -n auto" rev=28860c87 -->.
