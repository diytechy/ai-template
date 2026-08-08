---
name: session-protocol
description: Use when running a work-item (WI) or thread session in this template repo — how to read the plan, execute only the scoped work, pass the gates, write the session/WI log, and commit in this repo's style.
stacks: [any]
domains: [any]
phases: [dev, gate, release]
tags: [session, improvement-plan, workflow, commit-style, wi]
scope: this-repo
---

# Session protocol (this template repo)

How a WI/thread session runs here. The live homes: **`docs/status.md`** (what's
next), **`docs/work/`** (the WI registry — one spec file per item, status = its
directory), and
**`docs/log.md`** (the session/gate record). This skill is the fast path; the
process masters (`PROCESS.md` / `PROCESS_OPTIONS.md`) win when they disagree. The
kit's design history — the old thread specs and the WI-1.x log — is archived at
`docs/archive/IMPROVEMENT_PLAN.md` (context, not a working surface).

## 1. Read before doing

- Read `CLAUDE.md` (governs editing the kit) and `AGENTS.md` (the pointer stub).
- Read `docs/status.md` (the working surface — what's next) and the scoped WI's
  spec file under `docs/work/` (its directory is its status). The
  spec-of-record for a WI is what its `specref` points at (an SR and/or a plan doc); older landed work is in the
  archived plan. **Do only the scoped work** — no unrelated edits.
- If a stub is being revived, find and link its earlier backlogged form (search
  `docs/archive/scratch.md` + the stub threads) so the resolution is traceable.
- **Check `git status` first.** Residue in the working tree is from an
  interrupted session; reconcile it against the open WI's spec / Done-when
  *before* new work — verify-and-commit what is complete, discard what is not
  part of the scope, and record which in the log. (The unattended loop surfaces
  this into the session prompt; the judgment is yours — it never auto-stashes.)
- **Treat a declared-policy change as a status-staleness event.** In the same
  sitting, grep `docs/status.md` for pause/stop/approval
  language predicated on the old ratification-boundary, `policy.push`,
  `policy.review_rounds` or `policy.guardrails` value; point to the declared key
  in `docs/config.toml` instead of paraphrasing it.

## 2. Respect the constraints

- **Byte budgets** on `AGENTS.template.md` (10,000) and `PROCESS.md` — see the
  `byte-budget-guard` skill. Push expansion to `PROCESS_OPTIONS.md` /
  `ADOPTING.md` / `EXAMPLE.md`.
- **Stdlib-only, cross-platform** kit scripts (Python 3.11+, Windows + POSIX).
- **Single source of truth:** state a fact once and link to it; don't paraphrase
  a rule into five files.

## 3. End green (gates)

Run the real checks and paste the real output — never a green you didn't produce:

```
python -m pytest -q -n auto -m smoke
python project-trajectory/scripts/check_docs.py --root . --stale
```

Both must pass before **each** commit — this is the **commit bar**. `-m smoke`
is the fast per-commit tier, re-tiered to a **budget** by WI-281: it must run
**≤ 60 s** wall (measured 2026-07-23 on a 24-core box: ~7 s / 349 tests vs
~4.2 min / ~1380 for the full suite, both `-n auto`) so it stays a real smoke
test — "is it basically alive?", not a re-run of most of the suite. Tiering is
opt-out: smoke drops the **subprocess/scaffold-heavy** modules
(`tests/conftest.py` `SLOW_MODULES` — the hook/gate/scaffold/heavy-script runs
the commit hook and the gate re-exercise anyway), so a **new (in-process) test
is in the bar by default**. The runtime is its own budget item — declared
seconds + a deterministic membership ratchet — in `docs/stack.ini`
`[smoke-budget]` + `tests/test_smoke_budget.py` (it bites if the tier grows back
toward the full suite; re-stamp deliberately, reason in the log). Run the
**full** unfiltered suite (`pytest -q -n auto`) before claiming a slice/phase
done, at close, and after a broad script change. The
full `check.py --gate <gate>` is the **gate bar** (unfiltered suite + coverage):
it belongs to gate advancement, phase close, and CI, not to each
mid-phase slice; `--jobs 0` runs its independent steps concurrently. A per-WI
slice inside a phase ends at the commit bar (PROCESS_OPTIONS.md, "Phase
cadence"). New behavior needs new tests
(`tests/`); update `test_bootstrap.py` file lists and `README.md` kit-contents /
`bootstrap.py` `MAPPING` when the scaffold surface changes.

## 4. Record the work

- Close the WI by MOVING its spec file to the terminal directory its outcome
  names — `docs/work/complete/` when it shipped, `docs/work/cancelled/` when it
  never will — and filling
  its `## Deliverable` body (status is the directory, never a field), and
  record a session entry for `docs/log.md`: one-line summary, deliverables,
  **deviations from spec**, **byte deltas on budgeted files**, and the
  `pytest -q` totals (match the style already there). A **driven figure** in
  the fragment/Deliverable — a total, a census count, a timing — follows the
  declared-figure convention (process-options.md "Signed measurements",
  WI-392): its line carries the producing command + revision (or its
  derivation) under the `fig:` marker, held to presence by
  `check_figures.py`. **Where it goes:** on
  the serial trunk lane, append to `docs/log.md` directly; on a work branch,
  write it as a fragment `docs/log.d/<WI-id>-<slug>.md` (starting with its
  `## <YYYY-MM-DD> — <title>` heading; links authored relative to
  `docs/log.d/`) — `trunk_step.py` compiles fragments into the log in merge
  order and deletes them. Never hand-edit `docs/log.md` on a work branch.
- **Order the close against the verdict round.** Under `policy.review_rounds >= 1` the
  merge queue wants the APPROVE no older than the branch's last **non-record**
  commit (`docs/reviews/` + `docs/log.d/` are excluded; `docs/work/` is not), so
  anything committed after it buys another round. Close **first** — Deliverable
  filled, spec moved to its terminal folder, any ratifying Status-change commit
  — and take the final verdict round **last**; never hand-merge trunk, since
  only the station's `refresh` commit is peeled. A correction the verdict itself
  demanded still costs a round: that is the gate working, not a defect
  (process-options.md, "The LLM-gate verdict protocol").
- Update `docs/status.md` to point at what's next; don't leave a stale "next".
- WI ordering is derived from the registry by `schedule.py` (the DAG +
  `Priority` + gate class), not a hand-curated `docs/next-wi` — that pointer
  is retired (WI-180; process-options.md "Unattended operation"). When
  filing or triaging a WI, set `BuildTier` deliberately: `quick` for mechanical,
  off-spine work; `medium` by default; `strong` only for design-shaping or
  spine-touching changes — the worker session reads it from the WI row. Do
  not silently downgrade a declared route mid-loop.

## 5. Commit in this repo's style

- **Logical commits** — one per deliverable/thread, message
  `WI-<n>: <imperative subject>` then a body explaining the *why* and any
  deviation (see recent `git log`).
- **Attribution footers are fine here** — add `Co-Authored-By:` as usual (this
  repo is not anonymous). Omit them only in a privacy-restricted / anonymous repo,
  where a tool trailer is itself a leak (process-options.md "Commit identity &
  privacy").
- **Do not push** unless explicitly asked; branch is whatever the plan header's
  **Branch:** line names.
