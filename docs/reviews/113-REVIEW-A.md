# 113-REVIEW-A — WI-268 (`--dual-plan` flag path honors `autonomous`; SR-108 widened)

Independent adversarial review (REVIEW-A) of commit `0c1d108` on
`dualplan-routing-fix` (WI-268). Reviewer did not write the code and read no
builder self-assessment (the `docs/log.md` WI-268 entry was treated as narrative,
not evidence). Judged the diff + its requirement surface and drove the shipped
paths. Rubric: `docs/rubrics/code-review-adversarial.md`.

## Scope / subject frame (R1)

**Behavior change.** The single-shot `agent_loop --dual-plan <WI>` early path
(`agent_loop.py` `main`, ~line 2857-2886) previously returned `EXIT_NEEDS_HUMAN`
(7) **unconditionally** on a dual-plan round PAGE, writing the NEEDS-HUMAN
run-state only under `attended`. The change branches the PAGE handling on
`plan_round.page_action(gate_policy)`: `stop-needs-human` (attended, and
unknown/absent policy — `page_action` fails safe to attended) keeps NEEDS-HUMAN
run-state + stop banner + `EXIT_NEEDS_HUMAN`; the else arm (autonomous →
`design-check-session`, single-ratify → `surface-block-continue-others`) writes
run-state `RUNNING` + an attention banner and returns `EXIT_STALL` (4) — the
pause-free attention end state the dispatcher's dual-paged route-on reaches via
`agent_dispatch._terminal_decision`.

**Blast radius.** (a) Exit-code contract 7→4 for a `--dual-plan` PAGE under
autonomous/single-ratify; (b) a new unconditional `_write_runstate(docs,
"RUNNING")` on the else arm where pre-fix left run-state untouched; (c) the
`agent-resume.*` launchers (they `exec agent_loop.py --root . "$@"` and propagate
the raw exit code — no 7-vs-4 branching, and they never inject `--dual-plan`
themselves); (d) the spine rows SR-108 / LLR-096 / TC-098, widened (not minted)
to cover both dual-plan PAGE entries.

**Requirement it must satisfy.** The widened SR-108 (both the dispatcher
disposition and the `--dual-plan` single-shot round map a PAGE through gate
policy: hard-gate a human only under attended, otherwise reach RUNNING +
`EXIT_STALL`, never a human gate) and the WI-268 Done-when.

Worst failure classes hunted first (R3): a silent fail-open (the else arm
swallowing a page that should still gate a human, or a non-PAGE `error` outcome
misrouted through it); a run-state clobber erasing a meaningful NEEDS-HUMAN; an
exit-code-contract break in a launcher/orchestrator; and the misleading
`design-check-session` label semantics.

## What I drove (reproduced, not assessed — R2 / R5)

**1. The targeted tests pass on the shipped code.**
```
$ ./.venv/bin/python -m pytest -v tests/test_agent_loop_dualplan.py \
    -k "arbiter_disagreement or dispatcher_dual_page"
  test_arbiter_disagreement_pages                          PASSED
  test_arbiter_disagreement_autonomous_stalls_not_pages    PASSED
  test_dispatcher_dual_page_attended_parks_needs_human     PASSED
  test_dispatcher_dual_page_autonomous_continues_pause_free PASSED   (4 passed)
```
Both flag-path tests drive the REAL `agent_loop --dual-plan WI-002` entry via
subprocess with a fake CLI whose position-biased arbiter (`label = "A"`) makes the
two position-swapped runs pick different underlying plans → a genuine
position-unstable PAGE. attended asserts rc=7 + run-state `NEEDS-HUMAN`;
autonomous asserts rc=4 + run-state `RUNNING` + no `NEEDS-HUMAN`.

**2. The regression BITES pre-fix (R5.3) — the test proves the fix.** I reverted
ONLY the fix hunk in `agent_loop.py` (restored the pre-fix unconditional `return
EXIT_NEEDS_HUMAN`) and re-ran the new test:
```
  test_arbiter_disagreement_autonomous_stalls_not_pages    FAILED
  E  assert 7 == 4     (returncode 7 = EXIT_NEEDS_HUMAN; the test wants 4 = EXIT_STALL)
```
Then `git checkout -- project-trajectory/scripts/agent_loop.py`, re-ran → 1
passed, and `git status` clean. The green is load-bearing, not vacuous.

