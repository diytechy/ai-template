# Work Plan — Session Blocks

> **Skip (or delete) this file if the trajectory / work-items layer is
> enabled** — a WI row + its spec-of-record supersede it
> (process-options.md "Trajectory / work-items layer"). It serves the
> zero-tooling rung: no registries, attended sessions, pure markdown.

The **sequenced block list** the plan/build cadence runs on (see
[process-options.md](process-options.md) "Unattended operation" → *Plan/build
cadence*): a **PLAN** session (strong tier) writes or repairs this list; each
**BUILD** session (cheaper tier) executes the next `pending` block — and only
it. [status.md](status.md) stays the lean resume surface and points here; this
file is the compressed hand-off between the two, so a build session reloads a
*spec*, not the exploration that produced it.

Discipline (same bullet rules as status.md Open items):

- One block per bullet; stable ids (`B-1`, `B-2`, … — never renumbered).
  Finished blocks flip to `done` (or are pruned once logged in log.md) —
  history lives in [log.md](log.md), never here.
- A block = **one coherent deliverable + its tests**, sized for one session.
  Sizing heuristics and the too-big/too-small smells: process-options.md
  *Plan/build cadence*.
- Every block states an observable **done-when** (the §4 honest-gate rule in
  miniature — "block done" must be checkable, not felt).
- A BUILD session that finds this list exhausted — or *wrong* (route it as a
  finding, don't silently rework) — re-chunks it on the strong tier before
  continuing (re-planning belongs on the strong tier).

## Blocks

<!-- Example block — replace with your first real one. Fields:
     status: pending | in-flight | done      size: S | M | L
     tier: the §6 model-tier hint (strong | cheap — advisory, never enforced) -->

- **B-1** `pending` (size M, tier cheap) — Implement the CSV export behind
  `SR-000`'s acceptance predicate.
  **Scope:** `src/export.py` (new), `LLR-000`, `TC-000`.
  **Done-when:** `TC-000` passes in the smoke tier; `scripts/check.py --stage DevStg-Tests`
  green.

## Notes for the next PLAN session

_(Optional: what the last BUILD sessions learned that should reshape the next
chunking — e.g. "sessions 004–006 each finished trivially, coarsen"; read the
recent `iteration_index.md` rows before re-chunking.)_
