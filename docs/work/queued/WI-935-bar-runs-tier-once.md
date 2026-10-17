+++
id = "WI-935"
title = "The commit bar runs the smoke tier once: the lints run first, then the budget step's timed run, which now fails on a red tier"
workstream = "process"
sr_refs = []
specref = "docs/decisions/coordinator-2026-10-16.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = []
+++

## Context

The per-commit bar is one declared command, `run_menu.py smoke`. Its steps
are `docs/stack.ini` `[run] smoke`: the smoke tier, `trace.py --strict`,
`check_trajectory.py --strict`, `check_docs.py --root . --stale`, then
`scripts/check_smoke_budget.py --mode enforce`. The last step gets no
`--elapsed`, so the budget script runs the smoke tier a second time to time
it. Every bar costs two tier runs: about 112 to 115 s quiet on 2026-10-16,
where the tier alone is judged against 60 s (wi-914 D-006; coordinator-cycle
recipes §6). WI-914's post-checkpoint gate found it (007-REVIEW-B, MINOR). The
owner ruled in session to file this row now and queue it right after the
row-2 batch. It changes the commit bar, so it lands alone
(coordinator-2026-10-16 D-006).

The original rationale, read before drafting:

- WI-496 (OI-52 ruling (a), 2026-08-23) wired `check_smoke_budget.py --mode
  enforce` beside the smoke `pytest` call, so that the bar meant results AND
  seconds. WI-281 had built the script's no-flag form for CI's timing lane,
  and that form times a fresh run of its own. So from WI-496 on, the tier ran
  twice per bar. At a 27 s tier, nobody remarked on the cost.
- WI-914 (review-churn ruling 6) moved the steps into `[run] smoke` and put
  the strict lints between the tier and the budget. The `.desc` gives the
  reason: the budget runs "last so a breach under load never hides a lint
  red". `tests/test_smoke_budget.py::test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`
  pins that order. This row keeps the budget last.
- `--elapsed` takes a time that was already measured, but no portable shell
  line can measure one. `cmd.exe` and `sh` share no timing syntax, and steps
  joined by `&&` share no state except the file system.
- The timed form already reads the tier's exit code. On a red tier it prints
  a note ("test failures are not a budget breach") and exits on the budget
  verdict alone. WI-281 built it that way because CI's timing job sits beside
  a test job that already reds on a failing test. As the bar's only tier run,
  the form would let a red tier pass the bar. That is why it must now exit
  nonzero on a red tier.

The construction is the owner's (coordinator-2026-10-16 D-009). The drafted
alternative was not taken: a `--run-tier` producer writing a per-checkout
timing record for a `--from-record` judge to read, with a Trust section over
the record.

No spine row names the bar line or the budget script. A grep of
`docs/requirements/*.toml` and `docs/test/test-cases.toml` for `smoke`,
`budget`, `check_smoke_budget` and `60 s` finds only the performance-budget
rows (SR-167 and the PB registry) and Smoke tier cells. `scripts/` is this
repository's own tooling and sits outside the traced product. WI-281, WI-496,
WI-652 and WI-869 changed the same machinery and touched no rows. The
anchor is SN-007 (approved): "The declared bar is green before a change
lands." SN-012 asks that small changes stay cheap, and this row cuts the
bar's cost. SN-008 says a pass verdict never hides an unmet criterion, and
that is why a red tier must fail the timed form.

**The order, checked.** Nothing in the smoke tier depends on running before
the lints, or on what they write.
- The lints' only write at the checkout root is `trace.py`'s gitignored
  `docs/test/report.md`. `check_trajectory.py` and `check_docs.py` write
  nothing there.
- Every test that reads a `report.md` reads a scaffold's. The tests that run
  `check_docs.py` on the real root pass `--ignore docs/test/report.md`. No
  test asserts that the file is absent.
- In any working checkout, the previous bar's report already exists while
  today's tier runs.
- The tier writes nothing the lints read: it writes pytest's cache and its
  temporary directories, none of them under `docs/`.
- The lints keep their order among themselves.

## Deliverables

