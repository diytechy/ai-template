## 2026-08-23 — WI-496: re-tier smoke for real headroom, then enforce the seconds

Executes OI-52's ruled (a) ENFORCE LOCALLY, with the owner's tuning mandate
(the 60 s budget is a worst-machine ceiling and its VALUE never moves), on
branch `requirements/ears-and-quality-characteristics`. The spec's ordering
is load-bearing and was followed in order: re-tier first, measure green,
only then wire enforcement.

**Load conditions, stated honestly:** this box had been running a serial WI
grind through the day (the memory that opened this session), so earlier
timing figures in this fragment's own basis material (54.9/64.0/55.7 s in
CLAUDE.md, 59.59/59.07/59.98 s in `check_smoke_budget.py`'s docstring) were
taken under some ambient load. This session's runs had the box to itself —
stated as a condition, not a universal, per the one-machine-humility rule.

**1. Re-tier — modules moved out of `smoke`, into `tests/conftest.py`
`SLOW_MODULES`, and why:**

| module | tests | serial cost | why (the doctrine boundary) |
|---|---|---|---|
| `test_external_frame` | 33 | 50.5 s | every finding case takes the `scaffold` fixture (a real `bootstrap.py` subprocess) plus `trace.py`/`check` subprocesses |
| `test_baseline_snapshot` | 40 | 31.3 s | `scaffold` plus repeated `trace.py`/`intake.py` `run_py` subprocesses |
| `test_selection_at_or_above` | 16 | 26.8 s | `scaffold` plus `derive_stage.py`/`check.py` subprocesses |
| `test_adjudicate_brief` | 48 | 24.9 s | real git repos with `agent_loop.py` driven as a subprocess — the same class as the already-slow `test_agent_loop_review` |
| `test_intake` | 26 | 23.5 s | a real `git init`/commit repo built per test — the same class as the already-slow `test_handback` |

These five summed to 157.0 s of the tier's 304.5 s total per-test duration
(51.5%) while the tier's wall clock sat at 0.98x budget — the same inversion
WI-281 first cut, regrown module by module over the past month while every
re-stamp measured only membership growth, never re-checked which class each
new module belonged to. All five are the SAME heavy class already filed in
`SLOW_MODULES` (subprocess-driving a real script over a real scaffold or
git repo, re-exercised wholesale at slice/phase close + CI) — nothing here
is deleted or weakened, and nothing was moved to buy budget without a
doctrine-matching reason: each module's fixture usage was read before it was
moved (`scaffold` fixture reference counts, git-repo-building helpers,
`agent_loop.py`/`trace.py`/`derive_stage.py` `run_py` calls), not inferred
from its runtime alone.

**Warm-run figures, ≥3 runs, this box (3.11.9, `-n auto`):**

