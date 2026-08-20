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

### Slice 2 landed 2026-08-20 — the CROSSING half. What remains, measured.

The lane stays ACTIVE. `docs/architecture.md` is gone (slice 1) and the
boundary/tie-back half is now done (slice 2); the SCHEMA half is not, and it is
blocked rather than merely unstarted.

**Landed this slice:** `B-01` and `B-04`'s hook-floor half given a facing
(`IF-134`/`IF-135` minted Drafted, owned by `LLR-019`/`LLR-020`); the five
untied `external:` rows adjudicated one at a time (`IF-080`/`IF-081` tied to
`B-05`; `IF-032`/`IF-036`/`IF-041` keep no tie-back, each with its own reason
recorded in the row); `B-02`'s deliberate non-realization restated in the
registry header with the `SR-140` condition; 22 `notes` cells swept of retired
`CMP-001..005` ids, three of which had become FALSE rather than stale; the
`migrate_carrier.py` one-shot framing corrected on `IF-103`, the kit README and
`RESYNC_PACK.md`. The unrealized-crossing advisory now reads `B-02` alone.

**Item CLOSED by measurement, not by work — the one live derivability fire.**
`IF-128`'s owner-vs-endpoint disagreement is GONE, and it was closed by the
2026-08-17 re-point of its owner to `LLR-166` rather than by anything this lane
did. Verified as a real clear and not a skip: the row is `Consumes`, so its
owner-side column is `counterpart` (`scripts/spine_carrier`), and `LLR-166`'s
`module` is that module — they agree by construction, not by falling out of the
predicate. `docs/test/report.md` reads *"None. Every LLR-owned row's owner-side
endpoint agrees with its owner's Module."* Nothing is owed here.

**STILL OWED, and the first two are BLOCKED behind `WI-469` by a recorded
ordering, not by preference:**

1. **The `direction`/`this_project` shed and the counterpart→consumers
   transform.** `WI-469` re-authors the 27 SR-owned file-as-endpoint `Consumes`
   rows; its scope states the column drop *"follows this WI, never precedes
   it"*, and the `~WI-469` soft edge encodes exactly that. A second, separate
   blocker is UNRULED and is the owner's: which reading of `owner` governs a
   `Consumes` row — the-module-that-holds-the-code, or the provider — leaves
   ~20 rows unpointed either way, and the shed cannot be designed until it is
   settled.
2. **The 49 held `Contract`-cell provenance citations.** Re-measured this
   session and UNCHANGED at exactly 49 (46 `Contract names WI-###` + 3
   `Contract cites decision`). The hold and its `WI-469` blocker are recorded in
   `docs/provenance-allow`'s header, which stays the surface to re-open if the
   chain outlives this lane. Two retired `CMP-00x` ids survive inside `IF-056`'s
   and `IF-077`'s held clauses; they were deliberately left, because the whole
   sentence carrying them is what the hold's pass deletes, and correcting a
   number inside a sentence already scheduled for removal is two passes for one
   fix.
3. **The `external.toml` context view** — entities/crossings/relationships
   rendered into the dashboard. The spec's own *"may land as its own slice"*,
   still unbuilt, and not blocked by anything.

**Queued for the owner rather than decided here** (both minted this slice):
`OI-49` — what the sitting is actually being asked to ratify from the 2026-08-15
interface rework, given that 10 of its 21 judgement picks have since been
re-picked onto the design tier, 2 were recorded with no reason, and the
`carried_by` prototype has been generalised to three carriers past its own
"prove it on one seam first" precondition. `OI-50` — the locked frame names no
party for a vendored upstream source, so `IF-036` has an external endpoint and
no crossing to tie back to.

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
