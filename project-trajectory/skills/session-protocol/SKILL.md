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
next), **`docs/requirements/work-items.csv`** (the WI registry), and
**`docs/log.md`** (the session/gate record). This skill is the fast path; the
process masters (`PROCESS.md` / `PROCESS_OPTIONS.md`) win when they disagree. The
kit's design history — the old thread specs and the WI-1.x log — is archived at
`docs/archive/IMPROVEMENT_PLAN.md` (context, not a working surface).

## 1. Read before doing

- Read `CLAUDE.md` (governs editing the kit) and `AGENTS.md` (the pointer stub).
- Read `docs/status.md` (the working surface — what's next) and the scoped WI's
  row in `docs/requirements/work-items.csv`. The spec-of-record for a WI is what
  its row points at (an SR and/or a plan doc); older landed work is in the
  archived plan. **Do only the scoped work** — no unrelated edits.
- If a stub is being revived, find and link its earlier backlogged form (search
  `docs/archive/scratch.md` + the stub threads) so the resolution is traceable.
- **Check `git status` first.** Residue in the working tree is from an
  interrupted session; reconcile it against the open WI's spec / Done-when
  *before* new work — verify-and-commit what is complete, discard what is not
  part of the scope, and record which in the log. (The unattended loop surfaces
  this into the session prompt; the judgment is yours — it never auto-stashes.)

## 2. Respect the constraints

- **Byte budgets** on `AGENTS.template.md` (10,000) and `PROCESS.md` — see the
  `byte-budget-guard` skill. Push expansion to `PROCESS_OPTIONS.md` /
  `ADOPTING.md` / `EXAMPLE.md`.
- **Stdlib-only, cross-platform** kit scripts (Python 3.8+, Windows + POSIX).
- **Single source of truth:** state a fact once and link to it; don't paraphrase
  a rule into five files.

## 3. End green (gates)

Run the real checks and paste the real output — never a green you didn't produce:

```
python -m pytest -q -n auto -m smoke
python project-trajectory/scripts/check_docs.py --root . --stale
```

Both must pass before **each** commit — this is the **commit bar**. `-m smoke`
is the fast per-commit tier (WI-122: ~47 s / 531 cases vs ~66 s / 684 for the
full suite, both `-n auto` — the declared stack.ini command, WI-075). Tiering
is opt-out: smoke drops only the heavy end-to-end modules
(`tests/conftest.py` `SLOW_MODULES` — full hook/gate/scaffold runs the commit
hook and the gate re-exercise anyway), so a **new test is in the bar by
default**. Run the **full** unfiltered suite (`pytest -q -n auto`) before
claiming a slice/campaign done, at close, and after a broad script change. The
full `check.py --gate <gate>` is the **gate bar** (unfiltered suite + coverage):
it belongs to gate advancement, campaign close, and CI, not to each
mid-campaign slice; `--jobs 0` runs its independent steps concurrently. A per-WI
slice inside a campaign ends at the commit bar (PROCESS_OPTIONS.md, "Campaign
ruling"). New behavior needs new tests
(`tests/`); update `test_bootstrap.py` file lists and `README.md` kit-contents /
`bootstrap.py` `MAPPING` when the scaffold surface changes.

## 4. Record the work

- Set the WI's row in `docs/requirements/work-items.csv` to `done` with its
  deliverable, and add a session entry to `docs/log.md`: one-line summary,
  deliverables, **deviations from spec**, **byte deltas on budgeted files**, and
  the `pytest -q` totals (match the style already there).
- Update `docs/status.md` to point at what's next; don't leave a stale "next".
- Where the unattended coordinator is in use, maintain `docs/next-wi` (the next
  WI id) alongside `status.md`'s Next action, so a managed BUILD session honors
  that WI's `BuildTier` pin (process-options.md "Unattended operation").

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
