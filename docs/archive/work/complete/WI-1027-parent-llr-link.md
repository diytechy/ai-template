+++
id = "WI-1027"
title = "LLRs decompose under an authored parent link, and every walk from an SR to its LLRs walks the tree"
workstream = "process"
sr_refs = ["SR-157", "SR-186", "SR-049", "SR-241"]
specref = ""
needs = ["WI-1023"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1027`, cut from `refactor_again` at
`bba30552f`, with the commit hooks on, under the plan
[plan.md](../../../plans/WI-1027/plan.md) (`578416476`) and the coordinator's
go-ahead, which approved it with rulings on its decisions D1 to D15 (D13:
record D1 in the decisions record; D15: quote the evidence below). Not
rebased: the coordinator resolves the merge hunks with WI-1060 and WI-1024 at
the merge. The specref (the review-churn plan's pointer rules) is cleared at
close.

- `578416476`: the plan.
- `290d3d5d1`: the walk, the cell and its findings, every reader, the
  dashboard, the rows, the tests, the ratchet stamps and the regenerated
  views.
- `e158002d8`: PROCESS.md §4, the skills, the question list, the registry
  machinery reference and the RESYNC entry.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The cell** (Done-when 1; LLR-480, new). `parent` joins
`kitlib.spine.SPINE_TIER_KEYS["LLR-ID"]`, the carrier's column map
(`"parent": "Parent"`) and its pinned inverse in `migrate_carrier.KEY`, and the
shipped template's example row, which is the tier's schema (its header names
the rule). One id, a string. The orphan pass (`coherence._llr_parentage_findings`,
over the walk's `broken` map) reports, naming the row, at any status, each
failing `--strict`: a top-level row naming no SR (`has no SR parent`, as
before); a child naming SRs (`is a child of LLR-Y and names SR-Refs (...)`); a
parent cell naming no live design row, an SR id or a `-000` id included
(`names parent Z, which is no live design row`); one naming several
(`names N parents (...)`); each row on a cycle (`is on a parent cycle (X -> Y
-> X)`); and each row whose chain breaks at one of those (`reaches no SR: its
parent chain breaks at LLR-Y`); that last one is reported where the chain
reaches a parent cell of the third kind or a cycle, which is what the walk
propagates. `trace.schema_findings` asks `SR-Refs` of a top-level row only
(`_required_fields`; LLR-483, new at review round 1, below). The cell is
**accepted** text in the
cell split (`SPINE_ACCEPTED_CELLS`, by name; decisions record
`docs/decisions/maint-wi-1027.toml` D-001, as the coordinator asked): a
re-parent of an accepted row is an amendment of that row, judged with its
whole text; `ROUTED_TRACED_CELLS` is untouched. The parent-first rule is not
extended to the parent link (D2): the follow-up row is **filed by the
coordinator**, since SR-245, LLR-357 and a TC each state the rule's closed
edge list.

**The one walk** (Done-when 2; LLR-481, new). `kitlib.spine.llr_tree(llrs)`
returns `LlrTree(below, srs_of, parent_of, depth, broken)`: down, every design
row below an SR or below a design row, each once, in registry order; up, a
top-level row's own SRs and a child's read up its chain; never raising and
never looping (each chain stops at a top-level row, a broken parent cell or a
row it has passed). Its costs: resolving the chains is linear in the rows
for acyclic chains, since each row's answer is memoized and every row is
resolved once, while a cycle's report lists the loop from each of its rows,
so a cycle of n rows costs about n² entries in its diagnostic; building
the descendant index is output-sensitive, since each row is listed under every
ancestor and every SR its chain reaches, so a single chain of n rows costs
about n²/2 entries (a real tree, a few levels deep, costs a few times the
rows). `llr_tree_rows` gives the
same answers as rows for the readers that render them; `llrs_under` keeps its
signature and reads the walk. Every reader that relates an SR to its design
rows now takes it:

| Reader (file: function) | Direction | What it does with a child |
|---|---|---|
| `kitlib/spine`: `llrs_under`, `_unverified`, via `review_scope` | down, up | the review test set (`review_set.py` reaches it only through `review_scope`, so that file is unchanged) reaches the grandchild's tagged file, and an untested grandchild is a gap |
| `coherence`: `spine_orphan_findings`, `_llr_orphan_findings`, `_llr_parentage_findings` | up | the six findings; a parent past Drafted that no case names says its children's cases do not discharge it |
| `trace`: `schema_findings` (`_required_fields`) | | `SR-Refs` asked of a top-level row only |
| `trace`: `triangle_findings` (`_triangle_line`) | up | a TC citing a grandchild beside its chain's SR is coherent, beside another SR is reported |
| `trace`: `effective_hats` (optional `srs_of`; IF-141's body says so), `hat_findings` | up | a child's effective perspectives union its chain's SRs' |
| `trace`: `chain_buckets` -> `spine_chain` -> `reaccept_model` (live and recorded) | down | an SR's chain holds every row below it, so the re-acceptance brief, the operator page, the amendment brief and the first-acceptance adjudication brief see a child with no change of their own |
| `trace`: `acceptance_lines` (`_tree_order`, `_below_marks`) | down | the batch acceptance hierarchy renders a child after its parent, marked `(below LLR-Y)` |
| `trace`: `build_forest` (`_llr_forest_node`, `_rootless_llrs`), `matrix_lines` (out of `render_report`), `mermaid_graph` (`_design_up_edges`) | down | the outline and HTML nest a child under its parent; only a row reaching no live SR is in the no-parent group; the matrix lists every row below an SR; the graph draws each parent link |
| `trace_text`: `paraphrase_advisories` | up | a child's Detail is compared with its chain's SRs |
| `derive_stage`: `_phase_groups` (`_design_srs`), `_stage_map`, `_ATTRIBUTED_ROWS` | up | a row joins its chain's SR's phase, the walk taken over the live rows so a settled child under a Drafted parent keeps its phase; `Parent` joins the attributed cells |
| `adjudicate_brief`: `_cited_spine` | down | the consolidation brief's spine names every row below the cluster's SRs |
| `intake`: `_context_block` (the design-row join) | down | the planning briefs' context block (the minted row's Context and the worker prompt) maps the grandchild's files and cases |
| `gen_components`: `_add_members` | up | a placed child reaches its chain's SR |
| `assumption_rules`: `module_srs`, `component_srs` | up | the architecture arm's reach (D3; LLR-244 amended) |
| `check_test_first`: `_associations`, `_members` | up, down | a test case is paired with a requirement through any row below it in the same copy (D3; LLR-257 amended) |
| `census`: `_implemented_ids` | up | a grandchild of a done row's SR is claimed |
| `consolidate`: `_llr_modules` | down | the touched-module pre-filter sees a child's files |
| `gen_release_checklist`: `_scope_ids` | up | a case naming only a child stays in phase scope |
| `gen_okf`: `emit` (`_children_by_parent`, `_llr_tree_links`) | | the bundle exports the authored link: a child's page links its parent, a parent's lists its children |
| `check_trajectory`: `_placed_sr_components` | up | the knowledge-pack join reaches a placed child's SR |
| `traj_parse`: `tree_llrs`; `rendering/traj_render`: `icicle_offsets`, `icicle_columns`; `rendering/traj_views`: `LLR_TIER`, `arch_icicle` | down | the dashboard (Done-when 4) |
| `kitlib/spine`: `interface_reach` (`_verifying_cases`); `coherence`: `interface_coverage`, `_route` (`_cases_below`) | down | blast radius: a design row constraining an interface brings the cases of every design row below it, as a constraining SR brings those below it; a row only observed at the interface brings its own cases alone; each of the two builds the tree once per call, never per row or interface (after trunk's merge, below) |

Unchanged readers of the link, as the plan says: `spine_rules._decomposed_sr_ids`
and `coherence._sr_orphan_findings` (only top-level rows carry `SR-Refs`, so
the set is the walk's on every tree the strict check passes; D14),
`trace_text.sr_fanout_advisories` (an SR's direct children are its top-level
rows), `kitlib.spine.parent_first_findings` (D2) and `intake._owning_srs` (a
re-parent is an accepted change and never reaches its routed arm). The 13
files that read only the work registry's `sr_refs` are untouched. **Blast
radius** moved onto the walk on this branch: WI-1024's slice 1 landed first
and reached the branch with trunk's merge (`60d44150a`), so the move was this
row's at the coordinator's call (D10). `interface_reach` builds the tree once
per call and reads `llr_tree(...).below` for a constraining SR and, new, for a
constraining design row; `coherence._route` reads the same `below`, built
once per `interface_coverage` call, for its design-row and requirement
routes (so a coverage call builds the tree twice, once in each). A spine with no parent cell reaches exactly as before: this
repository's reach and routes over its 239 interfaces dump byte-identical
before and after.
<!-- fig: cmd="interface_reach and interface_coverage over this repository's registries, dumped as JSON with the base and the changed scripts, then cmp" rev="01b49c333" -->

**A parent's discharge, coverage and the stage** (Done-when 3). LLR-408's rule
already holds: a design row is discharged only by a live case naming it, so a
parent's children's cases never discharge it; the parent's own case is its
integration TC, and a parent past Drafted with none fails `--strict`, the
finding saying `(a parent: its children's test cases do not discharge it)`. A
Drafted parent owes none yet, as SR-248's acceptance criteria say for every
Drafted design row (D7). Through the walk each descendant counts as a
top-level row: an SR is verified through any verified row below it, an untested
row below it is a review-set gap (a partial refusal for code-touching work),
an unverified row past Drafted is the no-test finding, and a Drafted
grandchild holds its SR's phase at the design-row rung in the live reading.

**The dashboard** (Done-when 4; LLR-482, new). The spine view's icicle has one
design column per tree depth: a child is drawn inside its parent's span one
column further in, and the test-case column follows the deepest design column.
A spine with no child renders as before; `PROJECT_STATE.html` regenerated with
only the new rows' counts and its as-of stamp moving. The depth comment on the
recursive walks is rewritten: the links come from the walk, which never links
a cycle.

**PROCESS.md, the skills and the question list** (Done-when 5). PROCESS.md §4
states decomposition (b) once: an SR states behaviour at the system boundary;
the component tree and the requirement tree decompose together below it; a
child names one parent and carries no `sr_refs`, its SR read up an acyclic
chain; a parent is discharged by its children plus its own integration TC;
every SR-to-LLR derivation walks the tree; "the rung does not recurse; the
rows do". The ladder's `DevStg-Reqs` and `DevStg-LLReqs` lines and the
oscillation sentence follow, and §2's table names both links (+537 bytes on a
watched file, re-stamped in the byte-budget skill). The spine-authoring skill's
authority sentence and a new `spine-questions.md` §3 bullet point at §4; the
gate-advance skill's ladder no longer says TERMINAL (all three copies of each
skill synced; the prompt catalogue regenerated). The registry machinery
reference states the `Parent` column, the tree-aware orphan and triangle
rules, the effective-perspectives reading and the cell split, and replaces its
stale §12.10.

