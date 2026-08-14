# WI-398 — REVIEW-A (2026-08-01)

Verdict: APPROVE

Reviewed independently against the spec
(`docs/work/complete/WI-398-a-red-bars-refusal-carries-its-own-error.md`) and
drain-plan row 7 (`docs/archive/history/backlog-plan-2026-08-01.md`: "One anchor fix + keep the
bar log a refusal points at; no log-management layer"). Diff = two commits
(`b121aba8` build, `e49fcbd8` close) on
`wi-398-a-red-bars-refusal-carries-its-own-error` vs `ConcurrencyTrainRewrite`.
`docs/log.d/` was not read. I did not trust the shipped fixtures: I constructed
my own hostile bar outputs from `check.py`'s real printing shapes
(`run_step`/`run_lane` banner `=== {name} : {cmd} ===`, status row
`"  {:5} {:16} {}"`, summary rule `"=" * 56`) and drove
`agent_common._failure_tail` directly on all of them.

## Findings

1. **MINOR — the first-FAIL anchor trusts any `  FAIL <token>`-shaped or
   `=== <name> : `-shaped line in unstructured step output, and bar-shaped
   text EMBEDDED in a step's output can silently hijack the window onto a
   PASSING step.** The designed shapes all hold (see "none against" below),
   but three constructed shapes break the window's truthfulness, driven
   directly through `_failure_tail`:
   - a passing step's output quoting a `  FAIL  tests+coverage   exit 1 (3.4s)`
     line at line start (an old log pasted into test output) while the real red
     is `lint`: the extracted window was the PASSING `tests+coverage` step's
     banner section (`all good` / `  PASS  tests+coverage`), with zero bytes of
     the real `F401` error;
   - a passing step quoting a mock banner `=== tests+coverage : stub pytest -q
     ===` for the step that later genuinely fails: the window anchored on the
     quoted line and carried the quoting step's text (`fixture tail`), not the
     real `FAILED ... REAL ERROR` line;
   - the realistic one for THIS repo: a red `tests+coverage` whose pytest
     output embeds a nested scaffold bar (captured stdout of a failing
     integrate/check test — `STUB_CHECK_RED` prints exactly these rows). When
     the nested `  FAIL` row names the SAME step as the outer red (the common
     stub shape) the window is correct and even reaches the real `FAILED`
     line; but when it names a DIFFERENT step (`  FAIL  format ...` nested
     inside a red tests+coverage), the refusal window became the passing
     `format` step's own output (`146 files already formatted`) plus a
     `  FAIL  format` row — an actively wrong attribution, silent.
   Honest weighting: the OLD anchor was wrong on every full bar by
   construction, so this is a residual-risk class of the same text-scraping
   approach, not a regression on any shape the spec names; the DONE-WHEN is
   fixture-driven and satisfied; the scope guard ("one anchor fix", no
   machinery) rules out structural parsing; and on the refresh path the kept
   full log now survives regardless, which is the half that kills the WI-387
   triple-loss. Remedy owed: a one-clause known-limit in
   `_own_step_window`'s docstring (embedded bar-shaped text can misanchor;
   the kept log is the authority) — or a follow-up WI if the owner re-grades;
   nothing here warrants reopening the rung. -> @owner

2. **NOTE — a later refusal that keeps NOTHING leaves the branch's previous
   kept log in place, unmarked.** `_keep_refused_output` returns `""` on empty
   detail and on `OSError` (fail-soft, correctly), but does not remove
   `refresh-refused-<branch>.log` from the earlier refusal; a reader returning
   to the known path by habit after such a refusal reads the PREVIOUS red's
   evidence with nothing dating it. Inside the documented "one file per
   branch, overwritten by the next refusal" semantics (integrate.py docstring
   + Deliverable both state it), and the message-side behavior is right (a
   refusal that kept nothing names no path). Record-only. -> @owner

## None against — what I tried and could not break

- **The banner-match ambiguity I was most suspicious of is DEFENDED.** The
  real step list contains the prefix pair `trajectory` / `trajectory-map`
  (check.py step tables). Driven three ways: longer step failing at
  `--jobs 0` (inline statuses), longer step failing at `--jobs 1` (statuses
  only in the summary), and the SHORT step failing with the longer step's
  banner printed EARLIER — every window anchored on the correct step's own
  banner and carried its own output (`gen_trajectory: STALE` vs
  `check_trajectory: ERROR - blocked-ref`), never the sibling's. The defense
  is the marker's trailing delimiter: `"=== {} : ".format(parts[1])` — a
  `trajectory-map` banner does not start with `=== trajectory : `. The
  startswith-not-regex choice is justified in place (`tests+coverage` carries
  a regex metacharacter) and correct.