- Before (this session's own baseline measurement): 1409 collected,
  `python -m pytest -q -n auto -m smoke --durations=0` → **58.77 s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke --durations=0" rev=0cfb2e6f-dirty -->
- After: **27.27 / 28.16 / 27.86 s**, 1270 collected (1265 passed, 5 skipped,
  identical across all three runs)
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=0cfb2e6f-dirty -->

~2.15x under the 60 s budget — real headroom, not a budget-fitting reading.
The STOP rule (re-tier that still cannot clear 60 s with margin) did NOT
fire.

**Ratchet/stamp re-stamps, `docs/stack.ini` `[smoke-budget]`:**

- `max-tests`: **1416 -> 1280** (measured 1270 collected at the re-stamp,
  +10 headroom — the same small-slack posture the file's prior eighteen
  stamps carried, not a freeze at current+1).
- `seconds`: **60, unchanged.** The ruling is explicit that the budget VALUE
  never moves in either direction; what changed is that the unchanged value
  now has real margin behind it instead of none. Full reasoning and fig:
  lines recorded in `docs/stack.ini` beside the new stamp (revision
  `0cfb2e6f-dirty` — this is a work-branch commit, so the stamp will read
  `-dirty` until it lands; the next re-stamp on this file inherits a clean
  revision the normal way).

**2. Enforce — wiring points, checked before assumed:**

- `project-trajectory/skills/session-protocol/SKILL.md` §3's command block
  now runs `python -m pytest -q -n auto -m smoke` then
  `python scripts/check_smoke_budget.py --mode enforce` then
  `check_docs.py --stale`, all three named as the commit bar. Edited at the
  ONE kit-master source, then fanned out with `bootstrap.py --sync --dest .`
  to `.claude/skills/session-protocol/SKILL.md` and
  `.agents/skills/session-protocol/SKILL.md` — `gen_skills_index.py
  --check-agents` confirms all three copies are byte-identical
  (`612a0909aa0bf3cf81d705038d4c4a07`).
- `CLAUDE.md`'s "Self-test before claiming done" bullet: same wiring, same
  wording change.
- The pre-commit hook surface (`project-trajectory/hooks/pre-commit`,
  wrapped by `.githooks/pre-commit`) was READ, not assumed: it runs no
  `pytest` at all — its floor is the freshness/integrity/format steps
  (`check.py --run-steps okf,trajectory-map,status-map,open-items,trajectory,
  registry-integrity,derived-stage,skills-sync,skills-index,prompt-catalog,
  ratify-fresh,ratify-immutable,staged-divergence`, `check_trajectory.py
  --staged`, `check_privacy.py` x2, `check.py --run-step format`). Nothing
  in that surface runs the smoke tier, so there was nothing to wire there.
  CI's enforce lane (`.github/workflows/test.yml`) is left as-is, per spec.

**3. Words.** Both wired locations now say the bar means results AND
seconds, both enforced (OI-52 ruling (a), 2026-08-23) — the command that
actually fails on a breach, replacing prose that let "passed" be read over a
failed budget — plus the fresh 27.27/28.16/27.86 s figures in place of the
stale 2026-08-11 (~17 s) and 2026-08-20 (54.9/64.0/55.7 s) readings.

**Byte-budget-guard, before/after (`wc -c`):**

- `CLAUDE.md`: 7513 -> 7831 (**+318**; cap 8500, 669 headroom left).
- `project-trajectory/skills/byte-budget-guard/SKILL.md` (+ its `.claude`/
  `.agents` copies, kept byte-identical): 4841 -> 4834 (**-7**; cap 5000) —
  re-stamped BOTH the CLAUDE.md row and its own self-referential row in the
  same edit.
- `project-trajectory/AGENTS.template.md`: unchanged (9980; not touched this
  session)
- `project-trajectory/PROCESS.md` / `PROCESS_OPTIONS.md`: unchanged (not
  touched)
- `project-trajectory/skills/session-protocol/SKILL.md` (+ its `.claude`/
  `.agents` copies, kept byte-identical): grew by the wording change; this
  skill carries no declared byte cap in the byte-budget-guard table (only
  `AGENTS.template.md`, `CLAUDE.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`, and
  the byte-budget-guard `SKILL.md` itself are budgeted) — noted, not skipped.

**Caught by the full-suite run, not by the commit-bar floor:** the first
`--mode enforce`-wiring pass edited `CLAUDE.md`'s byte count without
re-stamping the byte-budget-guard skill's own Budgets table — the smoke
tier (re-tiered) never runs `test_bootstrap.py`, and the commit-bar floor
(`check.py --run-steps ...`) never reads that table either, so the drift was
invisible until the full suite's `test_capped_doc_baselines_match_the_real_sizes`
caught it (`1 failed, 2898 passed, 14 skipped in 1024.85s`). Fixed in place
(the byte deltas above are the corrected, final state); this is exactly the
gate the WI's own "full suite owed" clause exists to catch, working as
designed.

**Other regenerated surfaces staged in the same commit:** `docs/open-items.html`
was found STALE by the pre-commit floor before any WI-496 edit (pre-existing,
confirmed by `git stash` + re-running `gen_open_items.py --check` against
trunk HEAD) — regenerated per "regenerate surfaces when the hook demands"
and staged here rather than left for a future session to trip over.

**Gate outputs:**

- Pre-commit floor (`check.py --run-steps ...`): all PASS after the
  `open-items.html` regen, the `PROJECT_STATE.html`/`docs/status.md` regen
  the WI's own close triggered, and staging (`staged-divergence` and
  `trajectory-map` were transient FAILs along the way, both cleared by
  regenerating and `git add`).
- `check_docs.py --root . --stale`: exit 0, hints only (no broken links, 1
  pre-existing orphan warning).
- `check_trajectory.py --root . --strict`: exit 0, "clean (507 work item(s),
  475 done (94%), 21 cancelled, graph acyclic)" — warnings only, none new.
- Smoke (re-tiered): see the after figures above — 1265 passed, 5 skipped,
  27-28 s.
- Full suite, run 1 (`--basetemp=D:/pytest-tmp-w496`, Git Bash on PATH for
  `sh.exe`): **1 failed, 2898 passed, 14 skipped in 1024.85s (0:17:04)** — the
  byte-budget-guard table drift caught above, fixed in place.
- Full suite, run 2 (`--basetemp=D:/pytest-tmp-w496b`), after the fix:
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:/pytest-tmp-w496b" rev=0cfb2e6f-dirty -->
  **2899 passed, 14 skipped in 1054.43s (0:17:34), exit 0.** Green.

**Deviations from spec:** none in substance. Two scope additions, both
mechanical and both demanded by the commit-bar floor rather than chosen:
regenerating `docs/open-items.html` (pre-existing staleness, predated this
session's edits) and `PROJECT_STATE.html`/`docs/status.md`'s GENERATED
STATUS block (staled by this WI's own close dropping out of the ready
frontier). Also: `byte-budget-guard`'s Budgets table needed a second pass —
the first edit re-stamped `CLAUDE.md`'s row but missed the skill's own
self-referential row, caught only by the full suite (see above), not by the
commit-bar floor or the smoke tier — recorded as a gap, not silently healed.

**Deferred open items: none** — OI-52 closes with this row; the STOP rule did
not fire, so there is no unresolved finding to hand back.
