# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. Only what happens **next**
lives here; the spec/backlog and per-thread design history live in
[IMPROVEMENT_PLAN.md](../IMPROVEMENT_PLAN.md) (its thread `Status:` blocks and
WI-1.x log). The **gate-walk** record for the kit's self-adoption (Thread 47 —
sign-offs, verdicts) is [log.md](log.md).

- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) — this repo
  has no scaffolded `docs/process.md`; the masters are the reference.
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Bar:** `python -m pytest -q` and
  `python project-trajectory/scripts/check_docs.py --root . --stale` green
  before every commit — this repo's standing gate. **The kit's own
  `SN→SR→LLR→TC` spine is now being self-adopted** (Thread 47): `docs/gate`
  starts at G1; `trace.py --strict` / `check.py` join the bar as the spine fills
  (phases 3–6). Design history stays in the plan threads; the gate-walk record
  is `docs/log.md`.
- **Plan state:** Sessions L–S landed 2026-07-04 (Threads 29–40 complete);
  post-plan WI-1.19–1.30 landed since (latest: **WI-1.30**, 2026-07-05 —
  pre-push privacy review gains the declared `warn-unwired` opt-down for the
  adopted-but-not-wired-yet window; see the plan's WI log).
- **Open items:**
  - **Needs <human>**: _(none)_
  - **In flight:** _(none)_
  - **Deferred (backlog):** **WI-1.27** — coordinator working-tree stash/
    rollback on a hard-killed session (owner-deferred 2026-07-05: rely on
    fresh-session reconciliation; revisit only if pollution is observed).
- **Next action:** **Thread 47 (self-adoption) in progress** — phase 1 (layout:
  `docs/stack.ini`, `docs/gate` G1, the `docs/requirements/` + `docs/test/`
  registries, `docs/log.md`) + phase 2 (Stakeholder Needs) landed; phases 3–5
  (`SR → LLR → TC` decomposition) are next.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no `run.*` product launchers (the
  kit's "product" is `project-trajectory/` + `tests/` — nothing to double-click
  launch); no scaffolded `docs/process.md` (the masters live in
  `project-trajectory/`). *(The SN-spine non-goal was **lifted by Thread 47** —
  the kit now traces itself; its registries live in `docs/requirements/` +
  `docs/test/`, distinct from the shipped `project-trajectory/registries/`
  templates.)*