**The S5 rows** (Done-when 5, D15). Of the spec's five, only LLR-367 is
re-cut. For the other four, the clause that names a design row's SR or walks
SR to LLR, and why it stays true once LLR-481 states how a child reaches its
SR:

- **LLR-001:** "computes the orphan set (SR without LLR/TC, LLR/TC without a
  parent, SN without an SR)". A child names its parent; a child whose parent
  is missing, several, or on a cycle is reported (LLR-480), so "LLR without a
  parent" still holds, and the SR's "has an LLR" is read through the top-level
  rows every child sits under.
- **LLR-201:** "The four-tier orphan rules answer whether each row has the
  children its tier requires and whether each id it cites resolves - ... an
  LLR its SR parent and TC ...". A child's SR parent is the one LLR-481 reads
  up its chain, and the id its parent cell cites is resolved in the same
  cross-row pass the row places there.
- **LLR-186:** "groups the rows into phases by REFERENCE (an LLR belongs to
  the phase of the SR it decomposes, and a TC citing only its LLR resolves
  back through it)". A child decomposes the SR its chain reaches, so it joins
  that SR's phase, and a case citing only a child resolves back through the
  child's chain.
- **LLR-197:** it states no SR-to-LLR walk. Its scope is "What one registry
  row's cells MEAN, stated once below every reader", it enumerates neither the
  schema's keys nor the kernel's joins, and it says "NOT CLAIMED: that these
  are the only shared row rules". The walk and the `parent` key join the same
  kernel without making a clause false.

