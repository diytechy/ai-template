# Project Status — Blackboard

The **working surface** for the gated process (see [process.md](process.md)):
this whole file holds only what the agent or human must perform **next**. Keep
every section short and current; history — sign-offs, verdicts, ratified
decisions, session notes — appends to the log this header points at, never here.

- **History:** [log.md](log.md) _(append-only; see process.md §5)_
- **Work plan:** [plan.md](plan.md) _(the sequenced session blocks the
  plan/build cadence executes; the "Next action" below names the current
  block — see process-options.md "Plan/build cadence")_
- **Parallel tracks?** _(single-lane by default — ignore this line.)_ Under the
  multi-lane layer (process-options.md "Parallel tracks") this file becomes the
  **cross-track dispatcher** (a one-row-per-track roll-up, integrator-written)
  while each track keeps its own `docs/tracks/<track>/status.md`.
- **Work items?** _(off unless you adopted the trajectory layer — ignore this
  line.)_ With the trajectory/work-items layer (process-options.md "Trajectory /
  work-items layer") the **Next action** below names the next `WI-###`(s) from
  `docs/requirements/work-items.csv`, and `docs/trajectory.html` renders the DAG.

---

## Current State

- **Active gate:** G1 — Requirements, UX & constraints _(mirror it in the
  one-line `docs/gate` file — `check.py`/CI read that; see process.md §7)_
- **Round:** 1
- **Open items:** _(the few things blocking the current gate — **one bullet per
  item, never inline-enumerated prose**. Give each a stable short id (OI-1,
  OI-2, … — ids are never renumbered; closed items are removed or struck
  through) so a human can cite it from memory; add an optional `blocks:` clause
  naming what the item holds up (a gate, a TC — omit it when nothing waits);
  end every bullet with a link to the artifact it concerns; keep the two
  sub-lists below. Any deferrals/decisions list follows the same bullet
  discipline.)_
  - **Needs <human>** _(state the decision wanted, per item)_:
    - OI-1 — decide: keep or drop the legacy export flag (blocks: G1) →
      [system-requirements.csv](requirements/system-requirements.csv)
  - **In flight** _(driver; no approval needed)_:
    - OI-2 — pinning SR-000's acceptance predicate →
      [system-requirements.csv](requirements/system-requirements.csv)
- **Assumptions (unattended):** _(decisions taken without sign-off while running
  unattended — each to confirm or revert at the next gate; see AGENTS.md "Ask,
  don't assume". Once ratified, move the entry to the log's Decisions log.)_
- **Next action:** _(what happens next + who must approve)_

## Scope (restated from the brief)

- **Goal:**
- **Stakeholders / end user(s):** _(who or what the system serves — humans,
  operators, or another system, represented by its owner)_
- **Active hats:** Stakeholder, UX/Docs, System Engineer, Software Engineer, Test
  Engineer _(+ any domain hats this scope needs, e.g. Network / Security / Data /
  Hardware — see process.md §1)_
- **Supported platforms:** _(Linux / macOS / Windows — drives which setup/check
  launchers must exist)_
- **Constraints:**
- **Non-goals:**
- **Definition of done:**
