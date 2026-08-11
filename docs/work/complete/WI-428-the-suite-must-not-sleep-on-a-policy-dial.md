+++
id = "WI-428"
title = "The full-suite bar is a function of the wall clock: tests/test_agent_loop_critique.py (10 tests) does not RUN on a weekday between 12:00 and 19:00 UTC — it SLEEPS. conftest.set_process_key(seed=True) seeds a test scaffold's docs/process.toml from project-trajectory/process.toml.template, which declares blackout = \"12:00-19:00\"; critique_repo is the session-driving fixture that calls it, so the agent_loop under test correctly honors a LIVE policy window and waits it out (measured blackout_wake(\"12:00-19:00\", 14:22Z) = 16650 s). The suite therefore reports green as a function of time-of-day, and it has already misled this program once — docs/repo-lock.md §5 records this module as 'not reproduced, 2026-08-10 ... environmental or flaky'. It is not flaky; it is deterministic in UTC time-of-day. Make the kit's own test scaffolds immune (a seeded session-driving scaffold carries a DISABLED blackout, per the dial's own documented semantics), find EVERY fixture with this exposure rather than assuming critique_repo is alone, and add a GUARD that reds if a session-driving scaffold ever inherits an enabled window again. The blackout dial's own behavior must still be really tested, fast, on an injected clock. DO NOT change blackout = \"12:00-19:00\" in process.toml.template or docs/process.toml — WI-148's default is a ruling, and re-deciding it is the owner's call, tabled separately. This row makes the SUITE honest, not the policy different."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**DONE 2026-08-11 (`bea15693` + this close). The suite no longer sleeps, and it
was proven by producing the full unfiltered bar INSIDE the blackout window** —
started `16:40:40 UTC`, Tuesday, i.e. 4 h 40 m into the 12:00–19:00 window that
used to swallow ten tests: **2244 passed, 9 skipped in 378.81s**, no
`--ignore`, nothing excluded.

The policy is untouched. `project-trajectory/process.toml.template` and
`docs/process.toml` still declare `blackout = "12:00-19:00"`; a test asserts it,
so this row cannot be mistaken for the re-decision the owner has tabled.

### The exposure census — measured, not grepped

Grep can only find the fixtures that *look* exposed. The list below was produced
by **instrumenting the shipped code**: `agent_common.blackout_wake` was patched
in a throwaway tree to log `(cwd, window)` at every point where it resolved an
ENABLED window, and return `None` instead of a wait, then the **whole suite** was
run twice at ~16:15 UTC on a Tuesday — inside the window, so every scaffold
carrying the shipped default had to announce itself. That catches the fixture
that sleeps *and* the fixture that merely holds a live dial without reaching the
check yet. The instrumentation was reverted before any real change (`git diff`
clean at the claim).

| Fixture | Module | Verdict |
|---|---|---|
| `critique_repo` | `tests/test_agent_loop_critique.py` | **SLEEPS.** The only fixture that actually waited. 10 tests, 32 recorded waits (some tests launch the loop more than once), every one `window='12:00-19:00'` with `wake≈10 023` s at the time of the run. |
| `scaffold_with_queued_wi` | `tests/test_dispatch.py` | **LATENT, and fixed.** Not found by the census — it never reaches the check today — but it bootstraps its scaffold with `bootstrap.py`, so it carries the live window verbatim, and its module launches `agent_loop.py` for real. Found by the new source rule the moment that rule was written, which is the guard paying for itself before it shipped. |
| every other `agent_loop` / dispatch / dual-plan / adjudicate fixture | `test_agent_loop{,_env,_review,_routing,_worker}.py`, `test_adjudicate_brief.py`, `test_dual_plan_round.py` | **Clear.** Their repos carry no `docs/process.toml` at all, so `declared_policy` returns `""` and the dial is inert. Confirmed by the census, not assumed. |
| `loop_repo` in `test_blackout_present_but_inactive_does_not_block` | `tests/test_agent_loop.py:322` | **Clear, and deliberate.** It authors its own legacy `docs/blackout` window 30 minutes in the future so it is never active — the test that proves the loop reads the file. Left alone (see Findings: it does read the real clock). |

So: **one fixture manifesting, one latent, and a positive result that the other
seven session-driving modules were never exposed.**

### What changed

1. **`tests/conftest.py` — `set_process_key(..., seed=True)` disables the window
   on the file it seeds.** This is the seam the defect came through:
   `critique_repo` calls it to set `review_rounds`, and got a whole live policy
   file as a side effect. Scaffolds opt out through the dial's **own documented
   disable form** (the empty value; `start == end` is the other) rather than a
   test-only special case, so the seeded file still exercises the parse path a
   downstream scaffold takes.
2. **`conftest.disable_blackout(root)`** — the explicit call for the other way a
   scaffold is built, `bootstrap.py`, where conftest's seeding never runs.
   Delegates to `bootstrap.set_process_key` rather than carrying a second
   line-rewriter.
