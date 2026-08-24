+++
id = "WI-455"
title = "The docs/architecture.md RETIREMENT program (owner-ruled 2026-08-13u, sitting-2 decision 8): 'architecture.md can die — instead the available tables should produce full architecture in ProjectState.html.' This is a program, not a delete: TEN kit scripts touch the file (gen_arch_map, traj_parse, gen_trajectory, check_trajectory, check.py, traj_status, trunk_step, check_flows, check_doc_refs, bootstrap — plus gen_okf, traj_views and ~34 test files), and the data path registries -> gen_arch_map -> architecture.md -> traj_parse -> dashboard must become registries -> dashboard directly (the 'How (SW architecture)' tab already renders the map — extend, don't rebuild). Three things 13u refused to let lapse silently, each an explicit deliverable: (1) check_flows.py loses its input — the Runtime flows are narrative, SR-cited and NOT registry-derivable; move them into the dashboard as authored-and-checked content (the check follows them) or retire the obligation with a recorded ruling — never by the file's deletion (check_flows is named by 2 live SRs). (2) bootstrap.py's MAPPING and the scaffold surface change (ARCHITECTURE.template.md scaffolds today) — downstream-visible, owes a resync-pack entry, and is only verified by bootstrapping a real scaffold. (3) A disposition for each of the file's ~192 hand-authored lines (intro, Shape of the product, Runtime flows) — derived, moved, or retired, stated per block. Registry citations to the path (interfaces.toml, open-items.toml, low-level-requirements.toml) and process-doc references (PROCESS.md x7, PROCESS_OPTIONS, AGENTS.template.md x2 — byte-budgeted, must land net-zero, and the stale baselines must be reconciled first) re-point with the change that lands, not before. SEQUENCING: collides with WI-390 clause (2) (arch-map/Contracts declarations) and WI-448 (MAPPING) — sequence against both or the three programs fight over gen_arch_map; the generated-context-view half (entities/BIF/relationships rendered from external.toml) depends on the schema row and may land as its own slice. The boundary record itself (SN-040's 'kept with the architecture') is SATISFIED by the derived view — that was decision 8's point — so this program is also what closes sitting-2 decision 8's execution."
specref = ""
workstream = "process"
sr_refs = ["SR-162"]
needs = ["~WI-442", "~WI-469"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

`docs/architecture.md` is gone and the architecture it carried is DERIVED — the
data path is `registries -> dashboard`, with no markdown way-station — and the
interface registry that path reads now states a seam the way the dashboard draws
it: `provider -> consumers`, with no direction column and no cell restating what
the owner already says.

**The three deliverables 13u refused to let lapse silently, each dispositioned.**

1. **`check_flows.py`'s input** — the Runtime flows moved VERBATIM to
   [`../../../runtime-flows.md`](../../../runtime-flows.md) and the checker
   followed them there, so `SR-013`'s obligation never lapsed; the dashboard's
   How tab embeds the authored flows, and `RUNTIME_FLOWS.template.md` scaffolds
   the home downstream (slice 1).
2. **`bootstrap.py`'s MAPPING and the scaffold surface** —
   `ARCHITECTURE.template.md` deleted, the MAPPING row and the whole `arch-map`
   harness step retired, `[arch-map] mode` re-purposed as the AST-inventory
   dial, and the `RESYNC_PACK.md` entry written. VERIFIED by bootstrapping a
   real scaffold, twice, not by reading the mapping (slice 1).
3. **A disposition per hand-authored block** — the ~192 lines answered
   block-by-block (derived / moved / retired) in the slice-1 log's table, which
   is the record of what happened to each one.

**And the schema half the program owed, in six slices.** The crossing/tie-back
adjudication and the endpoint-marker sweep (slice 2); `SR-162`'s decomposition
into `LLR-187` + `TC-182` (slice 3); the 48 held `Contract`-cell provenance
citations swept to zero, `OI-36`'s hold recorded as expired-and-executed (slice
4); the `external.toml` context view derived into the dashboard, which IS the
boundary record `SN-040` kept "with the architecture" and what closes sitting-2
decision 8's execution (slice 5); `OI-60` ruled (a) with the twelve-row owner
report shipped and the shed HELD on a measurement (slice 6); and the rename +
shed themselves (slice 7).

