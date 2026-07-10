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

How a WI/thread session runs here. The authority is
`IMPROVEMENT_PLAN.md` — its **"Session protocol"** and **"Post-plan work items
log (WI-1.x)"** sections. This skill is the fast path; when they disagree, the
plan wins.

## 1. Read before doing

- Read `AGENTS.md` (governs editing the kit) and `AGENTS.md` (the pointer stub).
- Open `IMPROVEMENT_PLAN.md`. Find the relevant thread section (its
  Goal/Steps/Tests/Risks/Done-when **is** the spec) or, for new post-plan scope,
  the WI-1.x log. **Do only the scoped work** — no unrelated edits.
- If a stub is being revived, find and link its earlier backlogged form (search
  `docs/archive/scratch.md` + the stub threads) so the resolution is traceable.

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
python -m pytest -q
python project-trajectory/scripts/check_docs.py --root . --stale
```

Both must pass before **each** commit. New behavior needs new tests
(`tests/`); update `test_bootstrap.py` file lists and `README.md` kit-contents /
`bootstrap.py` `MAPPING` when the scaffold surface changes.

## 4. Record the work

- Add a `Status: ✅ landed <date>` block to a finished thread, or a WI-1.x log
  entry, matching the style already in `IMPROVEMENT_PLAN.md`: one-line summary,
  deliverables, **deviations from spec**, **byte deltas on budgeted files**, and
  the `pytest -q` totals.
- Move the ▶ NEXT session marker if the plan uses one; don't invent one.

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
