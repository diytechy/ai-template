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
