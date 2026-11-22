# WI-1023 plan: LLR rows lose their trace cells; readers use the Implements index and placement is derived

Planned on branch `maint/wi-1023` at `3002931c7`, cut from `refactor_again`
at the same commit. A maintenance-branch build (`planmode = "single"`): no
plan critique or pass record. Counts are read from the tree at `3002931c7`:
351 LLR rows (345 `Accepted`, 6 `Drafted`), every one carrying `module`,
`code_symbol` and `component`; 281 of them are named by an `Implements:` tag
under `[paths] src`; 412 TC rows, every `evidence` cell made of test-file
parts (`;`, `; ` or a space between them; no parenthetical note; 8 parts
outside the tests root).

## 1. The schema (Done-when 1)

- `kitlib.spine.SPINE_TIER_KEYS["LLR-ID"]` drops `module`, `code_symbol` and
  `component`; the shipped template's example row drops the three keys and
  the `component` comment block, and its `detail` guidance stops asking for a
  module and symbol.
- **Deny by default.** `spine_carrier.load` refuses, under the TOML carrier,
  any key of a requirement tier's row (`SN-ID`, `SR-ID`, `LLR-ID`, `TC-ID`:
  the tiers `SPINE_TIER_KEYS` declares) that the tier does not declare,
  naming the file, the row and the key, as it already refuses a nested table
  and an explicit empty string (`undeclared_key_findings`). The CSV carrier is
  the legacy one: its columns are a header, not a row's keys, and the
  migrator is its one home, so it is not judged here (decisions record).
- **The approval snapshot is read without the key rule.** Its copy is the
  act's record, written by an act and editable only by one; until the batch
  act it carries the three cells. `baseline_snapshot._tier_rows` reads it
  with the rule off (`load(..., declared=False)`); every live read keeps it.
- `acceptance_record.SPINE_TRACED_CELLS` keeps `Module`, `CodeSymbol` and
  `Component` classed traced for the LLR registry, with a comment saying why:
  the snapshot copy and every git revision before this row still carry them,
  and an unclassed column reads as accepted, so dropping the names would make
  all 345 accepted rows drift and the amend-without-flip guard warn on each.
  The removal is a traced change, which is what the batch act records.
