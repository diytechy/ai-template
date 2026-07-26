# Specs-of-record (`docs/specs/`)

A **spec-of-record** is the durable, cross-session memory of an *open* work item:
what it must achieve and how you will know it is done. It is the bridge the
`SpecRef` column of [`work-items.csv`](../requirements/work-items.csv) points at
(process-options.md "Trajectory / work-items layer", rule **R-E**), and it exists
only while the WI is open.

Why it exists: a fresh agent session launches from repo text alone. A queued WI
whose only description is a one-line title is not implementable; a `SpecRef` that
resolves to a real spec here makes the next session start on solid footing —
and `check_trajectory.py` fails a gate when an open WI names no reachable spec.

## Shape

- **One file per standalone WI** — `docs/specs/WI-###.md` — **or** a shared
  **effort doc** with `#anchor`s when a batch of related WIs ships together
  (e.g. `docs/specs/my-effort.md#s1--first-slice`). A `SpecRef` is either a
  `path` or a `path#anchor`; the path part must exist in the repo.
- Every spec carries a **Done-when checklist** (see [`WI-000.md`](WI-000.md)).
  Sessions tick
  boxes as work lands, so a half-complete WI's frontier is its **first unticked
  box** — not prose discipline. Ticks are *transient working state*.

## Interface boundaries (§8 seams)

A spec whose WIs act **across a module boundary** carries an `Interfaces`
section citing each seam as an `IF-###` that resolves in
[`docs/requirements/interfaces.csv`](../requirements/interfaces.csv) — the one seam
home (`PROCESS.md §8`), so a spec never sketches its own near-duplicate. A
**new** seam is filed as a `Status=Proposed` row *at filing*, and the citation
names the **nearest existing** IF and why it falls short (the forced search is
the anti-duplication mechanism — search before you invent, never invent a seam
before a second consumer exists). Single-module WIs state that in one line and
cite nothing; the section arms only where §8 applies. `check_trajectory`
verifies the citations resolve and that a Proposed citation carries a rationale
(the full contract + the honest reviewer-tier gap: process-options.md
"Spec-of-record"). See [`WI-000.md`](WI-000.md) for the shape.

## Lifecycle

`open` (spec lives here, `SpecRef` resolves, WI named in
[`status.md`](../status.md)) → `done` (Deliverable filled with what shipped,
`SpecRef` cleared, spec **archived**).

**Archive at close, don't delete.** When a WI closes, move its spec to
`docs/archive/specs/` with the **close date appended** to the filename and the
**WI id it was attributed to** noted inside — future context, and no live plan
file can re-grow onto the working surface. A shared effort doc archives (date-
stamped, WI-attributed) when its **last** open WI closes. This close half is
**mechanized as rule R-F** (WI-251): `check_trajectory.py` flags a done WI
whose `SpecRef` is still set and a live spec here that no open WI cites —
WARN at the commit bar, ERROR under `--strict` (G2+). Verify durable content
reached its spine/architecture home *before* archiving; that judgment is the
reviewer's, not the checker's.

## What a spec is not

Not a second source of truth. The requirement lives in the `SN→SR→LLR→TC` spine;
the spec argues *how the work executes* and *when it is done*. Durable references
inside a spec are `WI-/SR-/LLR-/TC-` ids or in-repo paths — never session-local
codenames.