**LLR-244's edit, on its own** (for the join with WI-1024's edit to the same
cell): in the first sentence, after "reaches the requirements named in SR-Refs
by the design rows realized in the one file stating its contract body", the
words **", a child row's requirements being those of the top-level row its
parent chain ends at"** are inserted before the full stop. Nothing else in the
cell changes.

**Rows** (`Drafted`, phase 6, minted from the branch's ranges, then
`trace.py --bump-ids`: LLR 408 -> 483, TC 508 -> 568): LLR-480 (SR-157),
LLR-481 (SR-157, SR-049), LLR-482 (SR-168), LLR-483 (SR-157, review round
1); TC-560 (LLR-480), TC-561 and TC-567 (LLR-481), TC-562 (LLR-482), TC-563
(LLR-367), TC-564 (LLR-244), TC-565 (LLR-257), TC-566 (LLR-408), TC-568
(LLR-483, review round 1), each naming its SRs beside, its evidence
generated from the tests' tags (`--regen-evidence`). Amended, `detail` text
only: LLR-367 (the scope phrase), LLR-244 (above), LLR-257 (the pairing
phrase, and four inherited code names scrubbed: the settings key, the tag
spelling, "pickaxe" and the step name). No SR written or amended. For
blast radius, two `Drafted` rows of WI-1024's are amended in text, no act
involved: LLR-421's `detail` (a constraining design row's cases include those
of the design rows below it, as a constraining requirement's include those of
the design rows decomposing it), and TC-531's `method` and `expected` (the
two cases below; its evidence regenerated from their tags).