- **The remaining constructed shapes hold.** `--jobs 1` statuses-only: window
  = the failing step's own banner-to-next-banner block with the anchoring
  summary row appended (`  FAIL  tests+coverage` rides along; `Check summary`
  and the other steps' output excluded). First-FAIL step with EMPTY output:
  window = its banner + its FAIL row, next step's output excluded. Last step
  failing: window stops at the summary rule (`^\s*={8,}$` matches `"=" * 56`
  but not pytest's text-bearing `====== short test summary info ======`
  separators — checked). No banner at all (bare git text): the bounded
  WI-240-style fallback, now anchored on the FIRST fail. A bare `  FAIL `
  line with no step token: falls back instead of crashing.
- **The mutation-twin claim is TRUE — I reproduced the red myself.** Trunk's
  `_failure_tail` (main checkout at `ConcurrencyTrainRewrite`) run against the
  branch's two new fixtures produces exactly the claimed pathology: the LAST
  step's banner (`=== trajectory ...`, `check_trajectory: OK`) + `Check
  summary` rows, zero bytes of the failing step's output — both new tests
  would red under the old anchor and green under the fix.
- **The kept log, driven via the e2e test and verified by inspection.**
  `test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log`
  (in the 137 green below) drives a real red refresh: the refusal names
  `<root>/out/run-logs/refresh-refused-wi-401.log`, the file holds the WHOLE
  bar output (summary included), and both the lane worktree and the root are
  porcelain-clean after the undo. The home is outside the lane worktree by
  construction (`Path(root)`, while the reset and `_shed_residue` run in
  `wt`), gitignored in this repo (`.gitignore:17` `out/`) and in a fresh
  scaffold (`project-trajectory/gitignore.template:35` `out/run-logs/`,
  seeded by `bootstrap.py:1411`; unchanged by this diff — it predates the WI,
  the same home agent_loop already uses for session streams). Branch names
  are sanitized to `[A-Za-z0-9._-]` before entering the filename, so a hostile
  branch name cannot traverse. NO rotation/indexing/pruning layer exists —
  `_keep_refused_output` is one `mkdir` + one `write_text` — and its absence
  is recorded three times (docstring "Deliberately no rotation, indexing or
  pruning (WI-398's scope guard)", the ratchet stamp, the Deliverable).
  Overwrite-per-branch is stated in the docstring and the Deliverable.
- **Consumers.** Every `_failure_tail` caller (integrate x10 incl. the refresh
  undo, handback x5, the journal/park paths, `_lane_close` via drive) rides
  the same function; suites green below. `check.py`'s own printing is
  untouched (its diff is empty), honoring "do not touch what a PASSING bar
  prints".
- **Registration judgment — the no-new-rows call is defensible, said so as
  asked.** SR-132's AcceptanceCriteria pin refusal/stop semantics, not
  refusal PROSE; LLR-140's Detail names `claim/finished_branches/
  _verdict_gate/integrate_one/audit` and has never named `refresh` (a
  pre-existing shape, not created here); `_failure_tail` has had no LLR row
  since WI-240. The precedent holds as claimed: LLR-143/144/145 were filed
  for NEW MODULES (drive.py, handback.py, spec_move.py); WI-398 adds none.
  Both new surfaces ARE pinned by tests that live in TC-132's cited evidence
  file (`tests/test_integrate.py`) and the harness suite, so the behavior is
  regression-guarded without a row. One observation for the next registry
  pass, not owed here: LLR-140's Detail could gain a `refresh` clause so a
  traceability reader can find where the station refresh (and its kept-log
  contract) is specified.
- **The record, re-run rather than read.** In the worktree at `e49fcbd8`:
  `tests/test_agent_common_harness.py` **17 passed in 0.04s** (fig claim: 17 —
  agrees); `tests/test_integrate.py tests/test_handback.py tests/test_drive.py`
  **137 passed in 28.40s** (fig claim: 137 — agrees); smoke tier **619 passed,
  2 skipped in 10.89s** (Deliverable's fig at `b121aba8` says 615/6 — same
  universe of 621, four environment-dependent skips pass on this machine);
  `check_trajectory --root . --strict` rc=0 (11 WARNs, the same 11 trunk
  prints — none about WI-398); `check_doc_refs --root . --strict` rc=0;
  `check_figures --root . --strict` rc=0, **14 declared figure(s), every one
  carrying its command and revision** — two spot-checked by re-running their
  commands with agreeing totals; `ruff format --check` 152 files already
  formatted; `ruff check` All checks passed. Size census by the ratchet's own
  metric: agent_common.py **1784**, integrate.py **1977** — both baseline
  re-stamps agree, both dated 2026-08-01 with WI-398 reasons. R-A/R-F are
  inside the rc=0 above (a done WI with an uncleared SpecRef or undated
  Deliverable would flag); the Deliverable is dated 2026-08-01 and every
  number in it re-verified true. `docs/work/` delta is exactly the WI-398
  active-to-complete move and nothing else; the `WI-398` token in
  `docs/status.md:173` sits inside the GENERATED frontier block (exempt from
  the forward-only rule; it drops at the merge's regen).

**THIS IS AN APPROVE:** I went at the two claimed surfaces with the real step
list's prefix pair, quoted status rows, mock banners, nested bars, empty-output
and no-banner shapes, and the designed behavior held on every shape the spec
promises; the one crack found (finding 1) is an adjacent residual of the
text-scraping approach the scope guard deliberately kept, is strictly narrower
than the always-wrong window it replaced, and is backstopped by the kept full
log on the path where diagnoses were being lost.

VERDICT: APPROVE findings=2
