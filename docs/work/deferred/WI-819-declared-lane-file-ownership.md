+++
id = "WI-819"
title = "Declared file ownership per lane: a lane changes only the paths its row owns"
workstream = "process"
specref = "docs/plans/2026-10-04-lanes-evaluation.md#taken-deferred-declared-file-ownership-per-lane"
needs = ["WI-808"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

DEFERRED by the owner's direction (2026-10-04: "Please add #1 but in deferred"),
from the evaluation of `thebpandey/lanes`
([plans/2026-10-04-lanes-evaluation.md](../../plans/2026-10-04-lanes-evaluation.md)).
There each brief names the paths a lane may change, and a deterministic check fails
the lane on any changed path outside them, or on uncommitted work, at review and
again at merge. The kit has no such check: a lane may touch any path, and scope
creep is caught only by a reviewer reading the diff.

It needs WI-808 (one landing per lane), because the landing is where the check
belongs: every lane passes it, by either path.

To settle when it is taken:

- **Where ownership is declared**, e.g. an `owns` list in the work-item spec
  (paths, a trailing `/` owning a directory).
- **What every lane may touch besides**: its own spec's moves, the declared
  generated set, its log fragment, its decisions record, its reviews, and the
  registries an adjudication sitting writes. The existing no-bar surface list
  (`integrate._ADJUDICATION_SURFACES`) is the precedent.
- **Whether `owns` is required on every row.** The owner's no-fallback rule
  points to required, with no unchecked mode beside it. Rows filed before it
  need a migration.
- **Overlap at dispatch**: whether two ready rows with overlapping ownership may
  run as parallel lanes (SN-027).

## Done-when

- Settled at the time it is taken, against the questions above. The sketch: a
  landing whose lane changed a path outside its row's ownership (plus the shared
  allowance), or that carries uncommitted work, is refused by name, and the
  refusal is tested for each case.
- Review bar: A. RESYNC_PACK: an entry (a new spec key; a migration if required).
