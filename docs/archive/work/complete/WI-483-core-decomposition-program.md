+++
id = "WI-483"
title = "Successor decomposition program: break the seven-module import cycle behind typed read models, split the largest engines by policy/effect boundary, and re-point the size-ratchet's debt owner (repo review 2026-08-19 H-02, H-05, M-02, M-06)"
specref = ""
workstream = "process"
sr_refs = []
needs = ["~WI-448"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

**The seven-module import cycle is GONE, the lifecycle band is LAYERED and the
layering is asserted, and the three worst engines are decomposed.** Seven
slices, 2026-08-20 → 2026-08-24; each slice's own record is a block under
`## Context` below and a fragment in `docs/log.d/`. Spec of record (the
`SpecRef` cell is cleared at a terminal close, so it is named here instead):
`docs/archive/repo-review-2026-08-19.md`.

**H-02 (the cycle).** 7 modules / 12 intra-cycle edges → **0 / 0**, measured on
a graph that INCLUDES function-body imports. Five extractions did it, each
placed BELOW every module that reads it: the lane-close terminal-outcome
vocabulary and the per-close report's shape into `scripts/kitlib/station.py`,
the registry-gap census into `scripts/census.py`, the pending-owner-action read
model into `scripts/pending.py`, the checker's cross-row coherence rules into
`scripts/coherence.py`. The two DOCUMENTED bad edges (`IF-088`,
`gen_open_items`) are cut rather than described, and the `gen_trajectory` facade
now has zero importers. `tests/test_import_layers.py` holds all of it as
equality ratchets.

**Program shape item 4 (the layering).** `dispatch` is the sole composer and the
band runs one way below it — `dispatch` > `handback`/`lane` > `integrate` >
`intake` — and slice 7 turned that sentence into `LIFECYCLE_RANK` plus
`test_a_lifecycle_edge_never_points_up`, which reds on an edge that points up OR
sideways even when no cycle forms. The surviving `integrate -> intake` edge was
MEASURED rather than inherited and ruled a downward call, KEPT.

**H-05 (the engines), on the axis the owner's `OI-16` correction names.**
`trace.analyze` 553 → 218 lines / C901 50 → under the limit; `agent_loop.main`
402 → 152 / 27 → under; `session_bookkeeping` 325 → 28 / 31 → under;
`run_iteration` 326 → 120 / 20 → under. **Four complexity-baseline entries
DELETED.** Four attribute bags became typed records — `Registries` (frozen, 34
fields, one construction site), `Findings`, `LoopContext` (frozen, 29 fields)
and `LoopRun` — and declaring them exposed a dead field and two defaulted
`getattr` reads that would have silently meant "human-held, don't keep going".
`check.steps` was re-measured and deliberately LEFT (649 lines, complexity
**8**): the split is a question about the carrier for a flat declaration, and
the honest answer is that it is not debt on this program's axis — see slice 7.

**The debt owner moves on, rather than rotting.** `tests/test_module_size_
ratchet.py` now names `WI-508`. Re-pointing it away from a closed item was this
row's own first act (H-05's finding); leaving it pointing HERE at close would
have recreated the defect exactly.

**Behaviour is byte-identical wherever a slice touched a CLI**, measured by
capture-diff against `HEAD`/a stash rather than asserted — 31 driven paths and
seven exit codes for the loop, console + exit code + the whole `render_report`
text for the checker.