3. **`conftest.blackout_is_live` / `live_blackout_scaffolds`** — the invariant,
   stated once. `blackout_is_live` asks the **shipped** `parse_blackout` and the
   **shipped** `start == end` rule; a guard that re-implements what it guards can
   only ever agree with itself.
4. **`tests/test_dispatch.py`** — `scaffold_with_queued_wi` now calls
   `disable_blackout`.
5. **`tests/test_blackout_isolation.py` (new, 11 tests, 0.06 s)** — the guard and
   the dial's own coverage.
6. **`docs/stack.ini`** — smoke `max-tests` 930 → 980, re-stamped with its reason
   and a signed figure (see Findings).

### The guard, and its planted-defect proof

The seeding change alone is a one-off; the guard is the deliverable. It has two
halves because the failure has two shapes.

**Half 1 — the autouse sweep (runtime).** `conftest._no_live_blackout_in_session_scaffolds`
runs after every test in a module that launches the coordinator, and reds if a
scaffold under that test's `tmp_path` declares a live window. Membership is
**derived from each module's own source** (the `SCRIPTS / "agent_loop.py"` launch
idiom), never a hand-kept list, so a new session-driving module joins the guard
by existing. It is scoped on purpose: `test_bootstrap`'s
`test_scaffold_ships_every_policy_dial_in_one_home` asserts a real scaffold
carries `"12:00-19:00"` and is checking the right thing.

Proven red against a planted defect — a throwaway module carrying the launch
idiom, whose fixture re-enables the dial in a `tmp_path` scaffold (run, observed,
deleted):

```
E       AssertionError: WI-428: a session-driving test scaffold inherited a LIVE
blackout window — the loop under test will SLEEP rather than run, and the suite
will report green on the tests that did run. Seed through
conftest.set_process_key or call conftest.disable_blackout(root).
/private/var/folders/.../pytest-478/test_a_session_driving_fixture0/docs/process.toml
 -> '12:00-19:00'
=========================== short test summary info ============================
ERROR tests/test_wi428_planted_defect_demo.py::test_a_session_driving_fixture_that_re_enables_the_dial
1 passed, 1 error in 0.03s
```

**Half 2 — the source rule (pre-emptive), because the sweep has a real hole.**
A teardown assertion never fires for a test that *hangs*, which is exactly the
symptom. So `test_every_loop_launching_module_that_bootstraps_disables_the_window`
reds without running anything: a module that launches `agent_loop.py` **and**
builds its scaffold with `bootstrap.py --dest` must call `disable_blackout`. Its
first run reds honestly, on a real latent exposure nobody had looked for:

```
E  AssertionError: WI-428: these modules launch agent_loop.py against a scaffold
they bootstrapped from the kit template, which ships a LIVE blackout window —
the loop will sleep instead of running. Call conftest.disable_blackout(root)
on the scaffold: test_dispatch.py
```

**And the permanent in-suite proof**, so neither half rests on a run nobody can
repeat: `test_the_guard_reds_on_a_planted_live_window` seeds a scaffold (guard
green), re-enables the dial (guard names the file and the value), and disables it
again (green). It also asserts the planted scaffold *would really have slept* —
`blackout_wake('12:00-19:00', 2026-08-11T14:22) == 16680` s, the measured
reproduction on an injected clock, so the guard is shown catching a sleeping
scaffold rather than a string.

### The dial's own behavior: VERIFIED as already tested, plus what was missing

The brief allowed "add or verify". Verified: `tests/test_agent_loop_policy.py`
already covers `parse_blackout` and `blackout_wake` **on an injected clock** —
inside-window, outside-window, both half-open boundaries (`12:00` waits, `19:00`
is clear), seconds honored, the empty-value and `start == end` disable forms,
malformed and out-of-range lines, the Mon–Fri weekday/weekend boundary, and the
past-midnight wrap — and `blackout_wait` with an injected `emit`/`sleep`, so the
countdown is tested without a real delay. Nothing there reads `datetime.now()`.
That coverage was never the problem; the problem was that it sat beside a suite
that took the *real* window from a config file.

What was missing, and is now added, is the **negative universal** the fixtures
actually depend on: `sleeps_at(window)` sweeps a full week of injected clocks
(7 days × 24 h × 3 minutes = 504 samples) and asserts a disabled dial has **no**
time at which it waits. One spot check cannot establish that, and a spot check is
what the 2026-08-10 "not reproduced" verdict was.

### The bar, produced inside the window

`date -u` → `Tue Aug 11 16:40:40 UTC 2026` (weekday, 4 h 40 m into 12:00–19:00).

```
2244 passed, 9 skipped in 378.81s (0:06:18)
```
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=bea15693 -->

Re-run at `16:47:24 UTC` with `-rs` to name every skip: identical,
**2244 passed, 9 skipped in 387.47s**.

**Reconciliation against the 2227 / 5 baseline.** The baseline was
`2242 collected − 10 excluded = 2232 selected = 2227 passed + 5 skipped`. This
run selects `2232 + 10 (the critique module, now RUNNING) + 11 (the new guard
module) = 2253`, and `2253 − 9 skipped = 2244 passed`. Exact, both columns.

