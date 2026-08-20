+++
id = "WI-455"
title = "The docs/architecture.md RETIREMENT program (owner-ruled 2026-08-13u, sitting-2 decision 8): 'architecture.md can die — instead the available tables should produce full architecture in ProjectState.html.' This is a program, not a delete: TEN kit scripts touch the file (gen_arch_map, traj_parse, gen_trajectory, check_trajectory, check.py, traj_status, trunk_step, check_flows, check_doc_refs, bootstrap — plus gen_okf, traj_views and ~34 test files), and the data path registries -> gen_arch_map -> architecture.md -> traj_parse -> dashboard must become registries -> dashboard directly (the 'How (SW architecture)' tab already renders the map — extend, don't rebuild). Three things 13u refused to let lapse silently, each an explicit deliverable: (1) check_flows.py loses its input — the Runtime flows are narrative, SR-cited and NOT registry-derivable; move them into the dashboard as authored-and-checked content (the check follows them) or retire the obligation with a recorded ruling — never by the file's deletion (check_flows is named by 2 live SRs). (2) bootstrap.py's MAPPING and the scaffold surface change (ARCHITECTURE.template.md scaffolds today) — downstream-visible, owes a resync-pack entry, and is only verified by bootstrapping a real scaffold. (3) A disposition for each of the file's ~192 hand-authored lines (intro, Shape of the product, Runtime flows) — derived, moved, or retired, stated per block. Registry citations to the path (interfaces.toml, open-items.toml, low-level-requirements.toml) and process-doc references (PROCESS.md x7, PROCESS_OPTIONS, AGENTS.template.md x2 — byte-budgeted, must land net-zero, and the stale baselines must be reconciled first) re-point with the change that lands, not before. SEQUENCING: collides with WI-390 clause (2) (arch-map/Contracts declarations) and WI-448 (MAPPING) — sequence against both or the three programs fight over gen_arch_map; the generated-context-view half (entities/BIF/relationships rendered from external.toml) depends on the schema row and may land as its own slice. The boundary record itself (SN-040's 'kept with the architecture') is SATISFIED by the derived view — that was decision 8's point — so this program is also what closes sitting-2 decision 8's execution."
specref = "docs/plans/2026-08-13-sitting-2-boundary-and-context.md#decision-8--where-the-boundary-record-lives-once-ruled"
workstream = "process"
sr_refs = []
needs = ["~WI-442", "~WI-469"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

### Frontier reconciliation (2026-08-19, repo-review triage)

- **The `~WI-469` soft edge encodes an ordering that already ruled.** WI-469's
  own scope states "the wi455 column drop … follows this WI, never precedes
  it"; until now that ordering lived in WI-469's prose only, with no edge in
  either direction. The edge is soft because only the column-drop slice waits —
  the lane's other work does not.
- **The `gen_arch_map`/MAPPING collision set grew.** The title's SEQUENCING
  clause names WI-390 clause (2) and WI-448; the 2026-08-19 review triage
  minted WI-483 (the core decomposition program), which contests the same
  module and the same MAPPING line. Four programs now touch it — read all
  four before any slice that moves `gen_arch_map`.
- **The 49 held `Contract`-cell provenance citations ride this lane** (OI-36
  ruled 2026-08-19): the hold and its WI-469 blocker chain are recorded in
  `docs/provenance-allow`'s header, which is the surface to re-open if the
  chain outlives the lane.
