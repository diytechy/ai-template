## 2026-08-02 — WI-405: the embedded-bar-shape limit, documented and pinned

**Summary.** WI-398 REVIEW-A finding 1: both of `_failure_tail`'s anchors
trust line SHAPE, so bar-shaped text EMBEDDED in a step's own captured output
— a quoted `  FAIL <step>` row, a quoted mock banner, a nested scaffold bar
naming a different step — can silently hijack `_own_step_window` onto a
passing step's text. Per the reviewer's own grading and WI-398's scope guard
(no parsing machinery, no log-management layer), the remedy is the documented
limit, not a fix: a known-limit clause in `_own_step_window`'s docstring
naming the class and pointing at the kept full log
(`out/run-logs/refresh-refused-<branch>.log`) as the refresh path's authority,
with the reviewer's three shapes pinned as fixtures so the choice is explicit,
never folklore.

**Deliverables.**

- **The docstring clause** (`agent_common._own_step_window`): one sentence —
  both anchors trust line shape, embedded bar-shaped text can misanchor the
  window onto a passing step's text, deliberately not parsed away, the kept
  full log is the refresh path's authority.
- **The three pins** (`tests/test_agent_common_harness.py`, WI-405 section):
  the reviewer's shapes rebuilt as fixtures and driven through
  `_failure_tail`, each WATCHED against current behavior first and then pinned
  exactly — a quoted FAIL row in a passing step's output (window = the passing
  quoter's `all good` / `  PASS  tests+coverage` section, zero bytes of the
  real `F401`); a quoted mock banner for the step that later genuinely fails
  (window = the mock banner + the quoting step's `fixture tail`, never the
  `REAL ERROR` line, though the appended anchoring row still names the right
  step); a nested scaffold bar naming a DIFFERENT step inside a red
  tests+coverage (window = the passing format step's
  `146 files already formatted` plus the nested `  FAIL  format` row — the
  truly failing step never named). The section comment states these pin the
  KNOWN LIMIT, not designed behavior: a red here means the anchor changed and
  the docstring clause is stale.

**Deviations and judgments.**

1. **The outermost-banner preference was judged and DECLINED** (the spec's
   conditional half). Identifying the OUTERMOST banner among nested
   line-anchored matches requires knowing which lines sit inside another
   step's section — structural parsing, which the scope guard forbids — and
   the parser-free approximation (first-match → last-match-before-FAIL) merely
   mirrors the hole: it would fix the quoted-mock-banner shape while breaking
   its symmetric twin (a failing step whose banner a LATER passing step
   quotes), which today's first-match handles, and would perturb behavior
   REVIEW-A's "none against" section explicitly defended. Shape 1's hijack
   sits in the FAIL-line anchor itself, out of reach of any banner
   preference. So: CURRENT behavior pinned, per the spec's own fallback.
2. **Registration: no new LLR/TC rows owed** — the WI-398 judgment (REVIEW-A
   "none against" upheld it) extends unchanged: `_failure_tail` /
   `_own_step_window` are private helpers with no LLR row since WI-240, no
   module was added, and the new pins live in the already-cited
   `tests/test_agent_common_harness.py`.
3. **Size ratchet re-stamped** `agent_common.py` 1784 → 1792, eight docstring
   lines, zero code tokens; reason in the baseline comment.
4. Budgeted docs untouched (no byte deltas).

**Watched, measured on the build commit 28860c87 (clean tree):**
`tests/test_agent_common_harness.py` 20 passed in 0.02s
<!-- fig: cmd="python -m pytest -q -p no:xdist tests/test_agent_common_harness.py" rev=28860c87 -->;
smoke tier 621 passed / 6 skipped in 9.92s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=28860c87 -->.
No red-first here by design: the pins assert CURRENT behavior (the scratch
drive watched all three windows before a single assertion was written), so
green-on-first-run is the correct watched outcome for a documented-limit WI.