1. **The timed form fails on a red tier.** In `scripts/check_smoke_budget.py`,
   the no-flag form still times the tier exactly as today: the
   `perf_counter` window around `smoke_argv`. It still prints the
   `smoke wall-clock budget:` line, with any breach message, and the
   red-tier note. When the tier exits nonzero, the form then exits with the
   tier's own exit code, in both modes. A green tier exits on the budget
   verdict as today. If the tier is red and also over budget, the form
   prints both and exits with the tier's code.
   - **Why the tier's own code, not 1.** pytest's code already tells the
     kinds of red apart: 1 failed tests, 2 interrupted, 3 internal error,
     4 usage error, 5 nothing collected. A 5 means the declared selector
     matched nothing, which is a misdeclared tier rather than a failing
     test, and a flat 1 would hide that. The bar's launcher already passes a
     child's code through unexamined (`run_menu.py`, IF-158), and so does
     this form. The code's overlap with a breach's 1 does no harm: every
     caller tests only for nonzero, and the printed lines name the cause.
   - **No new flag.** `--elapsed` keeps its behaviour, because it runs
     nothing. Every caller of the timed form wants a red tier to fail:
     - the bar, whose only tier run this becomes;
     - the harness `[step:smoke]`, whose own comment calls it "the existing
       per-commit regression bar". Passing a red tier was a fail-open there.
       At this repository's DevStg-Impl the gate plan's `tests+coverage`
       step masks it, but the step's `from-stage` is DevStg-Tests;
     - CI's `smoke-budget` job, where a red tier gives no valid budget
       reading. The `test` job already reds the same push, so the job only
       adds a second red. Its comment ("ENFORCES it (exit 1 on breach)")
       stays true.