**Not done, and named as such:** M-06's four test monoliths
(`test_integrate.py` 3,520, `test_trace.py` 2,099, `test_trajectory_arch.py`
1,927, `test_agent_loop.py` 1,640) are unsplit. Item 4's own rule is that a
split RIDES ALONG with a subsystem decomposition and a standalone split slice is
out of scope; every subsystem this program decomposed was checked and none
needed one. They belong to the next decomposition, `WI-508`. Record:
[../../../log.d/2026-08-24-wi483-layering-close.md](../../../log.md#2026-08-24--wi-483-slice-7-the-layering-measured-rather-than-assumed--decided-and-the-row-closed).

## Context

The review's architecture cluster, one program. The facts, verified or
already on record:

- **H-02 — the cycle.** The AST import graph (deferred imports included) holds
  one strongly connected component: `dispatch <-> handback <-> integrate <->
  intake`, plus `dispatch -> gen_trajectory -> traj_panels -> integrate` and
  `dispatch -> lane -> intake`. `handback.py`'s "never the reverse" prose is
  already false (`integrate.py:2186` — the sentence is WI-477's to fix, the
  structure is this program's). IF-088 documents dispatch's use of private
  presentation functions rather than removing it; `gen_open_items.py` imports
  the large facade for a state query.
- **H-05 — the scale, and the dead owner.** Seven scripts over 2,000 lines
  (trace 4,438 / check_trajectory 4,058 / agent_loop 3,162 / bootstrap 2,859 /
  agent_common 2,608 / integrate 2,541 / check 2,096); worst functions
  `trace.analyze` (514 lines, complexity 50), `check.steps` (494),
  `agent_loop.main` (402/27); `LoopContext` and `Registries`/`Findings` are
  empty classes populated as mutable attribute bags. The size ratchet's
  commentary directs active debt to WI-280 — CLOSED, and scoped to the
  dashboard + `bootstrap.main` only. FIRST SLICE of this program: re-point the
  ratchet's debt-owner comment here, so the baseline has a live owner again.
- **M-02 — the topology.** 59 modules, no package, 33 sibling `sys.path.insert`
  sites, private names as cross-module APIs. Direction: a stdlib-only package
  copied downstream as a unit, package-relative imports, thin direct CLI
  wrappers preserved — the MAPPING/bootstrap half is exactly WI-448's landing
  zone, hence the soft edge: WI-448's themed consolidation lands first and
  this program builds on its shape, never beside it.
- **M-06 rides along** — when a subsystem is decomposed, split its test
  monolith by stable behavior in the same slice (test_integrate 3,495 lines /
  test_trace 1,826 / test_agent_loop 1,567 / test_trajectory_arch 1,412);
  no standalone test-split slices.

Program shape (the review's, adopted as the starting plan): (1) characterize
import directions and behavior; (2) extract dependency-neutral typed modules
for work outcomes, terminal-state enums, registry-gap parsing, pending-action
queries; (3) views depend only on read models; (4) `dispatch` becomes the
top-level composer with `integrate`/`handback`/`intake`/`lane` one-way below;
(5) split `trace.analyze`, `check.steps`, and the loop state by policy/effect
boundary — typed immutable config + explicit mutable runtime state; (6)
install an SCC/layer test that includes FUNCTION-BODY imports so deferred
imports cannot hide regressions. The house exemplars to imitate are already in
the tree (review P-04): `plan_round.py`, `spine_carrier.py`, `traj_graph.py` —
pure decisions, explicit data, effects at the edge. Explicitly NOT: growing a
generic `common.py` (the review's own warning to WI-448).

Collision square: `gen_arch_map`/MAPPING/module moves are contested by
WI-455 (lane), WI-390 (clause 2), and WI-448 — read all three before opening
any slice; module moves re-point LLR `module` cells and IF endpoints, which is
why this row is `safety_class = "spine"` despite being a scripts program.

### SLICE 1 LANDED 2026-08-20 — the first cycle edge, and the guard

**The census, re-derived rather than inherited.** The review's SCC reproduces
exactly: 7 modules, 12 intra-cycle edges, and 4 of the 12 exist only inside
function bodies. The characterization step (program shape item 1) is done and it
is now a TEST rather than a paragraph — `tests/test_import_layers.py` builds the
graph, including function-body imports, on every commit.

**The edge broken, and why this one first.** `traj_panels` — a render leaf that
writes nothing — imported the 2,541-line merge coordinator for exactly TWO
constants. That is the review's "the dashboard can drag mutation coordinators
into read-only rendering", literally and in one import line. The lane-close
terminal-outcome vocabulary moved to `project-trajectory/scripts/kitlib/station.py`
as a typed read model (`Outcome`, a `str` enum; `OUTCOME_DIRS`, immutable;
`outcome_of`, the "exactly one declared directory, or none" DECISION lifted out
of `integrate.branch_outcomes`, whose git-tree read stays where the effect
belongs). `integrate` re-exports the former names, so no caller moved.

**Cutting one edge dropped TWO modules from the cycle: 7 -> 5.** `traj_panels`'
only route into the component was that import, and `gen_trajectory`'s only route
in was through `traj_panels`. The remaining SCC is the lifecycle core proper —
`dispatch`, `handback`, `intake`, `integrate`, `lane` — and it is baselined in
the ratchet, which may only tighten.

**TOPOLOGY DECISION (recorded here because the row is `safety_class = spine`).**
The read model landed in `kitlib/` — the `station` theme slot WI-448 named and
deliberately left uncreated, handing it to this row — under a NEW `LLR-182` with
a SINGLE `CMP-008` tag, NOT appended to `LLR-181`'s module list. Appending would
have been one line cheaper and was rejected: `LLR-181` carries the four-way
usage tag `OI-48` was open about at the time, and a four-way tag SUPPRESSES the
cross-component seam rule on the module's edges — so the view-to-service seam
would have stopped being policed at the exact moment it was fixed, and the slice
would have spent an unruled owner question to tidy its own diff. A single tag is
also true here in a way it is not for the shared kernel: the station flow's
modules are all CMP-008. `IF-093` is therefore RE-POINTED (counterpart
`scripts/kitlib/station`, owner `LLR-182`) and stays a policed CMP-009 to
CMP-008 seam. This gave `OI-48` a worked data point — per-theme ownership is
available where a theme has an owner — and did NOT pre-empt it: `OI-48` is now
RULED (d) AND EXECUTED (2026-08-21 / WI-494, 2026-08-22), which confirmed this
row's data point rather than overriding it — `LLR-181` collapses to `CMP-006`
alone (the recorded closest-fit reason: registry.py's bulk), its real
cross-component consumption moves to the declared shared-kernel surface
(`docs/kernel-modules-allow`), and `LLR-182`'s single `CMP-008` tag stays
exactly as this row left it, `IF-093` still the declared seam and station.py
still outside the kernel declaration.

### SLICE 2 LANDED 2026-08-22 — the cycle is GONE (0 modules, 0 edges)

**The per-edge census, read before the cut was designed.** The five-module
component's three back edges were all deferred function-body imports, and they
carried three quite different things:

- **`intake -> dispatch`** (two call sites, one edge). `_census_drafts` needed
  `dispatch.parse_red_tc`; `_cmd_census` needed `dispatch.gap_census`. Behind
  those two names sat a self-contained ~180-line block — `gap_census`,
  `red_tc_census`, `_red_tc_line`/`parse_red_tc`, `_implemented_ids`,
  `RED_TC_PREFIX`, `_TC_NOT_RED` — whose only dependencies were `trace`,
  `schedule` and `agent_common`. Nothing in it decides anything about lanes.
- **`integrate -> handback`** (one call site). `_partial_report_refusal` needed
  `handback.report_path` and `handback.report_refusal` — a path built from two
  strings and a rule over a dict, reached from the merge slot through an import
  into the module that WRITES reports.
- **`integrate -> intake`** (one call site). `integrate_one`'s post-merge arm
  calls `intake.intake_after_merge` inside the held slot. This one is REAL
  lifecycle behaviour — amendment drafts, close drafts, disposition drafts and
  the mint, all-or-nothing on a trunk commit — and it is not extractable behind
  a read model without moving the mint itself.

**The two cuts, and why they were enough for the whole component.** The census
moved to a new sibling `project-trajectory/scripts/census.py`; the per-close
report's PATH/FORMAT/READ/REFUSAL moved down into
`project-trajectory/scripts/kitlib/station.py`, beside the terminal-outcome
vocabulary — the same `SR-144` sentence, whose two clauses had been living in
two modules. Both former homes re-export every name, so no caller moved and CLI
behaviour is byte-identical. With `intake -> dispatch` gone, `intake` reaches
nothing above it, so the surviving `integrate -> intake` edge closes nothing:
**7 -> 5 -> 0 modules, 9 -> 0 intra-cycle edges.** `CYCLES` is now an EMPTY list
compared for equality, which is the strongest form of the same ratchet;
`MAX_INTRA_CYCLE_EDGES` re-stamped 9 -> 0; the walker's self-test pin moved off
the edge this slice cut and onto `integrate -> intake`, the one still owed.

**Why the census is a plain sibling and not `kitlib`.** Every module of that
package must stay import-clean of the rest of `scripts/`
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`),
because `bootstrap.py` imports it. The census's whole purpose is to REUSE
`trace.analyze` rather than re-derive it, so it imports a sibling by
construction. The report's shape, by contrast, is pure and belongs exactly where
it landed.

**TOPOLOGY DECISION (recorded here because the row is `safety_class = spine`).**
Two NEW rows, not amendments: `LLR-188` (`scripts/census.py`, `SR-148`,
`CMP-008`, `TC-183`) and `LLR-189` (`scripts/kitlib/station.py`, `SR-144`,
`CMP-008`, `TC-184`). The alternative — re-pointing `LLR-149`/`LLR-159`'s module
cells and amending `LLR-182`'s detail — was REJECTED on authority, not on taste:
`Module`/`CodeSymbol`/`TestRefs`/`Component`/`Verifies`/`Evidence` are TRACED
cells and free to move, but `Title`/`Detail`/`Rationale` on an `Approved` row are
APPROVED, and `baseline_snapshot.refresh_refusal` exists precisely to stop a
session absorbing its own rewrite of approved text into the baseline. `--approves`
is a HUMAN's citation of an approving act and there is none here, so nothing this
slice did needed one: `refresh_refusal` reads clean because the diff is new rows
plus traced cells only. The re-export shims are what keep `LLR-149`/`LLR-159`
TRUE rather than merely unamended — `dispatch.gap_census` and
`dispatch.red_tc_census` still exist and the dispatcher is still rung 1's caller.
`LLR-182` is untouched and its "imports nothing" clause still reads true in its
own idiom (the module imported `enum` before this slice); `LLR-189` is the row
that names what station.py gained. `IF-089` is RE-POINTED (`this_project`
`scripts/census`) and stays a policed CMP-008 to CMP-006 seam — verified live
through `check_trajectory._classifiable_edges` + `_declared_seam_pairs`, not
assumed. Two new component-tagged modules means no new `uncontained` module in
the How-SW containment count.

**STILL OWED BY THIS ROW — the reason it is not closed:**

1. **The layering, which the cycle's death did NOT buy.** `integrate -> intake`
   survives: the post-merge mint at the held slot is a real upward call, and
   program shape item 4 (`dispatch` the sole composer with
   `integrate`/`handback`/`intake`/`lane` one-way below) is undone until it
   moves. Hoisting it into the composer changes what `integrate.py merge` does
   on its own, which is why it was NOT attempted inside a slice whose contract
   was byte-identical CLI behaviour; it needs its own slice and a decision about
   that CLI. Nothing polices the direction today except this file's
   view-never-imports-a-lifecycle-service rule, which `integrate` is not subject
   to.
2. **`IF-088` and `gen_open_items`** — ~~`dispatch._pending_cards` still calls
   the private presentation functions `_blocked_pending`/`_spine_pending`, and
   `gen_open_items` still imports the large facade for a state query~~ **DONE at
   slice 3, 2026-08-23** (see the slice block below).
3. **The engine splits (program shape item 5)** — ~~`trace.analyze`~~ **DONE at
   slice 4, 2026-08-23** (see the slice block below); `check.steps` and
   `agent_loop.main` plus the `LoopContext` bag REMAIN. The standing trap is
   confirmed rather than theoretical: ruff's C901 counts a nested def into its
   enclosing function, so a helper extracted INWARD raises the number the
   extraction was meant to lower — decompose outward.
4. **M-06's test-monolith splits**, which ride along with each subsystem
   decomposed. Slice 1 touched `test_traj_panels` and `test_integrate`; slice 2
   touched `test_loop_order`, `test_rule_sync` and `test_import_layers`. None of
   the five needed splitting for these cuts — the largest of them is under 400
   lines — and a standalone split slice is explicitly out of scope. The four
   monoliths the review named (`test_integrate` 3,495, `test_trace` 1,826,
   `test_agent_loop` 1,567, `test_trajectory_arch` 1,412) all still await the
   subsystem decomposition they ride along with.

**Deferred to the owner: nothing new, across both slices.** `OI-48` was engaged
by slice 1's topology decision but not widened by it, and it has since been ruled
and executed; slice 2 needed no ruling because it was built to need none — the
two new spine rows are authored, not amended, so no `Approved` approved cell was
rewritten and no approval act had to be cited.

### SLICE 3 LANDED 2026-08-23 — the two documented bad edges, and a facade with no importers

**The per-edge census, read before either cut was designed.** Both of item 2's
edges pointed at the SAME target — `gen_trajectory`, a CLI entry point that
re-exports the `traj_*` family — and both were reaching THROUGH it at code
living in `traj_status.py`:

- **`dispatch -> gen_trajectory`** (deferred, one call site). What crossed was
  two PRIVATE functions, `_blocked_pending` and `_spine_pending`, re-assembled
  at the dispatcher into "the cards, minus the pause" — and both consumers of
  that then took `len()` of it. The composer wanted a COUNT and imported a
  render family to get one. `IF-088`'s Contract cell spelled the arrangement
  out, which is a seam registry RECORDING a crossing rather than licensing it.
- **`gen_open_items -> gen_trajectory`** (module-level, one call site).
  `pending_block(root)`, the whole rendered pending region, reused verbatim so
  the owner surface grows no second opinion. The reuse was right and is
  unchanged; the route was wrong.

Those two were the facade's ONLY importers.

**The cut.** A new sibling `project-trajectory/scripts/pending.py` — the sibling
of `census.py`, answering the other half of the same question (*what does the
OWNER hold?* rather than *what do the registries lack?*). The three sources moved
verbatim out of `traj_status.py`; above them the slice added `pending_items`, the
TYPED read model (one `PendingItem(kind, line)` per action, `kind` a FIELD so the
one discriminating caller parses no prose), and `owner_cards`, that model minus
the pause — the WI-381 amendment's never-disagree requirement held by
construction rather than by three callers agreeing to be careful. `traj_status`
re-exports all four former names, `gen_open_items` and `dispatch` call the model
directly, and both generated surfaces are byte-identical (`--check` clean).
`gen_trajectory` now has ZERO importers, asserted as an equality ratchet
(`test_a_facade_is_an_entry_point_and_nothing_imports_it`) for the same reason
`CYCLES` is: zero is the state today and equality is the strongest form of it.
Census: 72 -> 73 modules, 204 -> 207 edges (one new module brings its own three
dependency edges; the count this slice moves is the facade's importers, 2 -> 0),
deferred edges unmoved at 19, `CYCLES` and `MAX_INTRA_CYCLE_EDGES` already at
their floor and untouched.

**TOPOLOGY DECISION (recorded here because the row is `safety_class = spine`).**
`IF-088` is RE-POINTED, not retired: the crossing is real and still happens, so
deleting the row would have removed a true seam along with the bad route. Its
`counterpart` moves to `scripts/pending`, its `owner` follows the counterpart to
the new `LLR-198` (the `IF-089` shape), and the CMP-008 to CMP-009 pair is
unchanged and still policed. `IF-125` follows the drift arm down to `pending`;
`IF-084` drops the clause for the projection that left it and `IF-138` is minted
for the loader read that went with it. `LLR-139`'s traced `Module`/`CodeSymbol`
cells follow their two functions. `LLR-198`'s Module cell names `pending.py` AND
`traj_status.py` — the shim is part of the deliverable, and `LLR-139` had been
the ONLY row whose Module cell tagged `traj_status`, so moving that cell alone
left the module uncontained.

**DEVIATION FROM SLICE 2's PRECEDENT, on cause rather than taste.** Slice 2
authored its new rows `Approved` and let `intake.py snapshot` record the approval
in the same act. That refresh is REFUSED in this tree, and not by anything this
slice did: `baseline_snapshot.refresh_refusal` blocks on `LLR-147`'s `Detail`,
already drifted from its snapshot copy at HEAD (verified by stashing this slice's
whole diff and re-running the refusal). Blessing another row's drift is not a
session's to do. So `LLR-198`/`TC-194` are `Drafted`: no approval act is claimed,
no approved cell is rewritten anywhere in the diff, and `integrity=0` is
unchanged from HEAD rather than gaining the two approval-record findings
`Approved` rows would have added.

**STILL OWED BY THIS ROW after slice 3: items 1, 3 and 4 above, unchanged.**
Item 2 is struck. Item 1 (the `integrate -> intake` layering) is next and needs
its own decision about what `integrate.py merge` does on its own; items 3 and 4
follow it.

**Deferred to the owner: nothing new.** The `LLR-147` snapshot block is a finding
this slice reported to `docs/status.md`, not a decision withheld: it predates the
slice and belongs to whoever amended that row.

### SLICE 4 LANDED 2026-08-23 — the first engine, and the pair of typed bags

**Re-measured before choosing, and two of the three had grown.** `trace.analyze`
553 lines / C901 50 (the review recorded 514/50); `check.steps` 628 (was 494) but
UNDER the complexity limit — C901 does not flag it, because it is a flat
declaration of steps rather than branching; `agent_loop.main` unmoved at 402/27.
Worst-offender-first therefore picked `trace.analyze` with no argument, and the
disagreement between the two axes on `check.steps` is itself the reason the
program pays down complexity rather than length (the owner's `OI-16` correction).

**The boundary, in one sentence, because a decomposition that cannot say where
its line is has not drawn one.** A rule that JOINS ACROSS ROWS moved to the new
sibling `project-trajectory/scripts/coherence.py`; a rule that inspects one row's
prose, or asks whether a CARRIER parses, stayed with the engine. Out: the
four-tier orphan rules, `tc_citation_findings`, the PB/REPO/CMP back-link and
membership resolutions, the knowledge-pack resolution, `PhaseScope` and the
`--require-verified` status criterion. Stayed: the carrier sweeps, now NAMED
(`integrity_sweep` / `placeholder_sweep` / `schema_sweep`), the per-row prose
lints, `verification_basis` (a counter, not a rule), the renderers, the
approval/watermark machinery and the CLI. `analyze` is what is left — the
composer, 218 lines, under the complexity limit and OFF the census whose largest
number it had been.

**The trap was live, not theoretical.** The `in_phase` closure nested inside
`analyze` was charged to `analyze` by C901, which is the item-3 note working
exactly as written. It is now `coherence.PhaseScope.covers`: a frozen record with
a method, resolved once, reusable and testable.

**The bags.** `Registries` is a FROZEN dataclass, 34 declared fields, constructed
at exactly one site — asserted, because a frozen record is only a guarantee while
one place fills it — and the two defensive `getattr(reg, ..., [])` reads the bag
shape had forced are gone. `Findings` is the mutable half: a plain dataclass
whose two post-analyze fields are DECLARED with empty defaults rather than
conjured at a call site, since their rules read git and the filesystem and
analyze's contract is purity. `AnalysisFlags` is new and small: `census.py` had
been importing `argparse` to forge a four-field `Namespace`, which is what a
non-CLI caller must do when the CLI namespace IS the config type.

**Byte-identical, measured that way.** Console + exit code, the whole
`render_report` text, and `census.gap_census` all diffed empty against a stash of
the slice's script diff. Finding ORDER is now the composer's property (SR → LLR →
TC → SN, documented as load-bearing) and every tier returns the
`(at_fault_id, finding)` pair `tc_citation_findings` already returned, so the
at-fault id set is collected in one place instead of at eight append sites.

**Ratchets moved DOWN, with one declaration-only bump.** `trace.analyze`'s
complexity entry DELETED (50 → under 10); `trace.py` 5,373 → 5,316 re-stamped
down — a net shrink despite ~75 new lines of field declarations, because 323
lines of rules left; `coherence.py` 425 lines, under THRESHOLD and with ZERO
complexity entries (`spine_orphan_findings` measured 15 as a straight lift and
was split again rather than opening a baseline row). `bootstrap.py` +6, reviewed:
one MAPPING row plus its comment, the same shape slice 3 took for `pending.py`.

**TOPOLOGY DECISION (recorded here because the row is `safety_class = spine`).**
ONE new row, not an amendment, on slice 2's rule: `LLR-201`
(`scripts/coherence.py`, `SR-157`, `CMP-006`, `TC-197`). `CMP-006` is trace.py's
own component, so the new module opens NO cross-component seam and mints no
`IF-###` row — verified live through `check_trajectory --strict`, which reported
the containment error before the row existed and is clean after it. Both rows are
`Drafted`, following slice 3's recorded deviation for its stated cause: the
`LLR-147` snapshot refusal still stands in this tree, it predates this slice, and
blessing another row's drift is not a session's to do. `integrity=0` unchanged
from HEAD.

**M-06 rides nothing here.** The split needed no monolith split, and the new
module gets its own `tests/test_trace_coherence.py` (16 tests) guarding the
BOUNDARY rather than re-asserting rules already covered through `trace` — the
rules driven directly one tier at a time, the frozen/total record and its single
construction site, per-instance list defaults on the mutable record, and that
`analyze` STAYS a composer (measured span, plus "no nested def", so the 553-line
function accreting back is a red rather than a discovery).

**STILL OWED BY THIS ROW after slice 4: items 1, 3 (partly) and 4.** Item 3 is
struck for `trace.analyze` only. `agent_loop.main` (402/27, with
`session_bookkeeping` at 325/31, `run_iteration` at 326/20 and the `LoopContext`
bag — the direct analogue of the two bags typed here) is the honest next engine:
same defect, same fix, a bigger blast radius because the loop's state is
genuinely mutable across an iteration. `check.steps` needs a DECISION rather than
a technique — 628 lines of flat step declaration, under the complexity limit, so
its split is a question about the carrier for a declaration and may reasonably
end in "leave it".

**Deferred to the owner: nothing new.**

### SLICE 5 LANDED 2026-08-23 — the second engine (`agent_loop.main`), and the loop's bag typed

**Re-measured before designing, and nothing had drifted.** `agent_loop.main` 402
lines / C901 27, `session_bookkeeping` 325 / 31, `run_iteration` 326 / 20,
`agent_loop.py` 3,240 lines — slice 4's figures exactly, so worst-offender-first
picked `main` and its bag with no argument.

**The boundary, in one sentence.** Everything that RESOLVES what this run is —
the effective root, the five phase maps, the enable-list, the declared dials, the
reviewer/knob integers — is a pure function returning a typed record; `main`
keeps the EFFECTS (console, coordinator lock, subprocess, banner) and the mode
decisions between them. Thirteen module-level functions came out (`_resolve_root`,
`_parse_session_maps`, `resolve_routing_setup`, `resolve_session_setup`,
`resolve_session_policies`, `possible_session_models`, `_clamped_review_rounds`,
`_int_env`, `build_routing_state`, `_live_console`, `is_drive_launch`,
`warn_on_inert_or_malformed_policies`, `announce_critique_budget`,
`_dual_plan_entry`, `run_loop`); what is left is the sequence a reader needs in
one place — parse, resolve, refuse-or-continue, lock, mode, context, run. `main`
is **152 lines and OFF the complexity census** (its entry DELETED, 27 → under 10).
Decomposition is OUTWARD and a test asserts `main` nests no def, so the recorded
C901 trap cannot come back silently.

**The bag, typed — and it was hiding a defaulted read.** `LoopContext` is now a
FROZEN, TOTAL dataclass of 29 fields built at exactly one site, with `LoopRun`
(`routing` / `state` / `warned_no_core`) as the explicit mutable half. Declaring
it exposed what the attribute bag concealed: `session_hold` had NO reader
(dropped), and `human_held`/`keep_nondependent` were read as
`getattr(ctx, ..., <default>)` — a forgotten field would have silently become
"human-held, don't keep going". Both reads are now direct and an AST test forbids
`getattr(ctx, ...)` returning. Behaviour is byte-identical across 18 driven paths
(DONE / BLOCKED / budget / stall / six preflight refusals / malformed dials /
interactive / managed routing / `--help`), diffed against HEAD's script.

**Ratchets: one entry DELETED, one declaration bump.** `main`'s complexity entry
is gone; `agent_loop.py` re-stamped 3,240 → 3,455 (+215), a reviewed bump whose
bulk is 54 bare field declarations plus the comments that moved out of `main` —
the `bootstrap.py` shape the size ratchet's own header records as the owner's
`OI-16` counterexample.

**No new module, so no topology decision.** Nothing left `agent_loop.py`, so no
MAPPING row, no `bootstrap.py` change, no RESYNC entry, no new spine row and no
new seam — and no `Approved` cell was rewritten anywhere in the diff. The eight
boundary tests went to `tests/test_agent_loop_policy.py`, already the declared
home of "the ungated Slice D/E `main()` seams" (WI-277).

**STILL OWED BY THIS ROW after slice 5: items 1, 3 (partly) and 4.** Item 3 is
struck for `trace.analyze` and `agent_loop.main`. What remains of it:
`session_bookkeeping` (325 / 31 — now the kit's most complex single function) and
`run_iteration` (326 / 20), which this slice deliberately did NOT take because the
main/bag split left them no better home: both are per-session consequence ladders
whose branches are about routing state, not configuration. `check.steps` still
needs a DECISION rather than a technique.

**Deferred to the owner: nothing new.**

### SLICE 6 LANDED 2026-08-23 — the loop's two consequence ladders, and one page rule instead of two

**Re-measured before designing, and nothing had drifted.**
`agent_loop.session_bookkeeping` 325 lines / C901 31 (the kit's most complex
surviving function), `run_iteration` 326 / 20, `agent_loop.py` 3,462 —
slice 5's figures exactly, so the remaining engine pair was taken with no
argument about which.

**The boundary, in one sentence.** What a session's outcome MEANS — which
consequence arm applies, whether a page stops the run, what a reset hint buys,
how two verdicts compare — is a named function over routing state, several of
them returning frozen records; the arms keep the EFFECTS (console,
`RoutingState` mutation, telemetry commits, stop banners, the subprocess).
Twenty module-level functions came out: the four bookkeeping arms
(`reroute_rate_limited`, `review_bookkeeping`, `critique_bookkeeping`,
`build_bookkeeping`) with their decisions under them, and the session's own
stages (`wait_out_blackout`, `current_assignment_wi`, `launch_session`,
`write_raw_stream`, `session_meta`, `after_session`). **`session_bookkeeping` is
28 lines and `run_iteration` 120, and BOTH are OFF the complexity census** —
their two baseline entries DELETED in the same commit. Decomposition is OUTWARD
and a parametrized test asserts neither ladder nests a def, so the recorded C901
trap cannot come back silently.

**The duplication the split exposed, consolidated.** The two S8 page-the-human
ladders — a review escalation and an exhausted critique budget — had been
written out in full, thirty lines apart: the same `failure_action` read, the
same `human-held and not keep_nondependent` stop test, the same design-check
re-arm. They are now ONE rule, `page_consequence(fa, force_block)` returning a
frozen `PageConsequence(stop, design_check)`, plus `apply_page_consequence` for
the banner/exit/re-arm effect; the critique arm's declared `exhaustion = block`
is the single declared asymmetry, passed as an argument rather than duplicated
as a second ladder. Writing it once made an implicit ordering explicit — the
original never reached the design-check arm on a stop path because it had
already returned, and that is now a field.

**Three typed records, and one deliberate non-record.** `PageConsequence`;
`RoundSubstance(family_substance, margin, primary)`, because `margin` and
`primary` are only meaningful across a PAIR and were three locals kept in step
by hand; `LimitWait(nap, seconds, message)`, whose explicit `nap` discriminator
exists because a zero-second wait is still a wait. The session telemetry
projection stayed a DICT (`session_meta`): it IS `write_session_log`'s column
set, so a record would only be splatted back into one — its key ORDER is pinned
by a test instead, that being the property which could silently break.

**Byte-identical, measured that way.** 31 driven paths — 16 legacy, 10 managed
review (including the full escalation ladder to page-human), 5 critique
(including budget exhaustion under both `move-on` and `block`) — diffed empty
against HEAD's script, seven distinct exit codes covered, after the harness was
first self-diffed against HEAD twice to establish determinism.

**Ratchets: two entries DELETED, one declaration bump.** Both complexity entries
gone; `agent_loop.py` re-stamped 3,462 -> 3,614 (+152), a reviewed bump smaller
than slice 5's on the same module and of the same shape — the two functions shed
651 -> 148 lines between them and what replaced them is twenty signatures plus
the docstrings that used to be inline comment blocks.

**No new module, so no topology decision.** Nothing left `agent_loop.py`: no
MAPPING row, no `bootstrap.py` change, no RESYNC entry, no new spine row, no new
seam, and no `Approved` cell rewritten anywhere in the diff. The nine new
boundary tests went to `tests/test_agent_loop_policy.py`, already the home of
the ungated `main()` seams and of slice 5's record tests. M-06 rides nothing:
`tests/test_agent_loop.py` (1,640) is untouched and needed no split.

**STILL OWED BY THIS ROW after slice 6: items 1, 3 (only `check.steps`) and 4.**
Item 3 is struck for the whole `agent_loop.py` engine. Its entire remainder is
`check.steps` — 628 lines of flat step declaration, UNDER the complexity limit —
which needs a DECISION rather than a technique: its split is a question about
the carrier for a declaration and may reasonably end in "leave it". Item 1 (the
`integrate -> intake` layering) is unchanged and still needs its own decision
about what `integrate.py merge` does on its own; item 4 (M-06) is unchanged.

**Deferred to the owner: nothing new.**

### SLICE 7 LANDED 2026-08-24 — the layering MEASURED, item 3 dispositioned, and the row closed

**Item 1's premise was re-measured before anything was designed, and it does not
hold.** The lifecycle band's whole edge set, read off the same walker the
ratchet uses (function-body imports included):

| edge | kind |
| --- | --- |
| `dispatch -> handback`, `lane`, `integrate`, `intake` | module-level |
| `handback -> integrate` | module-level |
| `lane -> integrate` | module-level |
| `integrate -> intake` | deferred (the post-merge mint) |
| `intake -> ` *(nothing in the band)* | — |

fig: `import_graph()` from `tests/test_import_layers.py`, restricted to
`LIFECYCLE`, at `14759fc8`.

That is a strict total order — `dispatch` 0, `handback`/`lane` 1, `integrate` 2,
`intake` 3 — so **`integrate -> intake` points DOWN, and program shape item 4 is
already true.** The word "upward" in this row's own spec was inherited from the
cycle era: `intake` was above `integrate` only THROUGH `intake -> dispatch`,
which slice 2 cut. `intake` imports no lifecycle module at all, which is the
definition of the bottom, and `integrate.py`'s comment at the call site
(*"intake sits ABOVE this module"*) has been false since that cut — the same
class of defect as `handback.py`'s "never the reverse" that the review named,
and it is corrected in place.

**TOPOLOGY DECISION — `integrate -> intake` is KEPT, and `integrate.py merge`
is UNCHANGED.** This is the decision item 1 asked for, recorded here because the
row is `safety_class = spine`.

- **Rejected: hoist the mint into `dispatch`.** The mint must run INSIDE the
  held merge slot — serial by construction, all-or-nothing on one trunk commit
  (`integrate_one`'s own docstring, rulings R1/R3). Hoisting it above `integrate`
  runs it after the slot is released, or else moves lock acquisition up out of
  `_slot`, whose docstring names itself the one acquisition site *"and it must
  stay that way (§A2.0 requirement 1)"*.
- **Rejected: inject the hook** (`integrate_one(..., after_merge=…)`, dispatch
  passing `intake.intake_after_merge`). Either `integrate`'s own `main` supplies
  the default — in which case the import edge simply moves up one function and
  the graph is unchanged, a cosmetic fix — or it does not, in which case a
  human's `integrate.py merge` LANDS THE MERGE AND SILENTLY MINTS NOTHING. That
  is an owner-visible contract change trading a correctness hazard for one graph
  edge, and the edge was not even pointing the wrong way.
- **Rejected: move the mint family down.** `intake_after_merge` reaches
  `_amendment_drafts`, `_close_drafts`, `_disposition_drafts` and `_mint`, which
  is most of `intake.py`; "moving it below `integrate`" is renaming the module.
- **Accepted: `integrate_one` composing "merge, then mint" is not a second
  composer.** It is what taking the slot MEANS. `dispatch` remains the only
  module that sequences lifecycle services against each other.
- **The import stays DEFERRED**, and the reason is unchanged and now stated
  honestly: it keeps a plain `integrate.py claim` — the hot path of every lane
  run — from paying the mint family's import (`trace`, `check_trajectory`,
  `census`, `schedule`, `baseline_snapshot`, `wi_convert`). It hides nothing,
  because every rule in `test_import_layers.py` reads function bodies.

**What the slice SHIPS is the instrument, because the ratchet file itself
recorded that nothing policed direction.** `LIFECYCLE_RANK` + two tests: the
ranks must cover `LIFECYCLE` exactly (so a new lifecycle module forces a
placement rather than being exempt), and every intra-band edge must point
STRICTLY down. Strict, not `>=`: a peer-to-peer edge means one module is really
above the other and nobody has said which. **Mutation-checked three ways rather
than asserted** — a deferred `intake -> integrate` reds it; the 2026-08-21
review's own mutation (`lane -> dispatch` + `lane -> handback`) reds it; and the
case that matters, a SIDEWAYS `handback -> lane`, reds it **while both cycle
tests stay green**, which is the hole it was added to close.

**No new module, no spine row, no seam.** Nothing moved between modules, so no
MAPPING row, no `bootstrap.py` change, no RESYNC entry, and no `Approved` cell is
rewritten anywhere in the diff. `integrate.py` is NET-ZERO at 2,597 lines — the
corrected comment was written to fit rather than to buy a ratchet bump, since the
argument's one home is `LIFECYCLE_RANK` and a code comment restating it would be
the duplication this kit forbids.

**ITEM 3 REMAINDER — `check.steps` is LEFT, and this is the decision, not a
deferral.** Re-measured at `14759fc8`: **649 lines** (was 628 at slice 4),
**complexity 8**, **350 of the 649 lines are comment** and 299 are code.

fig: `wc -l` + `python -m ruff check --select C901 --config
"lint.mccabe.max-complexity=1"` over `project-trajectory/scripts/check.py`, plus
an `ast` span/comment count of the `steps` node, at `14759fc8`.

Four grounds, in order of weight:

1. **It is not debt on this program's axis.** The owner's `OI-16` correction —
   quoted by the size ratchet's own docstring and by slice 4 — is that the
   monolith risk is FUNCTION COMPLEXITY, not file length. `steps` measures 8,
   under the limit and BELOW three other functions in the same file
   (`approval_immutability` 10, `staged_divergence` 8, `run_plan` 8) that nobody
   proposes splitting. Splitting the one long flat function while leaving the
   branchier short ones is length-chasing.
2. **Its bulk is RATIONALE, not code.** 54% of the lines are the per-step
   comment explaining which rung a check arrives at and why. A split relocates
   comments; it does not simplify anything.
3. **The order of the returned list is load-bearing and reads top to bottom
   today** (*"Listed before traceability so at `--gate all` the fuller report.md
   wins"*). Per-band helper functions would distribute that ordering across
   call sites.
4. **The data-file carrier already exists and is deliberately partial.** An
   adopter adds steps through `docs/stack.ini` `[step:<name>]` and overrides the
   three product commands there; the PROCESS floor stays in code, where a
   profile cannot edit it away. Moving that floor into data would hand the
   assurance floor to the same file the project owns.

**And "leave it" is not an unguarded state.** `tests/test_complexity_ratchet.py`
compares the C901 census for EXACT equality, so a function absent from the
baseline that crosses the limit reds — the day `steps` stops being a flat
declaration, it fails, with no new instrument needed. Adding a second sensor for
one function would duplicate an armed one.

**ITEM 4 — M-06 rides nothing, at close as at every slice.** Nothing was
decomposed here, so nothing needed splitting. The four monoliths the review
named are unsplit and re-measured for the record: `test_integrate.py` **3,520**
(review: 3,495), `test_trace.py` **2,099** (1,826), `test_trajectory_arch.py`
**1,927** (1,412), `test_agent_loop.py` **1,640** (1,567).

fig: `wc -l` at `14759fc8`.

Item 4's own rule — a split rides along with a subsystem decomposition, a
standalone split slice is explicitly out of scope — held for all seven slices:
each checked its touched tests and none needed one. They belong to the next
subsystem decomposition, `WI-508`. **Named as unfinished rather than folded into
the close**, and one thing found while measuring them is left as a FINDING for
its own row, not fixed here: `tests/test_module_size_ratchet.py` censuses
`SCRIPTS` only, so no armed sensor watches these four grow — and three of the
four have grown since the review recorded them.

**THE DEBT OWNER MOVES TO `WI-508`.** This row's FIRST act (slice 1) was
re-pointing `tests/test_module_size_ratchet.py` away from the closed `WI-280`,
on H-05's finding that *"a ratchet whose commentary names a closed item tells the
next author that the debt is somebody's when it is nobody's"*. Closing this row
while it is named there would recreate that defect precisely, so the pointer
moves to `WI-508` — the live architectural-remapping program, which `needs`
this row and whose declared output is consolidation WIs filed against exactly
this residue. The dated per-entry bump notes are NOT re-pointed, for the reason
that file already states: rewriting a dated record to cite an item that did not
exist on its date would falsify it.

**STILL OWED BY THIS ROW: nothing. The row CLOSES.** Items 1 and 3 are
dispositioned above (one measured and ruled, one decided and left); item 2 was
struck at slice 3; item 5's engines are all done; item 4 never triggered and its
residue is named with a live owner.

**Deferred to the owner: nothing new.** Item 1's decision changes no
owner-visible contract — that is the reason it was takeable in a slice — and
item 3's is a shape call inside a kit script, argued from a rule the owner
already gave.