- `spine_carrier.SPINE_COLUMN` drops `module` and `code_symbol`; `component`
  stays mapped (the IF tier's retired-cell finding reads it).
- `trace.py` `REQUIRED_FIELDS["LLR"]` drops `Module` and `CodeSymbol`, so
  `--strict-schema` no longer asks for them.

## 2. The Implements index (Done-when 2)

One home: `arch_inputs.implements_index(root)` returns `{spine id: [file,
...]}`, repository-relative and sorted, from `gen_arch_map.scan_backlinks`
over the declared source root (`[paths] src`) and the `[arch-map] headers`
files. Text, not AST, so it holds in `files` mode too. `kitlib.spine` takes
the index as an argument where it needs it (it imports no sibling).

The readers, enumerated from the code (a name match over-counts: the
`check_privacy.py`, `kitlib/secret_classes.py` and `lane.py` hits are prose
naming a row's `code_symbol` cell, reworded here and reading nothing):

| Reader | Today | After |
|---|---|---|
| `kitlib.spine.resolve_modules`, `module_tests`; `trace.py --tests-for` (LLR-263) | design rows whose `Module` names the file | design rows the index names for the file; `--tests-for` reads the index of the root above `--docs` |
| `assumption_rules.module_srs` (LLR-244 reach) | `{module: SRs}` from `Module` | `{file: SRs}` from the index; `component_srs` (files mode) reads derived placement |
| `coherence.llr_module_ids` (PB `Refs`, LLR-005, LLR-201) | an LLR `Module` path is a PB target | retires: a PB row's `Refs` names SR and LLR ids only |
| `coherence.component_membership_findings` (LLR-201) | an LLR `Component` tag must name a CMP | the LLR arm retires with the cell |
| `check_doc_refs.SPINE_CELLS`, `symbol_findings` and its helpers (LLR-180) | binds `CodeSymbol` in `Module` under `--strict` | the LLR pointer cells leave the path scan (`TestRefs` stays); the symbol anchor retires with SR-180's chain (section 4) |
| `gen_arch_map.module_bindings`, IF-117 | the anchor's binding oracle | retires; IF-117 (`Drafted`) is deleted and its id spent, its body and marker leave `gen_arch_map`, and its TC citations drop it |
| `arch_tags.codesymbol_crosscheck_findings` (no row; warn-only) | holds each tag site to `Module`/`CodeSymbol` | retires with the cells; `trajectory_arch` and `check_trajectory` drop the re-export and the warn |
| `consolidate._llr_modules` (LLR-210) | basenames of the `Module` cells the SRs reach | basenames of the files the index names for the SRs' design rows |
| `intake._code_map_lines` (LLR-153) | `[Module :: CodeSymbol]` | the files the index names, or `(no Implements: tag)` |
| `intake._pack_lines`, `_seam_lines` (LLR-153) | the rows' `Component` cells | derived placement; the unplaced rows listed as unplaced |
| `check_trajectory.knowledge_pack_findings` | `LLR.Component` -> packs | derived placement -> packs |
| `gen_components._add_members` (LLR-199) | `Component` cells place the rows | derived placement; `design_rows_unplaced` and `[unplaced] llr_refs` list and count the rest |
| `observation_cadence._component_paths` (LLR-293) | `Module` of the component-tagged rows at two revisions | the files whose `Component:` header declares the component, read from the tree (`arch_inputs.component_headers`, the WI-1021 membership) |
| `rendering/traj_views` LLR icicle meta | `Module: <cell>` | `Placed: <CMP ids>` or `Placed: unplaced` |
| `gen_okf` LLR page | `**Code.** <module> — <symbol>` | `**Implemented in.**` the index's files, omitted when none |
| `trace.py` acceptance brief `llr_block` | `Module:` / `Component:` meta | retires: a sitting judges text, and placement is the view's |
| `trace_text` advisories (SR, SN artifact) | "move it to the LLR Module cell" | "an `Implements:` tag in the file" |
| `migrate_carrier` CSV map, `_llr_single_modules` | old-format conversion | unchanged: the migrator is the old formats' one home (D3) |

## 3. Placement (Done-when 3)

One home, pure, in `kitlib.spine`: `llr_placement(tcs, ifs)` returns `{LLR id:
sorted CMP ids}`. Per (TC, LLR) pair: each LLR a TC's `Verifies` names is
placed at the owner of each IF the same TC names, where that owner is a
`CMP-###` id; an `external:` owner places nothing. One placed at several
interfaces is placed at each. `unplaced_llrs(llrs, placement)` returns the
sorted rest. WI-1024 adds `constrains` as a second input; nothing here
pre-empts it. At `3002931c7`: 119 placed (18 at several components), 232
unplaced.

`trace.py` prints one advisory count line, `placement: N design row(s) placed,
M unplaced` (outside every exit code: unplaced is counted, never refused),
and the component view lists them. The views that read placement: the
component view, the icicle meta, the intake context, the knowledge-pack warn,
the reach fallback.

## 4. SR-180's chain (Done-when 4)

New, `Drafted`, minted from the launch ranges:

- **SR-248** (SN-002, SN-003, B-09, like SR-180): a design row is discharged
  by the evidence of its kind: a test case verifies it (an executable case
  through its tagged tests, or an inspection, analysis or attestation with its
  declared evidence); where it constrains an interface, the interface's
  realization is read from the code (WI-1025's clause, named and not built
  here); otherwise it is placed through the interfaces its verifying cases
  name or listed and counted as unplaced, never refused. Its realization and
  placement are derived from the code and the rows, never stated on the row.
  The back-link stays encouraged, never obliged.
- **LLR-403** (SR-248): derived placement, the unplaced list and count, and
  the reading of discharge (the orphan rule reports a row no case verifies).
- **LLR-404** (SR-157): the loader's deny-by-default key rule.
- **LLR-405** (SR-248): the Implements index and the readers it feeds.
- **LLR-406** (SR-157): the generated evidence column (section 5).
- **LLR-407** (SR-036): the migration arm (section 6).
- **TC-480** to **TC-484**, one per new LLR, `Drafted`.

`retire.py` retires SR-180 (successor SR-248), LLR-180 (successor LLR-403)
and TC-175 (successor TC-480), writing the records under
`docs/log.d/retired/`. If it refuses an `Accepted` row, the lane stops and
reports. `trace.py --root . --bump-ids` follows.

## 5. The evidence column (Done-when 5)

`arch_tags.generated_evidence(cell, tagged, tests_dir, refused)`: the cell's
parts outside the tests root, its parenthetical notes and the parts in a file
refused as unreadable are kept verbatim, as are the tests-root parts a tag
declares (a parametrized case included, read as LLR-366 reads it); a
tests-root part no tag declares is dropped with its separator; a declared node
the cell lacks is appended, `; `-joined, sorted. `evidence_regen(root,
tests_dir)` returns `{TC: (before, after)}` for the cells it would change.
`trace.py --regen-evidence` writes them in place, line by line (the
`intake._flip_status_lines` pattern: multi-line strings tracked, every other
byte kept). `trunk_step --regen` runs it first, ahead of the OKF bundle, which
reads the cells. "Checked current" is LLR-366's existing equality check: the
generator is the identity exactly when the parts equal the tags. At
`3002931c7` it changes no cell ("equal today's on every row").

## 6. The migration and the adopters (Done-when 7)

`migrate_carrier.py --llr-trace-cells` removes `module`, `code_symbol` and
`component` from every `[design.*]` table of
`docs/requirements/low-level-requirements.toml`, multi-line values included,
in place; it re-parses the result and refuses unless every other cell is
unchanged; `--check` reports without writing. Run on this repository it is
the removal itself. The RESYNC entry (variant F, after WI-1022's) gives the
steps, the PB `Refs` change and the batch act an adopter owes; `ADOPTING.md`
gains the note. `RUNTIME_FLOWS.template.md` names participants by component
or file; the performance-budget template's `Refs` names SR and LLR ids.
Shipped prose stating the column (`PROCESS.md`, `PROCESS_OPTIONS.md`,
`EXAMPLE.md`, the spine-authoring skill, the spine questions, the
coordinator recipes, `README.md`, `KICKOFF_PROMPT.md`, `MULTI_REPO.md`, the
consolidation prompt) is reworded where it says the column exists.

## 7. Rows amended (text only; acts owed)

`Accepted`, drifting for adjudication: LLR-005 (PB `Refs`), LLR-153 (the
context block's code map and components), LLR-198 and LLR-217 (sentences
naming the `Module` cell), LLR-199 (placement), LLR-201 (PB `Refs`, the LLR
component arm), LLR-210 (the shared-file signal), LLR-244 (reach), LLR-263
(the listing), LLR-293 (the component trigger); TC-197 (PB `Refs`), and the
TCs whose method, expected or evidence the build makes untrue, found as the
tests move. `Drafted` beside them: TC-460, TC-466. Each list is final in the
Deliverable.

## 8. Tests

Red first: `tests/test_llr_trace_cells.py`, one test per new TC (placement
per pair, multi and external; the unplaced count in the report and the
view; the loader's refusal and the snapshot exception; the index and
`--tests-for`; the generator's keep, drop and append, and the live registry
unchanged; the migration arm). Then every module importing a changed module,
the four whole-tree tests and `run_menu.py smoke`.

## 9. Acts owed (for the Deliverable)

The batch act, the operator's ruling "trace cells removed, requirement text
unchanged", over every `Accepted` LLR; the SR-180 chain's retirement; the
section 7 amendments; first acceptance of SR-248, LLR-403 to LLR-407 and
TC-480 to TC-484.
