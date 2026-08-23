+++
id = "WI-496"
title = "Re-tier smoke to fit its 60 s ceiling everywhere, then enforce the seconds at the commit bar (OI-52 ruled (a), 2026-08-21)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Both ordered steps landed, in order — the re-tier first, enforcement only
after it measured green.

**1. Re-tier.** Five subprocess/scaffold-heavy modules moved from `smoke` to
`slow` in `tests/conftest.py` `SLOW_MODULES` (reasons and per-module figures
recorded there): `test_external_frame` (33 tests, every case takes the
`scaffold` fixture — a real `bootstrap.py` subprocess — plus `trace.py`/
`check` subprocesses), `test_baseline_snapshot` (40 tests, `scaffold` plus
repeated `trace.py`/`intake.py` `run_py` subprocesses), `test_selection_at_or_above`
(16 tests, `scaffold` plus `derive_stage.py`/`check.py` subprocesses),
`test_adjudicate_brief` (48 tests, real git repos with `agent_loop.py` driven
as a subprocess — the same class as the already-slow `test_agent_loop_review`),
and `test_intake` (26 tests, a real `git init`/commit repo built per test —
the same class as the already-slow `test_handback`). Nothing is deleted or
weakened: all five still run in full at slice/phase close and in CI.

Measured this box (3.11.9, `-n auto`), before and after:

- Before (baseline, this session): 1409 collected,
  `python -m pytest -q -n auto -m smoke` → **58.77 s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke --durations=0" rev=0cfb2e6f-dirty -->
  — 0.98x the 60 s budget, the same near-the-line reading
  `check_smoke_budget.py`'s 2026-08-21 re-argument and CLAUDE.md's prior
  stamp (54.9/64.0/55.7 s) both recorded.
- After, three warm runs: **27.27 / 28.16 / 27.86 s**, 1270 collected (1265
  passed, 5 skipped each run)
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=0cfb2e6f-dirty -->
  — ~2.15x under budget, the real headroom the ordering clause asked for.
  The STOP rule did not fire.

`docs/stack.ini` `[smoke-budget]`: `max-tests` re-stamped **1416 -> 1280**
(measured 1270 collected at the re-stamp, +10 headroom, the same small-slack
posture the file's prior stamps carried); `seconds` stays **60**, untouched —
the ruling is that the budget VALUE never moves, and this re-tier is what
gives the unchanged value real margin instead of none. Reasons and the fig:
lines are recorded in `docs/stack.ini` beside the new stamp.

**2. Enforce.** `check_smoke_budget.py --mode enforce` is now named beside
the smoke `pytest` invocation at every commit-bar location: the
session-protocol skill's own §3 command block (source
`project-trajectory/skills/session-protocol/SKILL.md`, fanned out
byte-identical to `.claude/skills/` and `.agents/skills/` via
`bootstrap.py --sync`, confirmed by `gen_skills_index.py --check-agents`) and
`CLAUDE.md`'s "Self-test before claiming done" bullet. The pre-commit hook
surface (`project-trajectory/hooks/pre-commit`, wrapped by `.githooks/pre-commit`)
runs no `pytest` at all — its floor is the freshness/integrity/format steps
only (`check.py --run-steps ...`, `check_trajectory.py --staged`,
`check_privacy.py`, `check.py --run-step format`) — so there was nothing to
wire there; checked before touching it, not assumed. CI's enforce lane
(`.github/workflows/test.yml`) is unchanged, as directed.

**3. Words.** Both wired locations now state the bar means results AND
seconds, both enforced (OI-52 ruling (a), 2026-08-23), replacing the wording
that let a worker read "passed" over a failed budget (the defect OI-52 was
minted for) with the command that actually fails on a breach, plus the fresh
27.27/28.16/27.86 s figures in place of the stale 2026-08-11/2026-08-20 ones.

Byte deltas (`wc -c`, before -> after):

- `CLAUDE.md`: 7513 -> 7831 (**+318**; cap 8500, 669 headroom left) —
  re-stamped in `project-trajectory/skills/byte-budget-guard/SKILL.md`'s
  Budgets table (source + its `.claude`/`.agents` copies), the row the
  first full-suite run caught unstamped
  (`test_capped_doc_baselines_match_the_real_sizes`).
- `project-trajectory/skills/byte-budget-guard/SKILL.md` itself (+ its
  `.claude`/`.agents` copies): 4841 -> 4834 (**-7**; cap 5000, self-referential
  row updated in the same edit that re-stamped CLAUDE.md's row).
- `project-trajectory/skills/session-protocol/SKILL.md` (+ its `.claude`/
  `.agents` fan-out copies, kept byte-identical): not in the capped/watched
  table (session-protocol carries no declared byte cap); grew by the same
  wording change, synced via `bootstrap.py --sync` and confirmed identical
  across all three copies.

`Deferred open items: none` — OI-52 closes with this row; no residue banked.

## Context

Executes OI-52's ruling (a) ENFORCE LOCALLY, with the owner's tuning
mandate: the 60 s budget is a WORST-MACHINE ceiling, not a this-box target
— the tier should pass within 60 s on every dev machine (a fast box might
pass in 30 s), because the point of smoke is that it executes quickly. The
budget VALUE does not move in either direction.

Ordering is load-bearing — the re-tier lands FIRST:

1. **Re-tier.** The tier grew from ~900 tests to ~1,300 in a month and
   runs at 0.9–1.1x budget on this box (the 2026-08-21 re-measurement in
   `scripts/check_smoke_budget.py` is the current basis). Move the
   subprocess/scaffold-heavy modules that crept back into
   `tests/conftest.py` `SLOW_MODULES`, per the original tiering doctrine
   (the hook/gate/scaffold runs exercise them anyway). Target: restore
   real headroom on this box (the slowest known dev machine) — the tier
   passes comfortably under 60 s warm, measured over ≥3 runs, stamped
   with the fig: convention. Re-stamp the membership ratchet and the
   seconds stamp deliberately with reasons.
2. **Enforce.** Only after (1) lands green: the commit bar names the
   seconds — wire `check_smoke_budget.py --mode enforce` beside the
   pytest smoke command (session-protocol skill §3, CLAUDE.md's bar
   sentence, and the pre-commit surface if the hook runs smoke), so a
   breach fails the bar where it is introduced instead of being reported
   green. Keep CI's enforce lane as-is.
3. **Words.** The session-protocol skill and CLAUDE.md state what the bar
   now promises (results AND seconds, enforced), replacing the current
   wording that lets a worker read "passed" over a failed budget — the
   defect OI-52 was minted for.

Known risk, stated by the ruling: a wall-clock assert on a loaded box reds
an honest commit — that is why the re-tier precedes enforcement and why
headroom (not budget-fitting) is the target. If after re-tiering the tier
still cannot clear 60 s with margin on this box, STOP and hand the finding
back to the owner rather than moving the budget or softening the mode.
