+++
id = "WI-1048"
title = "WI-1047's verdict answered: LLR-373 and TC-081 corrected, the six returned rows made ready for a second sitting"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-168", "SR-169"]
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1048`, cut from `refactor_again` at
`2474d7b4f`, with the commit hooks on. The specref (WI-1047's verdict,
`docs/reviews/wi-1047-adjudicate-f2-sitting/001-ADJUDICATE-3cd2513.md`) is
cleared at close, as a terminal row's is. No status moved and no act was
taken. Two test cases were minted from the lane's range, TC-474 and TC-475,
and `trace.py --bump-ids` raised the TC mark to 475.

- `732d08500`: the row text, the two new test cases, the tests they cite
  and the regenerated views.
- `3fa852a18`: the close-out, this Deliverable, the move to `complete/` and
  the log fragment.
- The commit after it, at the coordinator's request before the review
  ("LLR-373's title and rationale and LLR-398's scan surface follow the
  code"): the two text mismatches the close-out had left found, TC-474 and
  its test following LLR-398, and this Deliverable updated.

**LLR-373** (Accepted; Detail only, so it drifts). The code: the join
(`kitlib.spine.module_components`) is read by three rules on the
architecture surface: the How-SW top view and the cross-component scan,
each intersecting it with the ids it declares, and the per-component
connectivity warns, which do not intersect. The component view's generator
calls no join since WI-1022: it lists each component's modules from the
declarations themselves and places a seam from its endpoint cells
(`seam_placement`). The Detail's "gen_components places seams and lists
each component's modules by the declarations" now reads that gen_components
reads no map, lists each component's modules from the declarations
themselves, and places each seam from its endpoint cells alone, as LLR-199
states, so a map that answered nothing would move no seam (TC-435's
Expected). "The callers intersect them with the ids they declare" is
narrowed to the two that do, and the connectivity warns are named as the
third reader. The amendment adds no name the naming rule forbids: every
carrier in the cell is the accepted text's own.

At the coordinator's request, so that a sitting reading the row whole finds
it consistent, its title and rationale follow the Detail too (both drift;
no other cell changes). The title no longer says the component view reads
the join: "The module-to-component join has one home, which the
architecture checks read and the component view does not need". The
rationale drops the join's pre-WI-1021 inputs (a `-000` example row, an id
not starting LLR-), keeps the narrower answer as the Detail states it (a
value that cannot name a component makes no membership), says the two
gate-bearing rules intersect the map with their declared ids, where it said
every caller did, and adds why the component view needs no copy. It names
no carrier the accepted text did not, and drops one (`trace.py --strict`
becomes "the strict trace check").

**TC-081** (Accepted; Method and Expected, so it drifts; Evidence, a traced
cell, which routes to adjudication). It now states LLR-080's rendering:
with no rows the panel keeps its module table and draws no seam; a row's
seam is one edge, labeled with its id, between component and
external-party nodes, and a second render is byte-identical; in the
drilled view a component endpoint is wired at the layer that shows its
component's block (two parts meet inside their parent, a part's row to
another top-level component is the parent's wire at the top, a party is a
block of its own); and the architecture map's dependency diagram draws the
import and no seam, reading the same beside the rows as without them. Its
evidence is four tests that assert exactly that:
`test_how_sw_stays_a_table_without_seams`, kept and now also asserting the
module table, and three new ones,
`test_how_sw_graph_draws_component_and_party_nodes`,
`test_a_component_endpoint_wires_to_its_components_block` and
`test_the_dependency_diagram_draws_imports_only`. The two tests it cited for
module-, file- and bare-party-shaped rows, which the trace check now
refuses, keep running untagged (`test_how_sw_graph_renders_seams`,
`test_contracts_and_if_edges`), each with a comment saying why. The code
agrees with LLR-080's amended text on every registry `trace.py --strict`
passes: see "Findings".

**LLR-393, LLR-394, TC-455, TC-456** (Drafted). Their text names no
implementation carrier; the `module`, `code_symbol` and `evidence` cells
keep the names. LLR-393 states the table as "the rung table" beside the
stage derivation, each tier tied to "the derivation input that carries it",
and the four companion inputs by what they are (the need tier's drafted
set, the requirements the need-coverage arm reads, and whether the boundary
frame's registry and the component registry exist); its rationale says
"the derivation" and "input" where it said the function and its
parameters. LLR-394 states the lifecycle panel by what it draws, taking its
rungs from the stage ladder and each rung's tiers from LLR-393's rung
table. TC-456's Expected names "the stage derivation's rung table" where it
named the constant. TC-455's Method drives "the derivation" and "the rung
table".

**TC-455's own pass condition.** Its Expected no longer defers to LLR-393:
the settled inputs derive DevStg-Release with no tier named there; each
tier in work derives the rung the table names, and the table names SN and
STK at DevStg-Needs, B, DA and SUR at DevStg-Boundary, SR at DevStg-Reqs,
CMP at DevStg-Arch, LLR at DevStg-LLReqs, TC at DevStg-Tests and the
evidence record at DevStg-Impl; the rungs are the ladder's eight in order;
no tier name or input appears twice; and the inputs with the four
companions are exactly the derivation's. The literal mapping had no
assertion, so
`test_rung_tiers_covers_the_ladder_and_every_input_spine_stage_reads` gains
one, rung by rung, by the tiers' names.

**LLR-398's five clauses: TC-474** (new, Drafted, Integration, Full;
verifies SR-159 and LLR-398). TC-463 stays as it is, the unit case of the
uniqueness, ownership and surface rules. TC-474 is its companion over the
trajectory check, the verdict's own second option, since the five clauses'
tests sit in a Full-tier module and TC-463 is Smoke. Each clause and the
existing test TC-474 cites for it:

- warn plain, fail strict:
  `test_a_declared_seam_with_no_body_warns_plain_and_fails_strict` and
  `test_a_refused_header_reds_the_cli_under_strict`;
- the `interfaces_check` opt-out and no-surface vacuity:
  `test_the_gate_shares_the_interfaces_check_opt_out_and_the_files_mode_vacuity`,
  which turned the check off only through its legacy one-word file and gains
  `[checks] interfaces_check = false`, then `true`, in the process settings;
  its no-surface arms now list a configuration file whose body is a finding
  while the source root is scanned, and read none in files mode or with the
  source root pointed at a directory that does not exist (it read files
  mode with nothing listed before);
- a body in a file with no marker refused:
  `test_a_body_with_no_marker_is_refused_not_skipped`;
- a listed Python file read through its docstring:
  `test_a_python_file_listed_outside_the_source_root_is_read_as_a_module`.

LLR-398's `test_refs` reads `TC-463; TC-474`.

**LLR-398's scan surface** (Drafted), at the coordinator's request. Its
Detail placed a listed header file on the surface whatever the source root,
while the code (`_no_surface_reason`, ahead of `_declaration_sites`) reads
no surface at all in files mode or with the source root absent, a listed
header included. The Detail now says so: the surface exists only when the
scan profile is not in its files mode and the declared source root is
present, and then holds the files it held before; in files mode, or with
the source root absent, there is no surface, so a file the header list
names is not read either. No code changed. TC-474's Method and Expected,
and its opt-out test, follow (above), so the new clause is verified rather
than only consistent.

**LLR-395: TC-475** (new, Drafted, Integration, Full; verifies SR-157 and
LLR-395). Its Method and Expected are TC-428's and TC-429's together, with
one more input state: a case whose one validly tagged test fails when run
reads clean. That clause had no test, so
`test_a_declared_test_that_fails_leaves_its_case_clean` is new: it runs the
fixture's tagged test to show it fails, then runs the trajectory check under
strict checking and reads no finding and exit 0. TC-475 cites the thirteen
tests TC-428 and TC-429 cite, each now tagged `TC-428, TC-475` or
`TC-429, TC-475`, and the new one. TC-428's and TC-429's cells are
untouched. LLR-395's `test_refs` reads `TC-475; TC-428; TC-429`.

**WI-1038 is superseded, not still needed.** It exists to give LLR-395 a
verifying test case once LLR-395 is accepted, and the parent-first rule is
why it had to wait. TC-475 is that case now, Drafted beside its Drafted
parent, so the two can be accepted in one act and the circle is gone.
Re-pointing TC-428 and TC-429 at LLR-395 afterwards would add nothing a
sitting reads: TC-475 already covers every clause LLR-395 states, on the
same tests plus the failing-test case, and the re-point would leave three
cases verifying one row on one evidence set. What remains is a
duplication, TC-428 and TC-429 verifying SR-157 directly on evidence
TC-475 also cites; whether to retire them is a separate call, not
WI-1038's Done-when. WI-1038 is superseded by WI-1048; the coordinator
cancels it on trunk at the merge.

**Red first.** Each new test or arm passed on its first run, since the
behaviour it pins exists. Each was then shown to fail under a deliberate
mutation of the code it pins, reverted before any commit:

- `_sw_node` without its component arm, and `_seam_edges` drawing an edge
  for an endpoint outside the map: the three new TC-081 tests,
  `3 failed, 179 deselected in 2.19s`;
- the module table's class renamed: the strengthened table test,
  `1 failed, 65 deselected in 1.12s`;
- `read_interfaces_check_enabled` ignoring the process settings: the
  extended opt-out test, `1 failed, 171 deselected in 0.61s`. In the build
  commit its absent-source-root arm, with no header listed, did not fail
  when its no-surface reason was removed, since such a scan reads nothing
  either way. The follow-up commit lists a header in both no-surface arms,
  and each reason removed now fails the test: files mode
  `1 failed, 172 deselected in 0.54s`, the absent source root
  `1 failed, 172 deselected in 0.92s`;
- `_undeclared_case_findings` ignoring a declaration: the failing-test
  case, `1 failed, 172 deselected in 0.88s`;
- a tier's name in the rung table changed: the literal-mapping assertion,
  `1 failed, 11 deselected in 0.32s`, the derivation test still passing.

**Tests.**

- The 45 modules `trace.py --tests-for` names for the rows' modules
  (`kitlib/spine.py`, `gen_components.py`, `traj_views.py`,
  `gen_arch_map.py`, `gen_trajectory.py`, `spine_rules.py`,
  `traj_parse.py`, `traj_panels.py`, `arch_tags.py`, `arch_interfaces.py`),
  which include every test the edited test cases cite; the registry readers
  `test_id_watermark`, `test_id_landing`, `test_cell_classes` and
  `test_check_test_first`; and the whole-tree tests `test_dogfood_sync`,
  `test_import_layers` and `test_module_size_ratchet`:
  `1898 passed, 1 skipped, 18 warnings in 4515.10s (1:15:15)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 12 --basetemp D:/rt1048/t <the 52 modules listed>" rev="732d08500 (its tree before the commit)" -->