**The end-state schema, as landed.** Three cells became two on all 135 rows:
`direction` DIED (flow is the shape of the row), `this_project` and
`counterpart` became `provider` (a single endpoint) and `consumers` (a list),
per class — carrier, medium, consumer-class and reader-set rows each handled by
their own recorded reading rather than by one transform. `provider` is then
absent on the 85 rows where `owner -> LLR -> module` derives it UNIQUELY, states
the fact on the 29 where it cannot (a requirement owner, a multi-module owner, a
file or `external:` provider), and is legitimately unstated on the 21
published-medium rows that never recorded one. The derivations ship as tests
(`tests/test_seam_resolution.py`), not as a claim; the readers resolve a seam
through ONE home (`kitlib.spine.seam_provider`/`seam_consumers`); and
`trace_text.if_provider_advisories` — the countdown that used to say "this cell
is on its way out" — now holds the state it counted down to.

**What this lane deliberately did NOT do.** Re-pointing the twelve
requirement-owned provider-side rows onto the design tier is an owner-informed
judgement per seam, fed by
[`../../../plans/2026-08-23-sr-owned-provides-report.md`](../../../plans/2026-08-23-sr-owned-provides-report.md);
the advisory above is its executable half, and it asks for each cell back as its
owner is re-pointed. Recording a medium as the provider on the 21 rows that
state none is authoring, per row, not a rename. Neither is owed by this program.

## Context

### Slice 6, 2026-08-23 — `OI-60` is RULED (a); item 1's two free corrections land, the `direction` shed is held on a second measurement, and the twelve-row report ships.

The lane stays ACTIVE and still holds exactly one thing — item 1 — but it is no
longer BLOCKED. `OI-60` is ruled (a) (owner, in session), so what remains needs no
further owner act: **the counterpart-to-consumers rename, then the `direction`
shed immediately behind it.** Both are agent-executable now. The lane does NOT
close.

**Landed.** The two free corrections (a)'s ruling folded in: `IF-031`'s owner
moved `LLR-014` → `SR-015` — the one row in 135 authored under the reading that
was not ruled, re-pointed to the requirement stating the consumed medium's own
invariant, with the cost of the move stated on the row — and the ruled
owner-as-provider reading written into `interfaces.toml`'s header where an author
meets it rather than in a log they must find. The header's `direction` block also
loses a false claim it had carried: `_declared_seam_pairs` does NOT read the
column (it stores every endpoint pair both ways), so the column's live reader set
is three, not two — `interface_findings`' producer/consumer credit, `traj_views`'
seam arrows, `gen_arch_map`'s dotted edges.

**HELD, measured before any cell was touched — the `direction` shed.** The ruling
expected the shed to land today on the premise that "its two readers derive the
same fact from owner-side versus consumer-side". Measured: `direction` is
derivable from `owner`→`module` on **90 of 91** design-owned rows (`IF-031` the
lone disagreement, and the correction above resolves it) and on **0 of 44**
requirement-owned rows — a requirement carries no module, which is `OI-60`'s own
finding applied to the other column. Deleting it today loses 44 rows' orientation
and silently reverses the 32 requirement-owned `Consumes` seams in all three
readers. The premise becomes true only AFTER (a)'s other clause: once
`counterpart` is a consumers list, this side is the provider on every row and the
fact is free. **(a)'s two clauses are ordered, not parallel** — rename first, shed
second — so the destructive half was not run without the enabling half, and
nothing was normalized to make the column look shed-able. A third measurement
lands with it: 19 `Consumes` rows name an `external:` counterpart (16 the
downstream adopter), where the cell reads as what the FAR side does — so the
surviving column is not one fact across the population either.

**Shipped: the owner's decision surface.**
[`docs/plans/2026-08-23-sr-owned-provides-report.md`](../../../plans/2026-08-23-sr-owned-provides-report.md)
— all twelve rows in prose, each with its contract, provider module, consumers,
owner SR's full requirement text and rationale, the candidate design rows in that
module (3–15 each), and what a re-point would decide. Its finding: four rows are
adopter-facing (`IF-013`/`IF-014`/`IF-015`/`IF-081`), where SR ownership is
arguably CORRECT rather than a fallback; eight are internal, of which three are
ordinary re-points and two are entangled with their module's own open
decomposition question. The `WI-495` dossier's KEEP reads on `IF-013`/`IF-044`
stand and are cross-referenced. A second population is named so it is not
discovered later: **32 requirement-owned `Consumes` rows** have the same gap and
will need the same judgement when the rename runs.

**Item 1 below stays OWED — unblocked, scoped, and next.**

### Slice 5, 2026-08-23 — item 3 CLOSES: the `external.toml` context view lands. The lane's ONLY remainder is item 1, blocked on `OI-60`.

