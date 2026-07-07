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
  `SN→SR→LLR→TC` spine is self-adopted** (Thread 47): `docs/gate` is at **G2** —
  `trace.py --strict` and `check.py --gate G2` now join the bar. Design history
  stays in the plan threads; the gate-walk record is `docs/log.md`.
- **Plan state:** Thread 47 phases 1–5 landed 2026-07-07 (self-adoption spine
  authored, meta-repo at **G2**: SN=22 SR=36 LLR=32 TC=36, 0 orphans); **Thread
  50** (trace.py SR/LLR citation-coherence integrity check) landed 2026-07-07;
  latest post-plan WI **WI-1.40**.
- **Open items:**
  - **Needs <human>**: **G1+G2 gate ratification** (`docs/gate-policy` =
    attended — the mechanical bar is met; the maintainer's attested sign-off in
    `docs/log.md` is outstanding).
  - **In flight:** _(none)_
  - **Deferred (backlog):** **Thread 51** — a first-class TC test-evidence
    column (surfaced by the Thread 47 dogfood; ruling pending). **WI-1.27** —
    coordinator working-tree stash/rollback on a hard-killed session
    (owner-deferred 2026-07-05: rely on fresh-session reconciliation).
- **Next action:** **Thread 47 phase 6** — the G3 walk: `--tier full` coverage
  with subprocess instrumentation (the `stack.ini` PROVISIONAL threshold),
  generated arch-map + `--check`, and meta-repo CI running `check.py` on itself;
  then phase 7 (thread back-pointers, mostly already seeded in SR `Rationale`).

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
