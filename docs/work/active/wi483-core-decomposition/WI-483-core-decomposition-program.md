+++
id = "WI-483"
title = "Successor decomposition program: break the seven-module import cycle behind typed read models, split the largest engines by policy/effect boundary, and re-point the size-ratchet's debt owner (repo review 2026-08-19 H-02, H-05, M-02, M-06)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = ["~WI-448"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

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
2. **`IF-088` and `gen_open_items`** — `dispatch._pending_cards` still calls the
   private presentation functions `_blocked_pending`/`_spine_pending`, and
   `gen_open_items` still imports the large facade for a state query. Both are
   documented bad edges rather than broken ones; neither is inside the SCC, so
   neither was on this slice's critical path.
3. **The engine splits (program shape item 5)** — `trace.analyze` (514 lines,
   complexity 50), `check.steps` (494), `agent_loop.main` (402/27), and the
   `LoopContext` / `Registries` / `Findings` attribute bags. Untouched. Note the
   standing trap when they are: ruff's C901 counts a nested def into its
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