The lane stays ACTIVE, and it now holds exactly one thing. The depth-0 frame is
DERIVED into `PROJECT_STATE.html`'s architecture tab, above the module map:
parties, crossings, relationships, the realizing `IF-###` rows joined from
`interfaces.toml`, and the adjudicated no-tie-back rows with their recorded
reasons. That derived view IS the boundary record `SN-040` kept "with the
architecture" — sitting-2 decision 8's own point, and the clause that let
`docs/architecture.md` be retired in slice 1. **Decision 8's execution is
therefore complete**; what is left of this program is the column shed, which
decision 8 never asked for.

Three rendering decisions worth the record. Realization is **joined**, never
read off the frame row — the frame is LOCKED and a realization is the other
side's claim. An **unrealized** crossing (`B-02`) draws dashed and says so
rather than being hidden; its `SR-140` reason is left in the registry header
where the ruling lives, not restated in the view. The three **adjudicated
absences** from slice 2 (`IF-032`, `IF-036`, `IF-041`) render with the whole
reason each row records, and slice 2's two tie-backs (`IF-080`, `IF-081`) now
appear in `B-05`'s realizing set — the view is checked against the registry by
test, so a frame silently shorter than the registry reds.

Two things the slice was not scoped for and did anyway, both forced: the
renderer is a **new shipped module** (`traj_context.py`) because folding it into
`traj_views.py` pushed that module past the 1,500-line decomposition ratchet,
whose rule is decompose-never-bump; and that made this a **scaffold-surface
change** (bootstrap MAPPING, the test file list, the kit README, a
`RESYNC_PACK.md` entry), verified by bootstrapping a real scaffold rather than
by reading the mapping. Spine acts: `LLR-200` + `TC-196`, both minted `Drafted`.