The **4 extra skips (5 → 9) are this row's own open claim, not env gating.** The
`-rs` listing is unambiguous: four `tests/test_wi_convert.py` cases skip with
*"live registry has in-flight claims: docs/work/active/wi-428-…"*. They return to
passing the moment the spec moves to `complete/`, so the closed tree reads
**2248 passed, 5 skipped** — skips back to the baseline's five, which are the
five platform/coverage gates (`test_agent_loop.py:898`, `test_check_harness.py:30`,
`test_cpu_cap.py:140` and `:303`, `test_onboard_devsetup.py:446`). Confirmed by
re-running the whole bar on the closed tree, started `16:58:06 UTC` — still
inside the window — which lands on the predicted figure exactly:

```
2248 passed, 5 skipped in 365.88s (0:06:05)
```
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=c47ec2da -->

The proof the defect is gone, at the same clock:

```
Tue Aug 11 16:38:02 UTC 2026
..........   10 passed in 3.90s   (tests/test_agent_loop_critique.py)
```
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto tests/test_agent_loop_critique.py" rev=bea15693 -->

Before the fix, at the same time of day, that module did not complete in 150 s
and each of its loop launches computed a ~10 023 s wait.

Commit bar: **928 passed, 6 skipped in 17.55s** smoke;
`check_docs.py --root . --stale` OK (810 docs, 0 broken).
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=bea15693 -->

`trace.py --strict` → rc 0. `check_trajectory.py --strict` → rc 0.
`check.py --jobs 0` → **RESULT: PASS**. Every generated surface `--check` fresh.

### Findings surfaced, not fixed

1. **`test_blackout_present_but_inactive_does_not_block` reads the real clock.**
   It computes a window 30–31 minutes ahead of `datetime.now()` so it is never
   active. That is the same *class* the brief forbids, held safe only by a
   30-minute margin against a saturated box (an L-17 review already widened it
   from 2 minutes for exactly that reason). It is a genuine loop-level test that
   the file is read, and making it deterministic needs an injected clock across
   the subprocess boundary, so it is a design question, not an inline fix.
2. **The smoke membership ratchet was re-stamped, 930 → 980.** WI-427 filed the
   thin headroom (923 of 930) as its own finding; this row's 11 in-process tests
   would have breached it. The wall clock — the real sensor — did not move:
   **17.6 s against the 60 s budget**. The margin was deliberately widened rather
   than re-set to the +15 the recent stamps held, because at 930 the ceiling sat
   7 above the then-current count, which is the near-exact freeze `stack.ini`'s
   own comment block warns against.
3. **The pre-existing `E741` in `tests/test_id_watermark.py:82`** is still the
   only `ruff check` error in the tree, unrelated and untouched.
4. **The census method is not reusable as shipped.** Instrumenting
   `blackout_wake` by hand found what grep could not, and there is no supported
   way to ask "which test scaffolds carry which declared policy". Every dial in
   `process.toml` is a candidate for this defect class — `blackout` is simply the
   only one that *waits*. If another dial ever grows a blocking behavior, the
   same census will have to be improvised again.

### Deliberate non-changes

`project-trajectory/process.toml.template` and `docs/process.toml` keep
`blackout = "12:00-19:00"` — and
`test_the_kit_still_ships_the_owners_live_window` now pins BOTH, plus the fact
that the value really does block (35 weekday hours a week, up to 7 h at a time).
That test is load-bearing in the other direction too: if the dial were ever
quietly emptied, every other test in the guard module would become a guard over
nothing, and this one reds first.

The autouse sweep is **not** suite-wide. A `docs/blackout` legacy file is **not**
swept (one deliberate writer, and SN-028 retired the file). `OWNER_SCRATCHPAD.md`,
`docs/repo-lock.md`, `docs/plans/*` and every registry row's text: untouched.

## Context

WI-427 surfaced this as its finding 1 and deliberately did not fix it: *"a bar
that silently blocks for a third of the day teaches people to skip it."* Its
2227/5 figure was measured with this module **excluded**, so the program's
headline suite number currently describes 2232 of 2242 collected tests.

**The class matters more than the ten tests.** This repo exists to eliminate
false greens (SN-008: a green must not hide a skipped check). A suite whose
membership depends on the wall clock is the purest form of that failure —
nothing errors, nothing is reported skipped, the ten tests simply never run and
the runner reports success on the other 2232. The earlier "not reproduced"
verdict is the predictable consequence: a probe outside 12:00–19:00 UTC passes.

**The boundary is the point.** The template's `blackout = "12:00-19:00"` is
WI-148's deliberate default, recorded in the template's own comment as a MOVE
that is not an occasion to re-decide the value. A test scaffold inheriting a
live operational policy is a *test-harness* defect, not a policy question. The
fix belongs in the seeding path, and the dial's own semantics already supply the
disable form (empty value, or `start == end`) — so the scaffolds opt out using
the documented contract rather than a special case.

**A seeding change alone is a one-off.** The durable deliverable is the guard:
a test that reds when a session-driving scaffold carries an enabled window,
proven non-vacuous against a planted defect.
