# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. Only what happens **next**
lives here; the spec/backlog and per-thread history live in
[IMPROVEMENT_PLAN.md](../IMPROVEMENT_PLAN.md) (its thread `Status:` blocks and
WI-1.x log are this repo's append-only history layer — the `log.md` role).

- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) — this repo
  has no scaffolded `docs/process.md`; the masters are the reference.
- **Working rules:** [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill.

---

## Current State

- **Bar:** `python -m pytest -q` and
  `python project-trajectory/scripts/check_docs.py --root .` green before
  every commit — this repo's gate. The SN→SR→LLR→TC spine is deliberately not
  applied here: the meta-repo's product is the templates, and its
  requirements live as plan threads (see CLAUDE.md).
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
- **Next action:** awaiting new scope — it enters the plan as WI-1.x log
  entries (never worked unscoped — see the `session-protocol` skill).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.8+.
- **Non-goals (self-application boundary):** no registries/SN-spine for the
  meta-repo itself; no `run.*` product launchers (the kit's "product" is the
  templates — there is nothing to launch); no scaffolded `docs/process.md`
  (the masters live in `project-trajectory/`).