**Item 3 below is STRUCK.** Item 1 stays blocked on `OI-60` (pending, the
owner's) and on nothing else. The lane is deliberately NOT closed: it holds
item 1 until that ruling lands.

### Slice 4, 2026-08-23 — item 2 CLOSES: the held `Contract` citations are swept and the hold expires.

The lane stays ACTIVE on items 1 and 3. `OI-36` (ruled 2026-08-19, option (b))
held its population on ONE condition — `WI-469` — and `WI-469` landed, so the
ruled pass ran.

**Population, re-measured before editing: 48, not the 49 recorded below** (45
`Contract names WI-###` + 3 `Contract cites decision`, over 35 rows). One
citation left with `WI-469`'s re-authoring of the `Consumes` rows. That drift is
exactly what pinning the hold on a read surface was for, so the number is
recorded rather than reconciled away.

Both advisory arms now report **ZERO** (48 → 0; the whole run's advisory WARNs
125 → 75). **24 rows took a plain deletion** — the citation was a parenthetical
tag or a whole provenance sentence, and the cell still states what crosses.
**11 needed a REWRITE** (`IF-015`, `IF-024`, `IF-029`, `IF-044`, `IF-052`,
`IF-056`, `IF-066`, `IF-071`, `IF-074`, `IF-091`, `IF-121` — the citation was
carrying contract content, so the cell re-states the fact plainly). The two
retired `CMP-00x` ids died with the sentences carrying them, as the hold
intended: `IF-056`'s `Declared at WI-064 … CMP-002 -> CMP-001` and `IF-077`'s
`Declared at WI-354 … CMP-001 -> CMP-003` are gone whole.

`docs/provenance-allow`'s header records the hold as **EXPIRED 2026-08-23,
EXECUTED** rather than deleting the clause — the population count and its drift
are the only measurement that pin ever produced. No entry line moved (the file
has had none since 2026-08-20, and this detector takes no `allow` parameter), so
every consumer reads what it read before. Approval authority verified rather
than assumed: all 35 rows are `Drafted`, `human_approves` governs a `status`
writer and not a `contract` cell, and no snapshot was refreshed — nothing was
stopped on and no human warrant is owed.

Two citation-SHAPED phrases the detector does not match were left standing as
findings, not fixed inline: `IF-090`'s "enact ruled decision 2" and `IF-094`'s
"the ruled A1/A8 tables". The `WI-390`-banked `IF-055`/`IF-080` hits are NOT in
this population and stay banked.

**Item 2 below is STRUCK.** Item 1 stays blocked on `OI-60` (pending, the
owner's); item 3 is unblocked and unstarted.

### Slice 3, 2026-08-22 — the `SR-162` fold-in LANDS; the D-3 shed STOPS at a measurement.

The lane stays ACTIVE. One of the two things this slice was scoped for landed;
the other stopped before it edited the registry, and the stop is the slice's
main product.

**Landed: the orphan fold-in.** `SR-162` (requirement boundary references
resolve against the declared frame) is decomposed — `LLR-187` (the frame's own
joins, the SR→crossing rule, and the severity split that makes both adoptable;
`trace.frame_findings`/`sr_boundary_findings`/`_frame_report_section`) and
`TC-182` (thirteen existing test nodes across `tests/test_external_frame.py`
and the signal-vocabulary case in `tests/test_trace.py`). Both mint `Drafted`
— approval is the owner's act. The machinery was already delivered, so the
decomposition RECORDS it rather than commissioning it, and the two clauses of
the parent that are NOT delivered are stated on the row in the debt-stating
pattern: the joined-seam signal-compatibility rule has no join to read, and the
two-sided-change obligation is the parent's own named residual. The orphan set
drops by one; the lane's `sr_refs` now resolves to a decomposed row.

**STOPPED, with the population measured first: the D-3 shed.** `OI-54` (a)
unblocked the transform, and the first act was to measure the 129 live rows
against the staged spec (R4 of
[`docs/plans/2026-08-15-retier-v2-one-decision-tiering.md`](../../../plans/2026-08-15-retier-v2-one-decision-tiering.md)
§1.4) rather than to start editing. Three findings, and together they say the
shed is not the pass the ruling's blast radius described:

- **The ruled reading is already the authoring** on 53 of the 54 design-owned
  `Consumes` rows — their `counterpart` IS the owner design row's module, the
  provider — so (a) costs nothing to adopt and re-authoring them would change
  nothing. `IF-031` is the single exception, authored under the reading that
  was not ruled (owner = the module holding the consuming code).
- **`this_project`'s death has an unmet precondition.** R4 kills it *"once
  derivable as owner→LLR→`module`"*. It is derivable on all 32 design-owned
  `Provides` rows and on none of the 12 requirement-owned ones (`IF-001`,
  `IF-005`, `IF-009`, `IF-011`, `IF-013`, `IF-014`, `IF-015`, `IF-044`,
  `IF-053`, `IF-065`, `IF-076`, `IF-081`), where the target shape has no cell
  that can hold the providing module — and dropping it takes their producer
  credit in the connectivity advisory and their source end in the declared-seam
  pairs with it.
- **`counterpart` is tri-modal on `Consumes` rows** since `WI-469`'s medium
  pass — provider, medium, or consumer CLASS (the 16 `B-05` rows) — so
  counterpart→consumers is a per-row re-judgement of 85 rows, and on the third
  group the ruled reading puts the counterpart *beside* `this_project` in the
  consumers list rather than opposite it, a shape `OI-54` does not state.

Filed as **`OI-60`** (pending) with the full census, four options and a
recommendation — (a) shed `direction` only and keep a provider-side endpoint
cell until the 12 are re-pointed, plus the two free corrections. Nothing in
`interfaces.toml` was touched. Item 1 below therefore stays OWED and is
re-blocked, this time on a *scoped* question with a row rather than on prose.

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
2. ~~**The 49 held `Contract`-cell provenance citations.**~~ **DONE — slice 4,
   2026-08-23.** Re-measured at slice 2 and UNCHANGED at exactly 49 (46
   `Contract names WI-###` + 3 `Contract cites decision`); measured at 48 when
   the pass executed, one having left with `WI-469`. The hold and its `WI-469`
   blocker were recorded in `docs/provenance-allow`'s header, which now records
   the hold as expired-and-executed. The two retired `CMP-00x` ids inside
   `IF-056`'s and `IF-077`'s held clauses died with the sentences carrying them,
   which is why they were deliberately left rather than corrected separately.
3. ~~**The `external.toml` context view** — entities/crossings/relationships
   rendered into the dashboard.~~ **DONE — slice 5, 2026-08-23.** The spec's own
   *"may land as its own slice"*, and it was: `traj_parse.frame_context` +
   `traj_context.py`, spliced above the derived structure in the How tab, with
   the tie-backs joined from `interfaces.toml` and the adjudicated absences
   stated. This is what satisfies the boundary record and closes sitting-2
   decision 8's execution.

**Queued for the owner rather than decided here** (both minted this slice):
`OI-49` — what the sitting is actually being asked to approve from the 2026-08-15
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
- **Orphan fold-in (owner-directed 2026-08-22):** the lane's remaining
  schema half owns `SR-162`'s subject (requirement boundary references
  resolve against the declared frame) — decompose that orphaned SR into
  its LLR/TC when the counterpart→consumers transform executes, mirroring
  the WI-484 Hat-Refs resolution-rule pattern.
