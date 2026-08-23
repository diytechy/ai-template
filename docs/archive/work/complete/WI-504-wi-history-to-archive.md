+++
id = "WI-504"
title = "Relocate terminal WI history under the archive: docs/work/{complete,cancelled,partial} move whole (OI-55 ruled (a), 2026-08-22)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed OI-55 (a) in full, in this one commit — readers taught first, then
the move, then the sweep, matching the ruled order:

- **Readers taught** (both roots read as ONE registry): `kitlib/registry.py`
  (`read_spec_rows` unions `docs/work/` and its new `spec_archive_dir`/
  `spec_roots` sibling — every consumer that funnels through it, `schedule.py`'s
  done-set, `check_trajectory.py`'s registry, `agent_common.py`, `intake.py`'s
  dedup/mint, inherited the fix with no call-site change); `check_trajectory.py`
  (`_head_spec_status_map`, `_staged_spec_registry` scan both `WI_WORK` and the
  new `WI_ARCHIVE_WORK`); `integrate.py` (`branch_outcomes` reads both prefixes
  with a per-prefix outcome-dir index; `docs/archive/work/` joined
  `_ADJUDICATION_SURFACES`); `intake.py` (new `_terminal_hits` helper backs
  `_closed_spec`, `_disposition_drafts`, `_cmd_sweep`; `next_wi_id` scans both
  roots); `check.py` (`docs/archive/work/*` joined the doc-navigability
  `--ignore` list). `kitlib/station.py` and `spec_move.py` needed NO change —
  `station.REPORTS` (`docs/handbacks/`) never nested under `docs/work/`, and
  `spec_move` is a generic `(src, dest)` mover with no hardcoded terminal
  destination.
- **Moved whole**: 495 files (472 `complete/`, 21 `cancelled/`, 1 `partial/` +
  its `.gitkeep`) via three directory-level `git mv`s, `docs/work/{complete,
  cancelled,partial}/` → `docs/archive/work/{complete,cancelled,partial}/`.
  Zero live disposition rows cited the pre-move paths in their `specref`
  (checked), so the "disposition keys update in the same commit" half of the
  ruling is a no-op for THIS population; the reader (`intake._closed_spec`) is
  taught for the next one regardless.
- **Link sweep**: 8 inbound docs re-pointed + 22 moved specs' own outbound
  links re-relativised, via `spec_move`'s own `_rebase_moved_spec_links` /
  `_relink_inbound_links` primitives run once over the precomputed remap.
  `check_docs.py --stale` with the exact `--ignore` set `check.py`'s
  doc-navigability step runs: 0 broken across 504 docs / 1315 links. Tombstone
  `README.md`s left in the three vacated `docs/work/` directories.
- **Scaffold surface**: `bootstrap.py` GITKEEP_DIRS, `orphans-allow.template`,
  `work/README.template.md`, `work/WI-000.template.md` updated so a FRESH
  scaffold ships the new shape directly (verified: bootstrapped a real
  scaffold under a temp dir, confirmed the directory listing, then hand-drove
  a scratch `WI-901` through claim → close into
  `docs/archive/work/complete/` on its branch — `read_spec_rows`,
  `branch_outcomes` and `finished_branches` all read it correctly with no
  further changes). `project-trajectory/RESYNC_PACK.md` carries the
  `[since d6818b0b]` entry with the one-command adopter migration recipe.
- **This row itself**: closed straight into the new home,
  `docs/archive/work/complete/` — the shape this WI just built.

Done-count invariant held: 472 done / 21 cancelled / 507 total, unchanged by
the move (`check_trajectory.py --strict` exit 0 before and after). Full
session record, file-by-file reader list and the driven figures:
[docs/log.d/2026-08-22-wi504-history-relocation.md](../../../log.d/2026-08-22-wi504-history-relocation.md).

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