**Red before the code** (each case written, run against the unchanged reader,
then the reader changed):
- The walk and the cell's findings, as first written: `23 failed, 2 passed in
  0.64s` (the two passes are the existing "no SR parent" case at each status).
- The checker's readers and the stage: `8 failed, 30 passed in 0.45s`.
- The discharge cases, run against the base `coherence.py`: `4 failed, 34
  deselected in 0.30s`.
- The remaining readers (component view, census, pre-filter, release
  checklist, OKF export, knowledge-pack join): `7 failed, 42 passed in 0.59s`.
- D3's two readers: `3 failed, 18 passed, 198 deselected in 0.66s`.
- The dashboard: `1 failed, 1 passed, 50 deselected in 0.35s` (the
  all-top-level case passes before and after, as it must).
- The review set and the brief cases, written after their readers changed,
  run against the base scripts (script changes stashed): `23 failed, 1 passed,
  46 deselected in 8.12s`; the one pass was a weak case, since rewritten to
  verify the requirement through the grandchild alone (red on the base too).
  <!-- fig: cmd="python -m pytest -q <the cases named> per stage" rev="the worktree before each reader's change, ahead of 290d3d5d1" -->
- Blast radius (after trunk's merge): `test_a_constraining_design_row_brings_the_cases_of_the_design_rows_below_it`
  and `test_a_row_only_observed_at_an_interface_brings_its_own_cases_alone`
  (TC-531), committed red in `5bbac4efd`: `2 failed, 19 deselected in
  0.36s`, each failing on the constrained interface's reach
  (`assert (['LLR-001'], ['TC-003']) == ...`), and again against the base
  scripts after one case gained SR-001 in a run case's verifies, so the
  strict check over its project does not stop on an SR no case names:
  `2 failed, 19 deselected in 0.35s`; after the change
  `test_constrains.py` reads `21 passed in 4.98s`.
  <!-- fig: cmd="python -m pytest -q tests/test_constrains.py (-k the two cases for the red run)" rev="5bbac4efd (red), 01b49c333 (green)" -->

**Tests:**
- The rule-5 set: every test module importing a changed script (an import
  grep over 22 modules, wider than the plan's 130), the modules holding every
  touched TC's evidence (TC-239, TC-250, TC-413 to TC-420, TC-466, TC-468 to
  TC-471, TC-560 to TC-567), the spine-linked modules `trace.py --tests-for`
  lists for each changed script, and `test_import_layers`,
  `test_module_size_ratchet`, `test_complexity_ratchet` and
  `test_dogfood_sync`: 181 modules, `1 failed, 6052 passed, 19 skipped, 18 warnings in 6199.58s (1:43:19)`. The one failure, `test_disposition_adoption.py::test_every_dispositions_section_in_the_repository_passes_the_fence_grammar[planted-indented]`, is a race of this lane's making: the case listed the queued spec, and the close moved it to `complete/` while the run was going (`FileNotFoundError` on `docs/work/queued/WI-1027-parent-llr-link.md`). On the settled tree the module reads `67 passed in 2.07s`.
  <!-- fig: cmd="python -m pytest -q -n auto <the 181 modules>" rev="e158002d8" -->
- `trace.py --root . --strict`: exit 0 (`orphans=0 integrity=0`);
  `check_trajectory.py --root . --strict`: exit 0 (`clean (1060 work item(s),
  ...)`); `check_complexity.py --mode enforce`: `OK - 169 row(s) over 15,
  unchanged from baseline`; `scripts/check_resync.py`: `OK, 26 shipped path(s)
  changed; entry anchored at bba30552f...`; `check_docs.py`: `OK - 3675
  doc(s), 3827 intra-repo link(s), 0 broken`.
- `run_menu.py smoke`, once at the end: exit 0, the strict lints first, then the tier `3821 passed, 3 skipped, 18 warnings in 163.63s (0:02:43)`; its budget line reads `CPU 665.0 s vs 540 s cpu-seconds; wall 164.3 s vs 600 s wall-seconds ... -> OVER`, warn-only by rule and the tier overrun WI-1039 is filed for.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="the close-out tree" -->
- The smoke tier collects 3824 against `max-tests = 3890`, so no re-stamp.
  <!-- fig: cmd="python -m pytest -q -m smoke --collect-only tests" rev="e158002d8" -->
- The unfiltered suite was not run, as the brief directs.

- Review round 1, after the fixes: the 79 modules importing what the round changed (`trace.py`, the dashboard's views, the registries' readers) with `test_requirement_tree`, `test_evidence_join`, `test_trace_golden` and the four named modules: `2715 passed, 2 skipped, 18 warnings in 2436.57s (0:40:36)`; `run_menu.py smoke`: exit 0, `3840 passed, 3 skipped, 18 warnings in 155.80s (0:02:35)`, its budget line `CPU 715.6 s vs 540 s ... -> OVER` warn-only, the tier overrun WI-1039 is filed for.
  <!-- fig: cmd="python -m pytest -q -n auto <the 79 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="the round-1 fix tree, ahead of its commit" -->
- Blast radius, after the change: the 39 modules importing `coherence` or the reach, those `trace.py --tests-for` lists for `kitlib/spine.py` and `coherence.py`, and `test_import_layers`, `test_module_size_ratchet`, `test_complexity_ratchet` and `test_dogfood_sync`: `1367 passed, 2 skipped, 18 warnings in 1238.89s (0:20:38)`; no ratchet moved. `run_menu.py smoke`: exit 0, `3874 passed, 3 skipped, 18 warnings in 130.80s (0:02:10)`, its budget line `CPU 656.2 s vs 540 s cpu-seconds; wall 131.6 s vs 600 s wall-seconds ... -> OVER`, warn-only.
  <!-- fig: cmd="python -m pytest -q -n auto <the 39 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="01b49c333" -->

**Ratchets.** `trace.py`'s module-size baseline is bumped +46 (3784 -> 3830),
the reason in its entry: the views and rules reading the walk, and the
outward decomposition the cognitive-complexity census asked for, which takes
`build_forest` and `triangle_findings` off that census and `mermaid_graph`
(31 -> 26) and `render_report` (65 -> 64) down. `check_trajectory.py` and
`intake.py` re-stamp down by one; ruff's ratchet re-stamps `render_report`
(17 -> 16) and `mermaid_graph` (17 -> 15) down. No complexity baseline rose.

**Also for the coordinator.** The watermark bump over the gap below this
branch's reserved ranges makes `trace.py` print a warn-only line naming spent
ids with no retirement record (LLR 409 to 479, TC 509 to 559 are other rows'
ranges); it is an advisory and changes no exit code. The recursive walks that
render the tree (the dashboard's icicle walks and the report's
`_llr_forest_node`) are bounded by the tree's depth, not capped: an acyclic
chain near the interpreter's recursion limit would raise RecursionError and
fail the generation loudly; their comments say so (review round 1). The merge hunks expected:
`intake.py` and `acceptance_record.py` (one line each beside WI-1060's
rework), `trace.py`, `kitlib/spine.py`, the registries, the watermark, the
ratchet baselines, the generated views and the RESYNC pack.

**Review round 1** (`bba30552f..9cc2cd5a0`): Hydrogen APPROVE; Sol, over a
code half and a docs half, six findings, all adopted by the coordinator, fixed
in one commit:

1. **MAJOR, LLR-480 stated two obligations** (the parentage findings and the
   required-field clause). The ruling: move the schema clause out, into an
   accepted row that states the required-field check, or a new row. It went to
   a new row, **LLR-483** (SR-157, Drafted) with **TC-568**, and the case's
   tag moved to TC-568 and gained the clause that every other required cell
   is asked of a child. LLR-003 names the required-field check only as a
   whole and lists no cell, so it stays true; amending it would have re-opened
   a row whose numeric-phase clause is driven by cases its TC-003 does not
   name (they are in `test_trace.py`; TC-003 names `test_registry_checks.py`)
   and whose text carries five flags and a ruling stamp to scrub, so the new
   row is the narrower act. The coordinator may rule it into LLR-003 instead.
2. **MINOR, LLR-480's propagation clause** read "each row whose parent chain
   ends at one of those faults", wider than the code, which propagates only a
   parent cell naming no live row or several, and a cycle. Narrowed to "each
   row whose parent chain reaches such a parent cell or such a cycle".
3. **MINOR, TC-562's expected** said "inside the top-level row's span" while
   the cases checked columns only. A new case asserts each row's vertical span
   lies inside its parent's and each height in units of its test cases (the
   grandchild one, the child two, the top-level row three).
4. **MINOR, TC-560's expected** said "at both statuses" while the cycle and
   below-a-missing-parent cases ran Drafted only, and the strict failure was
   checked for a missing parent only. Both cases now run at both statuses, and
   the strict check is driven for every fault kind at both statuses (16
   cases); TC-560's method and expected say so.
5. **MINOR, "linear in the rows"** overstated the walk: corrected above
   (linear chain resolution, an output-sensitive descendant index).
6. **MINOR, recursion depth**: the comments on the icicle's walks and on
   `_llr_forest_node` now state the bound and what happens past it; the walks
   stay recursive, as ruled.

Round 2 (narrow, 9cc2cd5a0..c319d6b9f): Hydrogen APPROVE; Sol two MINORs (the icicle comment's leftover 'provably safe'; linear resolution qualified for cycles), both adopted.

Round 3 (narrow: the merge's resolution, `git show --remerge-diff 60d44150a`, and the blast-radius move with round 2's fixes, 32e156e72..70024e28a): Hydrogen APPROVE; Sol one MINOR, that `interface_coverage` builds the tree once and `interface_reach` builds it again inside, against the prose's "once per call". Adopted in part by the coordinator: the docstring, this record and the log fragment now say each builds it once per call, never per interface; the two builds stay, since sharing one would widen `interface_reach`'s interface for no measured cost.

Round 4 (narrow, 70024e28a..3bf7831c8): Hydrogen APPROVE; Sol one MINOR, that the round's added "each build linear in the rows" contradicts the descendant index's cost stated above; adopted, the claim removed.

Round 5 (narrow, 3bf7831c8..0afc3a071): Sol APPROVE. Merged to trunk by the coordinator after round 5.

**Acts owed for automated adjudication:**
- First acceptance (`Drafted` rows this branch wrote): LLR-480, LLR-481,
  LLR-482, LLR-483, TC-560, TC-561, TC-562, TC-563, TC-564, TC-565, TC-566,
  TC-567, TC-568.
- Amendments to `Accepted` rows, each in its `detail` cell: LLR-367, LLR-244,
  LLR-257.
- No routed traced change to an `Accepted` row.

## Context

Variant F's seventh row (F-7), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F-call 5 with decomposition
(b) and an authored parent-LLR link (revision 35), and revision 36's
"every derivation that walks SR → LLR walks the tree". A child LLR names
one parent LLR and carries no `sr_refs`; only a top-level LLR carries
`sr_refs`; a child's SR is derived up the chain; the links are acyclic. A
parent is discharged by its children plus an integration TC.

Every LLR today is top-level, so no row migrates until a child is written.
The cost is in the readers. About thirty scripts read `sr_refs`; the walks
that matter are listed in Done-when 2, and the lane's plan confirms the
list from the code. PROCESS.md §4's ladder text ("TERMINAL", "the tier does
not recurse, the activity does") changes with decomposition (b).

**Siblings.** Blast radius is WI-1024's and the build brief's component
context is WI-1029's; both use this row's walk. WI-1029 waits on this row.
WI-1024 and this row both wait only on WI-1023 and may land in either
order: whichever lands second moves blast radius onto the tree walk.

## Scope answers

- **S1.** One deliverable: the cell, its rules and every walk changed
  together, so a child LLR's tests never drop out of the scoped set
  unseen (revision 36). The dashboard's requirement-tree view lands in the
  same lane, after the walks.
- **S2.** The scoped test set gates the review start (WI-995); this row
  changes the set's derivation, not its authority. No new authority.
- **S3.** Closed in Done-when 1 and 3: the cell's form and its findings,
  and when a parent is discharged.
- **S4.** `single`: schema, many reader families, a gate's input.
- **S5.** Adds the requirement tree; components and interfaces are
  unchanged. Re-cut LLRs (text only, drifting): LLR-001 and LLR-201 (the
  join and orphan rules), LLR-367 (the review test set), LLR-186 (the
  effective stage), LLR-197 (the spine row vocabulary); the lane's plan
  completes the list from the walks it changes.
- **S6.** `needs` WI-1023: the loader refuses undeclared requirement-tier
  keys there, so `parent` joins the declared set rather than sitting
  beside it. No new package, tool or service.

## Done-when

- [ ] LLR rows accept an optional `parent` cell naming one live LLR. A child
      carries no `sr_refs`; a top-level LLR carries at least one. A cycle,
      a dead id or either `sr_refs` breach is a finding failing `--strict`.
- [ ] One walk, in `kitlib.spine`, returns an SR's LLRs down the tree, and
      a child's SR up the chain. These readers use it: the orphan and
      coverage rules (`trace.py`, `coherence.py`), the stage derivation
      (`derive_stage.py`), the review's scoped test set (`review_set.py`),
      the acceptance brief, the adjudication briefs
      (`adjudicate_brief.py`), the planning briefs, blast radius (when
      WI-1024 has landed; otherwise WI-1024 adopts it) and the dashboard.
      The Deliverable lists every reader changed.
- [ ] **A parent's discharge.** A parent is an LLR some child's `parent`
      names. It must itself be named in the `verifies` of at least one TC
      (its integration TC); a parent with none is a finding failing
      `--strict`. An SR's coverage and the stage are derived over the
      whole descendant tree: each descendant counts exactly as a top-level
      LLR counts today, so an unverified or `Drafted` descendant holds its
      SR as one would now.
- [ ] The dashboard's spine view shows the requirement tree as the
      component view shows nesting.
- [ ] PROCESS.md §4's ladder text states decomposition (b) once; the
      spine-authoring skill and `spine-questions.md` point at it. The S5
      LLRs are amended (drifting, listed for adjudication).
- [ ] Tests build a three-level tree in a fixture and show each walk
      reaching a grandchild's TCs (red before the walk changes), a parent
      with no integration TC, and an unverified grandchild holding its SR;
      every importer of a changed module runs green.
- [ ] A RESYNC entry (variant F) gives adopters the cell; existing rows need
      no change.