**3. No `error`-outcome conflation (fail-open hunt).** The flag path calls
`plan_runner.run_dual_plan_round` **directly** (agent_loop.py:2848), whose entire
return contract is `("SELECTED", …)` or `("PAGE", …)` — never `"error"`. The
`"error"` outcome is introduced only by the dispatcher's `dual_plan_disposition`
**wrapper** (agent_dispatch.py:1906/1909/1912/1935: staging-worktree / reset /
headerless-registry faults), which the flag path never invokes. So on the flag
path every non-`SELECTED` outcome is a genuine PAGE; the else arm cannot swallow a
disguised error. `run_dual_plan_round` also converts its own expected failures to
PAGE (plan_runner.py:462, 223) rather than raising, so no exception escapes past
the branch.

**4. single-ratify parity confirmed against the dispatcher.** `page_action`:
attended/unknown→`stop-needs-human`, autonomous→`design-check-session`,
single-ratify→`surface-block-continue-others`. The flag path's else arm has NO
further branching on the action string, so single-ratify and autonomous reach the
identical RUNNING+`EXIT_STALL` terminal. The dispatcher's PAGE handling
(agent_dispatch.py:3334 `if action == "stop-needs-human": … else: …release,
quarantine, park "dual-paged"`) likewise routes BOTH single-ratify and autonomous
through its else arm to the same `_terminal_decision` → RUNNING + `EXIT_STALL`.
Parity holds; the widened SR-108 AC ("autonomous/single-ratify → RUNNING +
EXIT_STALL") is accurate for both sites.

**5. run-state clobber is the fix working, not a defect.** Writing RUNNING is
*required* for the pause-free invariant — leaving run-state untouched (the pre-fix
behavior) would let a launcher read a stale `NEEDS-HUMAN` and wrongly stop,
defeating the fix. `_write_runstate` is a plain overwrite; RUNNING is
deliberately NOT in `END_STATES = ("DONE","BLOCKED","NEEDS-HUMAN")`. The flag
path was already a run-state author (the pre-existing attended branch writes
NEEDS-HUMAN), and run-state is dispatcher-regenerated. Under autonomous the
dispatcher itself never leaves a dual-page NEEDS-HUMAN to clobber (it routes on),
and the flag is a single-shot manual/orchestrator path never looped by a
launcher — so the theoretical "erase an unrelated NEEDS-HUMAN" edge is both
outside the intended workflow and self-correcting on the next dispatch. `stop_banner`
only prints (it reads `status.md` for an excerpt but never writes it), so the
sentence passed as its `label` is cosmetic — no status.md mutation, no format break.

**6. Exit-code contract — no consumer breaks.** grep of the launchers +
scripts: the only `agent_loop --dual-plan` reference outside the flag definition
is a human-readable suggestion string in the dispatcher's `needs_human_ask`
(agent_dispatch.py:3342). `agent-resume.sh` `exec`s and propagates; `.cmd`
captures `%ERRORLEVEL%` and exits with it unbranched. Nothing programmatically
distinguishes 7 from 4 for this path.

**7. Spine gates + full G3 gate green (driven, not trusted).**
```
$ ./.venv/bin/python .../trace.py --root . --strict
    SN=25 SR=109 LLR=97 TC=100 orphans=0 integrity=0 …            EXIT 0
$ ./.venv/bin/python .../check_trajectory.py --root . --strict
    check_trajectory: clean (266 WI, 254 done, graph acyclic).    EXIT 0
$ cat docs/gate                                                   -> G3
$ ./.venv/bin/python .../check.py --gate G3
    tests+coverage 382.7s PASS · dupes PASS · derived-gate PASS ·
    arch-map "code map up to date" · trajectory-map "dashboard up to date" ·
    status-map up to date · okf "bundle up to date (407 files)" · skills-sync OK
    RESULT: PASS                                                  EXIT 0
```
The `trajectory-map`/`status-map` "up to date" results confirm the committed
`PROJECT_STATE.html` + `status.md` ARE fresh at commit time; a post-commit
`gen_trajectory.py` shows only a one-line `state as of commit` sha-stamp delta
(`54c4117`→`0c1d108`), the inherent parent-vs-self stamp, not content drift.
`gen_okf.py` regen produced no drift.

## Done-when coverage map (R4)

| Done-when item | Status |
| --- | --- |
| `--dual-plan` PAGE under autonomous/single-ratify → `EXIT_STALL` + RUNNING (never NEEDS-HUMAN); attended unchanged | **COVERED** — autonomous by `test_arbiter_disagreement_autonomous_stalls_not_pages` (driven, §1, bites pre-fix §2); attended by `test_arbiter_disagreement_pages` (driven, §1); single-ratify by the identical else-branch the autonomous test exercises (§4, no per-string branching) |
| Regression proves it; attended flag test + dispatcher pause-free invariant stay green | **COVERED** — all three driven green (§1); regression bite confirmed (§2) |
| SR-108/LLR-096/TC-098 amended + re-verified; `trace.py --strict` + `check_trajectory.py` green (0 findings); gate stays G3 | **COVERED** — §7 (both strict, exit 0; `docs/gate` = G3) |
| Full suite + `check.py --gate G3` green; dashboard + arch-map regenerated; log.md + status.md recorded | **COVERED** — §7 (`check.py --gate G3` RESULT: PASS, all 16 steps; dashboard/status/okf/arch-map "up to date"); log.md + status.md present in the diff |

Every Done-when item maps to a driven observation; none UNCOVERED.

## Spine hygiene

- **Widen vs mint — correct.** The flag path is a sibling call-site of the same
  PAGE→gate-policy obligation, exactly the LLR-095 multi-site precedent. The two
  real `page_action` call-sites are `agent_loop.py:2860` (flag, new) and
  `agent_dispatch.py:3330` (dispatcher, pre-existing) — precisely what the widened
  SR-108 now claims. No third site exists (grep-confirmed), so the widened
  requirement is complete, not over-claiming.
- **LLR-096** now honestly lists `…/agent_loop.py` + `main` alongside the
  dispatcher symbols; the flag PAGE handling is in `agent_loop.main`. Accurate.
- **TC-098 evidence** adds both `test_arbiter_disagreement_pages` (attended) and
  `…_autonomous_stalls_not_pages` (autonomous) to the existing dispatcher tests —
  both flag-path policies covered.
- **No missed consumer** (the WI-267/WI-262 failure mode): the only consumers of a
  `run_dual_plan_round` PAGE are the flag path and `dual_plan_disposition` (the
  dispatcher), and both map through `page_action`; this WI adds a mapping to an
  existing call-site rather than introducing a new vocabulary needing an audit.

## Observations (non-blocking, no change required)

- The pre-existing stderr line `gate-policy autonomous -> design-check-session`
  (agent_loop.py:2861-2866, OUTSIDE the diff hunk) and the new test's
  `assert "design-check-session" in proc.stderr` name a session that never runs.
  This is honestly recorded as a Non-goal + Residual in `docs/specs/WI-268.md`,
  matches the label the dispatcher already journals, and the realized behavior
  (RUNNING + STALL) is correct — an intent label, not a false claim of work done.
  Surfaced for owner visibility only; the Residual already owns the eventual fix.
- single-ratify has no dedicated flag-path test, but it traverses the exact
  else-branch the autonomous test exercises (§4) — consistent with the
  dispatcher's own single-ratify coverage. Not an uncovered acceptance.

## Verdict

Tried to break it across every worst class the frame named — fail-open via an
`error`-outcome misroute, run-state clobber, exit-code-contract break, and the
misleading-label semantics — and it survived each: the flag path's outcome
vocabulary is {SELECTED, PAGE} so the else arm is always a genuine page; the
RUNNING write is required for the invariant; no consumer branches on 7-vs-4; and
the label is a documented intent string consistent with the dispatcher. The
regression bites pre-fix, all four driven tests pass, every Done-when item is
covered, the spine widening is complete and honest, and the full G3 gate is
green.

- VERDICT: APPROVE findings=0