- The commit checks, `run_menu.py smoke`:
  `3717 passed, 3 skipped, 18 warnings in 593.77s (0:09:53)`. Its budget
  line reads CPU 852.8 s against 540, a WARN only, not charged to the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="732d08500 (its tree before the commit)" -->
- `trace.py --root . --strict`: `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. `scripts/check_resync.py`: "OK, no
  shipped path changed", so no RESYNC entry is owed. The build commit passed
  the hook (29 steps, all PASS).
- The follow-up commit (LLR-373's title and rationale, LLR-398's Detail,
  TC-474 and its test): the modules reading those rows and the registries,
  the changed test module, and the whole-tree tests, `test_trajectory_arch`,
  `test_if_owner_component`, `test_gen_components`,
  `test_components_registry`, `test_cell_classes`, `test_check_test_first`,
  `test_evidence_join`, `test_id_watermark`, `test_parent_first`,
  `test_rule_sync`, `test_trace_rules`, `test_trace_coherence`,
  `test_dogfood_sync`, `test_import_layers`, `test_module_size_ratchet`:
  `540 passed, 1 skipped, 18 warnings in 187.15s (0:03:07)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 12 --basetemp D:/rt1048/t <the 15 modules listed>" rev="3fa852a18 (with the follow-up's tree, before its commit)" -->
  `run_menu.py smoke`: `3717 passed, 3 skipped, 18 warnings in 128.86s (0:02:08)`,
  its CPU line 671.9 s against 540, a WARN only.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="3fa852a18 (with the follow-up's tree, before its commit)" -->
  `trace.py --root . --strict`: `orphans=0 integrity=0`;
  `check_trajectory.py --strict`: clean.
- Review round 1 (Hydrogen APPROVE; Sol's one MINOR, adopted):
  `kitlib.spine.module_components`' docstring drops its two caller-policy
  claims ("each caller intersects", "a rule reading the map treats a key
  with more than one as in no single component"), which the connectivity
  warns break, as does TC-435's evidence test docstring; a RESYNC_PACK.md
  entry anchored `[since 2474d7b4f]`; no behaviour change. The modules a
  docstring there can reach, `test_import_layers`, `test_dogfood_sync`,
  `test_components_registry`, `test_check_doc_refs`, `test_resync_pack`,
  `test_check_resync`, `test_module_size_ratchet`, `test_gen_arch_map`,
  `test_component_headers`, `test_gen_components`,
  `test_if_owner_component`, `test_policy_one_home`, `test_rule_sync`,
  `test_seam_resolution`, `test_seam_import_forms`, `test_evidence_join`:
  `417 passed, 1 skipped, 18 warnings in 130.27s (0:02:10)`;
  `trace.py --root . --strict`: `orphans=0 integrity=0`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 12 --basetemp D:/rt1048/t <the 16 modules listed>" rev="7096efadd (with the round's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched):
`docs/requirements/low-level-requirements.toml` 630,605 -> 631,471 (+866;
+586 at the build commit);
`docs/test/test-cases.toml` 681,090 -> 688,876 (+7,786; +7,547 at the build
commit); at review round 1, `project-trajectory/RESYNC_PACK.md`
745,116 -> 745,812 (+696) and `scripts/kitlib/spine.py` 74,218 -> 74,189
(-29).

**What the second sitting owes.** From this branch:

- Amendments (drifted `Accepted` rows): LLR-373 (Title, Detail and
  Rationale) and TC-081 (Method and Expected; its Evidence change routes as
  a traced cell). LLR-080's
  amendment, ruled MEANING and not blessed by WI-1047 because TC-081 was
  stale, is owed again, with TC-081 now matching it.
- First acceptance (`Drafted`, each with a verifying test case): LLR-393
  with TC-455; LLR-394 with TC-456; LLR-395 with TC-475; LLR-398 with
  TC-463 and TC-474.

Everything else WI-1047's sitting judged is owed unchanged by this branch:
the twenty amendments it ruled re-acceptable and the thirteen rows it ruled
ACCEPT, since its act was refused.

**Found and not changed** (outside this row's scope):

- `gen_arch_map`'s dependency diagram still draws a dotted seam edge for a
  row whose owner and far side name modules in the map (`_seam_edges`,
  pinned by `test_contracts_and_if_edges`). LLR-080's "draws imports only,
  since no row names a module" holds on every registry `trace.py --strict`
  passes, because LLR-041 makes a module-named endpoint a strict finding. I
  read that as no contradiction of LLR-080 and left the older arm.
- The flat How-SW graph now draws component nodes, but its legend lists
  only module, file and external actor.
- A question for later: should a files-mode adopter have its listed headers
  scanned? LLR-398 now states what the code does, that files mode (and an
  absent source root) leaves no contract-body surface, so a configuration
  file or registry header the scan profile lists is not held to one body
  per interface there. The header list exists to put such files on the
  surface, and files mode is the profile of a project whose source the
  symbol scan does not read, so an adopter in files mode may expect its
  listed headers checked. Changing that is a code and row change for its
  own work item, not this one.

## Context

Filed on trunk on 2026-11-22 from WI-1047's adjudication sitting (Gemini
Neon, verdict at `42df09628`). The sitting ruled 20 amendments re-acceptable
and 13 rows ACCEPT, but its act is refused: two amended `Accepted` LLRs it
ruled MEANING and would not bless still drift in the design registry the act
copies, and the snapshot will not absorb drifted text no act names
(SR-207). Until they are corrected and judged, no act can copy that registry,
and F-3's batch act cannot run. This row answers the verdict's findings, so
that a second sitting over everything still owed can accept it in one act.

**The two MEANING rows (blocking).**

- **LLR-373** (Accepted): its amended Detail says `gen_components` places
  seams by the files' `Component:` declarations. That contradicts its sibling
  LLR-199 and TC-435, which state that, since WI-1022, a seam is placed from
  its endpoint cells alone (component ids), even when the join answers an
  empty map. The fix is LLR-373's text: the join lists each component's
  modules; seams are placed from endpoints. Check the code agrees before
  changing a word.
- **LLR-080** (Accepted): its amended Detail renders interface seams in the
  dashboard view only, and the architecture map's dependency diagram draws
  imports only. Its one verifying test case, TC-081 (Accepted), was not
  updated and still asserts seams render in both views. The fix is TC-081's
  method and expected cells, matched to LLR-080 and to the tests it names as
  evidence.

**The six returned rows (Drafted; not blocking F-3).**

- **LLR-393, LLR-394, TC-455, TC-456** (WI-1014): each names implementation
  carriers (module, constant and function names) in its requirement text,
  against the brief's naming rules (§0, §3; the rule F-8, WI-1028, will
  enforce). Rewrite each as a contract that survives a refactor; traced
  cells (`module`, `code_symbol`, evidence) keep the names.
- **TC-463** (WI-1022): the only test case verifying LLR-398, it leaves five
  of LLR-398's clauses unverified: warn-plain versus fail-`--strict`
  gating, the `interfaces_check` opt-out, vacuity with no scan surface, the
  refusal of a body in a file with no `Contracts:` marker, and a listed
  Python file read through its docstring. Cover each, by extending TC-463 or
  by new `Drafted` test cases, each citing a test that exists (WI-1022's
  round fixes added several).
- **LLR-395** (WI-1019): returned because no test case verifies it. TC-428
  and TC-429 (Accepted) carry its evidence but verify SR-157 only, and the
  parent-first rule refuses re-pointing an accepted test case at a `Drafted`
  LLR, which is why WI-1038 waits for LLR-395's acceptance: a circle. Break
  it with a new `Drafted` test case verifying LLR-395, citing the tests of
  its rule, so both can be accepted together. Say in the Deliverable whether
  WI-1038 is still needed afterwards.

## Done-when

- [x] LLR-373's Detail states the join and the seam placement as the code
      does, consistent with LLR-199 and TC-435 (text only; it drifts).
- [x] TC-081's method and expected cells state LLR-080's rendering, and its
      evidence tests assert exactly that (text only; it drifts).
- [x] LLR-393, LLR-394, TC-455 and TC-456 name no implementation carrier in
      their requirement text.
- [x] TC-455's expected cell states its own observable pass condition for
      the rung-to-tier mapping and the holding behaviour, rather than
      deferring to LLR-393's detail (the verdict's second TC-455 finding).
- [x] Each of LLR-398's five clauses above is verified by a test case citing
      an existing test.
- [x] A `Drafted` test case verifies LLR-395, including its clause the
      verdict found uncovered: a validly declared test that still fails
      leaves its case clean under the undeclared-case rule; it cites the
      tests that show it.
- [x] `trace.py --strict` and `check_trajectory --strict` are clean; the
      Deliverable lists every row changed, what a second sitting owes, and
      whether WI-1038 is still needed or is superseded, with the reason.
