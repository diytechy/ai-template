+++
id = "WI-504"
title = "Relocate terminal WI history under the archive: docs/work/{complete,cancelled,partial} move whole (OI-55 ruled (a), 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-55"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-55 (a): the ~480 terminal specs leave the active workspace so
agents stop wading through history to find the frontier. The ruled shape:

1. **Teach the readers FIRST** — the registry reader (kitlib/registry +
   check_trajectory), spec_move's destinations, station.py's OUTCOME_DIRS,
   the R-A/R-F close rules, the scheduler's done-set — both roots valid
   during the move commit; new home docs/archive/work/{complete,cancelled,
   partial}/ (status stays directory, just under archive).
2. **Move whole**, one reviewed relocation; `partial/` handback reports
   move WITH their specs and the disposition keys update in the same
   commit.
3. **The link sweep** across committed docs, held to check_docs' 0-broken
   bar; tombstone READMEs in the old terminal directories.
4. Historical commits keep citing old paths — records, acceptable.

Scaffold surface: bootstrap ships docs/work/ skeleton — update MAPPING/
templates so a fresh scaffold gets the new shape; RESYNC entry (adopters
migrate with a one-command move + sweep recipe). Verify by BOOTSTRAPPING A
REAL SCAFFOLD and by running the full close machinery once against the new
home (a scratch WI moved through claim→close in a scaffold).