2. **The bar line.** `docs/stack.ini` `[run] smoke` becomes:

   ```
   python project-trajectory/scripts/trace.py --strict && python project-trajectory/scripts/check_trajectory.py --strict && python project-trajectory/scripts/check_docs.py --root . --stale && python scripts/check_smoke_budget.py --mode enforce
   ```

   Its `.desc` names the order and its reason: both strict lints and the docs
   staleness check, then the smoke tier, run once and timed against its 60 s
   budget. The budget comes last so a breach under load never hides a lint
   red, and a lint red stops the bar before the tier runs. If another landing
   adds a step before the budget step (WI-916's `check_resync.py`), that step
   keeps its place.
3. **Tests.**
   - `tests/test_smoke_budget.py`'s step-list test expects the new line, and
     its comment states the new order.
   - `tests/test_check_smoke_budget.py` gains in-process cases. Each imports
     the script, stands in a trivial interpreter command for `smoke_argv`,
     and calls `main`. The new cases stay in the smoke tier.
4. **Text.**
   - The script's docstring:
     - "It defaults to `--mode warn` for LOCAL convenience" becomes: the
       default stays `warn`, for a hand run that only reports, while the
       commit bar, CI and `[step:smoke]` run `--mode enforce`.
     - The sentence calling local enforcement "the owner's dial and is
       queued (2026-08-21 close, Q-3)" now cites OI-52 ruling (a),
       2026-08-23, which settled it.
     - Usage: the no-flag line names its three callers and says a red tier
       exits with its own code. The `--elapsed` line drops "CI times the
       step, feeds it here", which no caller does, and names the hand
       wrapper.
     - The red-tier comment in `main` matches the new exit.
   - `tests/test_smoke_budget.py`'s module docstring loses "its local
     default is report-only `--mode warn`, while CI deliberately invokes
     `--mode enforce`". The commit bar and CI both enforce.
   - The `[run] smoke` `.desc` (deliverable 2).
   - The coordinator-cycle recipes §6 bullet on the double run says the bar
     runs the tier once, as the budget step's timed run after the lints. Its
     lesson stays: a hand wrapper must exit nonzero on a red tier or a
     breach.
   - The session-protocol skill's §3 says the lints run first and the budget
     step's timed run is the bar's only tier run, failing on a red tier or a
     breach.
   - Both skills are `scope: this-repo`, and their per-agent copies stay
     byte-identical.
   - CLAUDE.md and `.github/workflows/test.yml` stay true as written and are
     not changed.

## Done-when

- `tests/test_smoke_budget.py::test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`
  expects the four steps above in order. It also asserts that exactly one
  step runs the tier: the last, `python scripts/check_smoke_budget.py --mode
  enforce`, with no step calling `pytest` directly. It fails on today's
  line.
- `tests/test_check_smoke_budget.py::test_a_red_tier_exits_with_its_own_code_and_still_reports_its_time`
  passes. With the stand-in tier exiting 3, `main` returns 3 in both modes
  and prints the `smoke wall-clock budget:` line and the red-tier note. It
  fails on today's code, which returns 0.
- Beside it, two in-process cases pass:
  - a green stand-in tier returns 0 within budget;
  - a red stand-in tier over a stood-in 0 s budget returns the tier's code
    in enforce mode, with both messages printed.
- The four existing tests in `tests/test_check_smoke_budget.py` pass
  unchanged.
- Coverage (S3): the promise is over the tier's exit code, closed by a
  default. Zero is green, and any other code is red and passes through. The
  bar is nonzero exactly when a lint is red, the tier is red, or the tier's
  wall time exceeds the budget. Tier failures are reported only when no lint
  is red.
- The new bar is green on the lane tip in a quiet run, pasted in full. The
  output shows one pytest session. The log fragment records the bar's whole
  wall time and the tier's own time, beside today's 112 to 115 s.
- The texts in deliverable 4 say the bar runs the tier once, last, after the
  lints. The per-agent skill copies are byte-identical.
- `check_trajectory.py --strict` exits 0.

## Scope answers

- **S1, independently landable deliverables.** Two pieces, kept together on
  purpose.
  - The red-tier exit could land alone. It closes `[step:smoke]`'s
    fail-open.
  - The line cannot land without the exit change. Alone, it would make the
    bar pass a red tier.

  So both land in one commit, and nothing lands first.
- **S2, authority over a hold, an act or a gate.** No file gains authority.
  The budget step already gates the bar. Its exit code now also carries the
  tier's result, which the removed first step carried. No `## Trust` section
  (D-009).
- **S3, closed coverage.** See the Done-when's coverage bullet.
- **S4, planning need: `none`.** None of the rubric's `single` criteria
  holds:
  - the row has no `## Trust` section;
  - it touches one script family, `scripts/check_smoke_budget.py`, which is
    untraced, has no interface row, and has no other caller of the changed
    branch;
  - it promises no behaviour over an input space beyond the tier's exit
    code, which is two cases: zero, or anything else.

  The rubric's "a diff a cheap test fully specifies" fits: two in-process
  tests pin the one changed branch, and the exact step-list test pins the
  line. The row adds no code path. The red-tier branch exists today, and it
  changes from printing a note to also returning the code. D-005's deletion
  exemption is not needed.
- **S5, architectural delta.** No state, boundary or input is added. One
  output gains values: the timed form's exit, once 0 or 1, now carries the
  tier's codes. It depends on an input the form already reads, the tier's
  exit code, which until now was only printed. This is within the row's
  scope and carried by deliverable 1. No component or interface row changes,
  and no refactor row is owed.
- **S6, dependencies.** `needs = []`. Two claimed lanes land later, touch
  the same surfaces and will rebase across this row:
  - WI-916 adds a step to `[run] smoke` before the budget step, so it edits
    the same step-list test;
  - WI-915 changes the script's stack.ini loader (`_profile`).

  Each is a small rebase, and neither changes what this row builds. The row
  adds no third-party package, tool or service, and the script stays
  stdlib-only.
- **RESYNC.** No entry is owed, because every changed file is this
  repository's own:
  - `scripts/` and `tests/`;
  - `docs/stack.ini` `[run]`, which the shipped template does not carry;
  - two `scope: this-repo` skills, which bootstrap never materializes.
- **B1.** No deliverable hides in the Context.
- **B2.** The row proposes no split.
- **B3.** No consumer re-derives a past decision. The budget step judges the
  run it times.
- **B4.** The Done-when needs no owner act or credential.

## Calls ruled at filing

- **Filing and placement** (coordinator-2026-10-16 D-006, ruled as
  recommended): the row is filed now, queued right after the row-2 batch
  (WI-928 to WI-931), and lands alone.
- **Construction** (coordinator-2026-10-16 D-009, ruled as recommended):
  - the lints and the docs check run first;
  - the budget step runs last, and its own timed tier run is the bar's only
    tier run;
  - the timed form exits nonzero on a red tier;
  - there is no record, no new state and no Trust section.

  This spec applies the red-tier exit to every caller of the timed form, as
  D-009 states it without scoping it, and adds no flag.

No owner call remains.
