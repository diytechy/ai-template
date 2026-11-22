+++
id = "WI-1023"
title = "LLR rows lose their module, code_symbol and component cells; readers use the Implements index and placement is derived"
workstream = "process"
sr_refs = ["SR-157", "SR-180", "SR-186"]
specref = ""
needs = ["WI-1021", "WI-1022"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1023`, cut from `refactor_again` at
`3002931c7`, with the commit hooks on, and merged with trunk at `73aa095ce`
before the close. The specref (the review-churn plan's item 5) is cleared at
close, as a terminal row's is. The plan,
[plan.md](../../../../plans/WI-1023/plan.md), enumerates every reader of the three
cells from the code and says what each reads instead.

- `16e5dce34`: the plan.
- `19749ec70`: the schema and the loader's key rule, the Implements index and
  its readers, derived placement, SR-180's chain retired to its successors,
  the generated evidence column, the migration arm, the documents, the RESYNC
  entry, the tests and the regenerated views.
- `8e7d43c6f`: the merge of `refactor_again` at `73aa095ce` (WI-1042 and
  WI-1048), as the coordinator directed: every design row keeps trunk's text
  and status cells and this branch's removal of the three cells (LLR-257,
  LLR-373, LLR-393, LLR-394 and LLR-398 took trunk's text, the cells
  stripped); both lanes' test cases, trunk's first; both RESYNC entries,
  trunk's first, this branch's re-anchored at the merged base; the higher
  watermark in each space, then `--bump-ids` (nothing raised); trunk's
  generated views, then `trunk_step --regen`. No conflict of meaning.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The batch act is held for the operator** (Done-when 6; queue-drill HANDOFF
§3.3 N4). The lane stops at a green tip with the cells removed and asks for the
ruling **"trace cells removed, requirement text unchanged"**, to be recorded
once, here, over every `Accepted` design row: 344 at the tip (345 at the base;
LLR-180 retired since). The three cells are classed traced, so no accepted
text moved and no row reads as drifted; the act re-takes the approval
snapshot's design-row copy, whose 345 rows still carry the cells
(`intake.py snapshot --accepts "low-level-requirements.toml=<ref>"`). Until
it, that copy is read without the loader's key rule. No status moved, and
`intake.py snapshot` was not run.
<!-- fig: cmd="tomllib over docs/requirements/low-level-requirements.toml and its docs/archive/last_accepted copy" rev="8e7d43c6f" -->

**The schema and the loader** (Done-when 1; LLR-404, new). `module`,
`code_symbol` and `component` leave `kitlib.spine.SPINE_TIER_KEYS["LLR-ID"]`
and the shipped template's example row (its `detail` guidance now asks for
the observable obligation and names no file). `spine_carrier.load` refuses,
under the TOML carrier, any key a requirement tier's row sets that the tier
does not declare (need, system requirement, design row, test case; the
example row included), naming the file, the row and the key, as it already
refused an explicit empty cell and a nested table
(`undeclared_key_findings`). The legacy CSV carrier is the migrator's and is
not judged; an off-spine tier is not judged. The approval snapshot is read
with `declared=False` (`baseline_snapshot._tier_rows`), since its copy keeps
the cells until the batch act re-takes it. `trace.py`'s `REQUIRED_FIELDS`
drops `Module` and `CodeSymbol`, so `--strict-schema` no longer asks for them.

**The Implements index and the readers** (Done-when 2; LLR-405, new).
`arch_inputs.implements_index(root)` maps each spine id to the files whose
literal `Implements:` line names it, over `[paths] src` and `[arch-map]
headers`, read as text through `gen_arch_map.scan_backlinks` (286 of the 355
design rows are named at the tip). Every reader the plan enumerated reads it,
reads derived placement, or retired:

| Reader | Now |
|---|---|
| `kitlib.spine.resolve_modules` / `module_tests`, `trace.py --tests-for` (LLR-263) | the index (design-row ids only), of the repository holding `--docs`; exit 1 says no indexed file matches |
| `assumption_rules.module_srs` / `if_reached_srs` / `component_srs` (LLR-244) | the index; placement where no source is scanned; `check_assumption_gate` hands both in |
| `consolidate.touched_modules` (LLR-210) | the index's basenames |
| `intake` context block (LLR-153) | the code map names each row's indexed files and its placement or `unplaced`; packs and seams follow the placed components |
| `check_trajectory.knowledge_pack_findings` | placement (`_placed_sr_components`) |
| `gen_components` (LLR-199) | placement; `design_rows_unplaced` and `[unplaced] llr_refs` |
| `observation_cadence` `component:` trigger (LLR-293) | the `Component:` headers of the checked-out tree |
| the state view's design-row detail (`rendering/traj_views`, `traj_parse.placed_llrs`) | placement |
| `coherence` PB `Refs` (LLR-005, LLR-201) | retired: SR and LLR ids only |
| `coherence` LLR `Component` tag rule (LLR-201) | retired with the cell |
| `check_doc_refs` registry tier and symbol anchor (LLR-180) | the LLR row's `Module`/`CodeSymbol` leave the path scan; the anchor, its advisory, its unbound count and `gen_arch_map.module_bindings` retire |
| `arch_tags.codesymbol_crosscheck_findings` (no row; warn-only) | retired, with its re-exports and the warn |
| `gen_okf` design-row `**Code.**` line; the acceptance brief's `Module:`/`Component:` meta | retired (decisions record D-002) |
| `trace_text` artifact advisories | point at an `Implements:` tag in the file |
| `check_privacy`, `kitlib/secret_classes`, `lane` | prose naming a `code_symbol` cell, reworded; they read nothing |
| `migrate_carrier` CSV map and `--if-shape` | unchanged: the old formats' one home |

**Placement** (Done-when 3; LLR-403, new). `kitlib.spine.llr_placement(tcs,
ifs)` places, per (test case, design row) pair, each row a case verifies at
the owner of each interface the same case names, where that owner is a
component; an `external:` owner places nothing; a row placed at several is
placed at each. `unplaced_llrs` lists the rest. `trace.py` prints one
`placement:` line counting them (never an exit code) and the component view
lists them. At the tip: 119 placed (18 at several components), 236 unplaced;
the view's placed requirements fall from 133 to 73 with it.
<!-- fig: cmd="kitlib.spine.llr_placement over the worktree's registries; gen_components.render" rev="19749ec70" -->

**SR-180's chain** (Done-when 4). New, `Drafted`, phase 6: SR-248 (SN-002,
SN-003, B-09: a design row is discharged by the evidence of its kind, and
where it sits is derived); LLR-403 (placement and the unplaced count, SR-248),
LLR-404 (the loader's key rule, SR-157), LLR-405 (the index, SR-248), LLR-406
(the generated evidence column, SR-157), LLR-407 (the migration, SR-036);
TC-480 to TC-484. `retire.py` retired SR-180 (successor SR-248), LLR-180
(successor LLR-403) and TC-175 (successor TC-480), writing
`docs/log.d/retired/{SR-180,LLR-180,TC-175}.md`; it refused nothing.
IF-117 (`Drafted`, the anchor's binding oracle) is deleted with its body and
marker, its id spent under the watermark, and leaves `docs/if-tc-coverage-allow`
(seed 99 -> 98, its pinned set with it). `trace.py --root . --bump-ids`
moved SR 247 -> 248, LLR 398 -> 407, TC 467 -> 484; IF stays 326.

**The evidence column** (Done-when 5; LLR-406, new).
`arch_tags.generated_evidence` rewrites a cell's tests-root parts as the tags
make them (kept as written where tagged, a parametrized case included; an
untagged part dropped with its separator; a missing node appended, `; `-joined
and sorted), every other part, note and refused-file part verbatim.
`evidence_regen` reports the cells it would change; `trace.py
--regen-evidence` writes them (`write_evidence`, line by line, refusing
unless the result re-reads as the same rows with exactly those cells changed).
"Checked current" is LLR-366's equality check, which the generator turns into
the identity. Run over the base tree `3002931c7`, it changes **none of its
412 cells**: the generated cells equal today's on every row. In the build it
rewrote TC-197's cell, whose test this row renamed.
<!-- fig: cmd="arch_tags.evidence_regen over `git archive 3002931c7 docs tests` extracted" rev="3002931c7" -->

**The migration and the adopters** (Done-when 7; LLR-407, new).
`migrate_carrier.py --llr-trace-cells` removes the three cells in place,
multi-line values included, refusing unless the rewrite re-reads as the same
rows less those cells; `--check` reports. Run on this repository: 351 rows,
1053 lines removed, nothing else changed. The RESYNC entry "Design rows lose
their `module`, `code_symbol` and `component` cells; the code's tags name the
files and placement is derived [since 3002931c7]" gives the steps and the
adopter's batch act; `ADOPTING.md` §6 gains the note. `RUNTIME_FLOWS.template.md`
names participants by component or file; the performance-budget template's
`Refs` names SR and LLR ids. Shipped prose stating the column is reworded:
`PROCESS.md` (§1, the id table, §3 twice, §5, §8's one placement sentence,
§9, §10), `PROCESS_OPTIONS.md` (the component layer, the multi-module layer),
`EXAMPLE.md`, `README.md`, `KICKOFF_PROMPT.md`, `MULTI_REPO.md`, the spine
questions and the consolidation prompt (catalogue regenerated), the
spine-authoring skill and the coordinator recipes (all three copies). This
repository's `docs/registry-machinery-reference.md` and
`docs/enforcement-audit.md` follow.
<!-- fig: cmd="migrate_carrier.py --root . --llr-trace-cells; git diff --stat" rev="19749ec70" -->

**Acts owed** (for automated adjudication unless the operator's; this lane
flipped nothing):

- **the operator's batch act**, above;
- the SR-180 chain's retirement: SR-180, LLR-180 and TC-175, all `Accepted`,
  removed from the live registries with records naming SR-248, LLR-403 and
  TC-480;
- text-only amendments of `Accepted` rows the build made untrue, drifting:
  LLR-005 (PB `Refs` against ids only), LLR-153 (the context block's code map
  and placed components), LLR-198 and LLR-217 (sentences naming the `Module`
  cell or comment), LLR-199 (placement in the component view and the unplaced
  table), LLR-201 (PB `Refs`; the LLR component arm), LLR-210 (the shared-file
  signal through the index), LLR-244 (`module_srs`, `if_reached_srs` and the
  files-mode reach), LLR-263 (the listing through the index, its detail and
  its rationale), LLR-293 (the
  `component:` trigger reads the headers); SR-212 (acceptance: "through the
  files its design rows' back-links are in"; its `Hat-Refs` left as they are,
  deliberately, since no perspective changes); TC-195, TC-197, TC-239 and
  TC-258 (method or expected). TC-197's `evidence` cell was regenerated, a
  traced change;
- first acceptance of SR-248, LLR-403 to LLR-407 and TC-480 to TC-484.

`Drafted` and owing none: TC-460 (expected), the interface rows IF-028,
IF-104, IF-131, IF-231, IF-233 and IF-316 (text naming the retired cells or
the old signatures), and IF-117, deleted. Read and left, since no sentence of
theirs names a retired cell: LLR-038, LLR-039, LLR-166, LLR-225, LLR-366
(its equality check is what holds the generated column current), SR-221,
TC-147 (its `Module`-only move still classes traced), TC-306.

**Tests.**

- Red before the code: `tests/test_llr_trace_cells.py` as first written, `5
  failed in 0.68s`; green with the code, `5 passed in 8.08s`.
  <!-- fig: cmd="python -m pytest tests/test_llr_trace_cells.py -q" rev="the worktree before the code, then after it, ahead of 19749ec70" -->
- The first batch of importing modules, before their fixtures moved: `34
  failed, 437 passed, 1 skipped, 18 warnings in 330.11s (0:05:30)`, every
  failure a fixture of the old shape (a design row carrying the cells, a TC or
  SN fixture row carrying a key its tier never declared, the old module
  listing), each rewritten.
  <!-- fig: cmd="python -m pytest -q -n auto <thirteen modules>" rev="the worktree ahead of 19749ec70" -->
- The full unfiltered suite: `66 failed, 8199 passed, 31 skipped, 18 warnings
  in 7363.62s (2:02:43)`. 33 (`test_dispatch` and `test_loop_provenance`)
  refused because scripts were edited while the run held them ("coordinator
  Python changed after this process imported it"), not this row's; 13
  (`test_stack_profile`, `test_intake_settled`) were fixtures already rewritten
  while the run held the old ones; the rest were old-shape fixtures, the
  goldens, the size ratchet, and two readers of history (below). The sixteen
  modules again after their fixes: `17 failed, 857 passed in 907.17s
  (0:15:07)`, then each fixed.
  <!-- fig: cmd="python -m pytest -q -n auto" rev="the worktree ahead of 19749ec70" -->
- Every edited module with every module importing a changed one that had
  failed, `test_dispatch`, `test_loop_provenance` and the whole-tree tests
  (`test_import_layers`, `test_module_size_ratchet`, `test_dogfood_sync`,
  `test_complexity_ratchet`, `test_smoke_budget`, `test_skills_sync`): `1
  failed, 1579 passed, 1 skipped, 18 warnings in 1038.10s (0:17:18)`, the one
  `test_derive_stage`'s committed-stage pin before the regeneration; after it,
  `31 passed in 118.70s (0:01:58)`. `test_old_kit_resync`: `8 passed in
  86.64s (0:01:26)`.
  <!-- fig: cmd="python -m pytest -q -n auto <thirty-six modules>; python -m pytest -q tests/test_derive_stage.py tests/test_old_kit_resync.py" rev="the worktree ahead of 19749ec70" -->
- `run_menu.py smoke` before the build commit: `trace.py --strict`
  `orphans=0 integrity=0`, `component-findings=0 interfaces=239
  interface-findings=0`; `check_trajectory.py --strict` clean (`1045 work
  item(s), 915 done (88%), 35 cancelled, graph acyclic`); `check_resync: OK,
  37 shipped path(s) changed; entry anchored at 3002931c7`; the tier `3721
  passed, 3 skipped, 18 warnings in 130.61s (0:02:10)`, its CPU 650.5 s over
  540 the report-only WARN on a loaded box. The commit hook over `19749ec70`:
  `RESULT: PASS`.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="19749ec70 (its tree before the commit)" -->
- After the merge: the modules the merge reaches (`test_check_test_first`,
  `test_components_registry`, `test_gen_arch_map`, `test_spine_rules`,
  `test_traj_views`, `test_trajectory_arch`, `test_derive_stage`,
  `test_baseline_snapshot`, `test_llr_trace_cells`, `test_dogfood_sync`,
  `test_import_layers`, the two ratchets, `test_smoke_budget`,
  `test_check_resync`, `test_resync_pack`, `test_id_watermark`,
  `test_trace_golden`, `test_evidence_join`, `test_phase_rule`): `797 passed,
  1 skipped, 18 warnings in 260.45s (0:04:20)`. The merge commit's hook:
  `RESULT: PASS`. `run_menu.py smoke` over `8e7d43c6f`: `trace.py --strict`
  `orphans=0 integrity=0`; `check_trajectory.py --strict` clean (`1045 work
  item(s), 917 done (88%), 36 cancelled, graph acyclic`); `check_resync: OK,
  37 shipped path(s) changed; entry anchored at 73aa095ce`; the tier `3721
  passed, 3 skipped, 18 warnings in 100.13s (0:01:40)`, CPU 616.2 s the
  report-only WARN.
  <!-- fig: cmd="python -m pytest -q -n auto <twenty modules>; python project-trajectory/scripts/run_menu.py smoke" rev="8e7d43c6f" -->

**Byte deltas.** `PROCESS.md` 101,959 -> 102,060 (+101, watched: §8's one
placement sentence, the id table and four column mentions); `PROCESS_OPTIONS.md`
202,446 -> 202,593 (+147, watched); the byte-budget skill 4,623 -> 4,603 (cap
5,000; its two watched rows re-stamped, three copies); `RESYNC_PACK.md`
748,241 at trunk -> 752,486 (unbudgeted); `EXAMPLE.md` 33,241 -> 33,375 and
`ADOPTING.md` 24,512 -> 25,040 (unbudgeted). `CLAUDE.md` and
`AGENTS.template.md` unchanged.

**Deviations from the plan.**

- `spine_carrier.SPINE_COLUMN` keeps mapping `module`, `code_symbol` and
  `component` (the plan said the first two leave): an unmapped key reads under
  its lowercase name, which the traced-cell table does not class, so the
  snapshot and history would read as accepted-text drift (decisions record
  D-003).
- The evidence regeneration is a command, not a `trunk_step --regen` step
  (decisions record D-001); the OKF `**Code.**` line and the acceptance
  brief's meta retire rather than read the index (D-002).
- Two readers of history went through the live loader, and the full suite
  showed it: the stage's before-side (`derive_stage._spine_at`, the phase rule
  the commit hook runs) and the id sweep (`trace._spine_ids`, which the landing
  check runs at the parent revision). Both read without the key rule now
  (`spine_rules.load_spine(declared=False)`); LLR-404 and TC-481 say so, and
  the test covers both.
- The deny-by-default rule also refuses keys an older kit's adopter carried
  unread: `test_old_kit_resync` now models the documented path
  (`migrate_vocabulary.py` for the SR `Verification` column, the `Aspect`
  entry for `Area`, then `--llr-trace-cells`), and the RESYNC entry names it.
- `placement_line` lives in `trace_text` and the icicle's placement in
  `traj_parse.placed_llrs`, keeping `trace.py` and `rendering/traj_views.py`
  inside their size lines; TC-482 verifies LLR-405 and LLR-263 and no SR (the
  triangle rule).
- Ratchets: `trace.py` 3780 -> 3788, `intake.py` 1939 -> 1946,
  `check_trajectory.py` 1656 -> 1663 (reviewed bumps, reasons in the
  baseline), `gen_arch_map.py` 1671 -> 1654 (down); C901: the crosscheck's
  entry deleted, `gen_okf.emit` 25 -> 24, `trace.acceptance_lines` 27 -> 24;
  cognitive: four rows deleted and five re-stamped down, the rest of the
  census untouched. `render_console`'s gating print went to `_print_gating`,
  `llr_placement`'s per-case step to `_case_places`, and the pack join to
  `_placed_sr_components`. The smoke tier's `max-tests` 3720 -> 3740 (the
  five new in-process cases less one retired, reason in `docs/stack.ini`).
- `tests/test_interface_owner_reach.py` is deleted: its one case pinned the
  module-key reading the PB targets used. The trace and page goldens are
  regenerated deliberately (the `placement:` line; `Placed:` for `Module:`).
- The RESYNC entry is anchored at `73aa095ce`, the merged base, as
  `check_resync` requires after the merge.

**Review** (the coordinator, 2026-11-22; queue-drill HANDOFF §4 step 4).
Round 1 over `73aa095ce..bcbc00bd6`, the generated views, the plan and this
spec's copies withheld and the spec at the tip given whole; the design
registry's diff was given as the base with the three cells stripped (checked
row for row with tomllib) against the tip, the eight dogfood skill copies as
notes (byte-equal to the kit's). OpenAI Sol (`gpt-6.1-sol`, low) read it in
two halves (code 94 s, registries and documents 54 s); Gemini Hydrogen
(`gemini-4-hydrogen-low`, the Antigravity CLI) read the prose: APPROVE, no
findings, the D3 question put to both by name. Sol raised four distinct
findings, each confirmed by reading and adopted: the migration turned CRLF
into LF against LLR-407's "every other byte" (raised MAJOR by both halves,
regraded MINOR, since adopters carry the kit's `eol=lf` attributes); it did
not handle a multi-line literal string; SR-248 and LLR-403 omitted the
`Drafted` exemption of the no-test rule; LLR-263's rationale still named the
retired cell. The coordinator added two from the second adjudication
sitting (WI-1049), which refused to bless amendments that add code names:
this branch's LLR-244 and LLR-263 rewrites added parameter names to call
signatures. All six answered in `4c105adf0`: the migration reads bytes and
tracks both delimiters (red first, `2 failed, 5 deselected`); SR-248 and
LLR-403 exempt a `Drafted` row and TC-480 cites the test of both sides;
LLR-244 and LLR-263 restated without signatures; TC-484 covers the two new
tests. Over the 18 affected modules `567 passed, 2 skipped in 112.38s`;
`trace.py --strict` and `check_trajectory --strict` clean. Round 2 narrow
over `bcbc00bd6..4c105adf0`: Sol and Hydrogen both APPROVE, no findings.

**At the merge into trunk:** trunk reverted LLR-244's `detail` to its
accepted text by the operator's ruling (2026-11-22, `0333b64f0`, so WI-1049's
act could be taken); this branch's LLR-244, which states F-2's and this
row's behaviour without code names, is taken over it. **Left stale, not
amended here:** SR-221 (`Accepted`) still says "for a module a design row
names"; it is WI-1018's kind (row text a lane leaves stale), noted there.

## Context

Variant F's third row (F-3), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). It is item 5's layer 1 ("make it unrepresentable in the
schema", owner ruling 2026-10-11, ruling 5), with revision 35's overruling
of "LLRs keep naming their component by id": LLR → CMP retires and
placement is derived.

Today all 347 LLR rows (345 `Accepted`) carry `module`, `code_symbol` and
`component`. `trace.py --strict-schema` requires the first two, and
`check_doc_refs --strict` binds the symbol. SR-180, LLR-180 and TC-175 state
that a design row is discharged only by a realization symbol that resolves:
the binding this row removes. The cells' readers include
`kitlib/spine.py`, `spine_carrier.py`, `migrate_carrier.py`, `trace.py`,
`check_doc_refs.py`, `check_privacy.py`, `kitlib/secret_classes.py`,
`lane.py`, `coherence.py`, `intake.py`, `acceptance_record.py`,
`gen_components.py` and the dashboard renderers; the lane's plan enumerates
them from the code, since a name match over-counts.

**Two down-pointing traced cells, one act.** The TC `evidence` cell's
test-file parts are already held equal to the test files' TC tags in both
directions (LLR-366). Ruling 8 (revision 8) and revision 35 make them
generated from those tags; CI workflows, inspection and review records stay
authored. They ride this row because both are layer 1 and both are covered
by the one batch act below.

**The batch act is the operator's (HANDOFF §3.3 N4).** Removing three cells
from 345 accepted rows is "trace cells removed, requirement text unchanged":
one ruling, recorded once, never 345 re-attestations. Every other act this
row creates (the SR-180 chain's retirement, the successor rows, amended
text) goes to automated adjudication; the lane lists them and flips nothing.

**SR-180's successor (F point 6, revision 18).** The discharge rule is
restated per evidence kind: a TC verifies the LLR; where the LLR constrains
an interface, the effective-contract reader returns a valid realization
(WI-1025 adds that clause); otherwise it is placed through its TC or
counted unplaced. New ids carry it; SR-180, LLR-180 and TC-175 retire with
a successor record (keep-or-mint, revision 26). This row mints one SR, its
LLRs and TCs, `Drafted`, from ranges the coordinator sets at launch (the
drill expects no SR mint without one).

**"Module" retires as a spine term (revision 35).** Shipped text that uses
it as a spine unit where this row removes the column is reworded:
`RUNTIME_FLOWS.template.md` (participants from the LLR `Module` column) and
the performance-budget template's `Refs`.

## Scope answers

- **S1.** Deliverables, in landing order on one branch: (1) the schema
  change, readers on the index and derived placement; (2) the SR-180
  chain's successor; (3) TC evidence generated. Kept together: one batch
  act covers (1) and (3), and (2)'s oracle is removed by (1).
- **S2.** No new authority: the index replaces cells as the input to
  existing checks.
- **S3.** The loader refuses any key a requirement tier does not declare
  (deny by default). The evidence generator reads the existing tag grammar
  and rewrites only the parts LLR-366's reader rule binds to the declared
  tests root; parts outside it and parenthetical notes are kept verbatim.
- **S4.** `single`: many script families, a schema and a migration.
- **S5.** Placement becomes an output derived from new inputs (interface
  owners; WI-1024 adds `constrains`). SR-180, LLR-180 and TC-175 are
  re-cut (PROCESS.md §5).
- **S6.** `needs` WI-1021: file membership no longer comes from LLR cells;
  WI-1022: placement derives through an interface's owner component. No new
  package, tool or service.
- **B4.** The batch act is held for the operator (Done-when 6).

## Done-when

- [ ] `module`, `code_symbol` and `component` leave the LLR schema in
      `kitlib/spine.py` and the template; the loader refuses a key a
      requirement tier does not declare, naming the row and the key.
- [ ] Every reader of the removed cells reads one index generated from the
      `Implements:` tags instead, or retires. `--strict-schema` and
      `check_doc_refs --strict` no longer require or bind them.
- [ ] An LLR's placement is derived: the owner component of an interface
      its verifying TC names (WI-1024 adds `constrains`). An LLR with
      neither is listed as unplaced and counted, not refused; one placed
      at several interfaces is placed at each. The views read placement.
- [ ] SR-180, LLR-180 and TC-175 retire with a successor record; a new SR,
      LLR and TC state the per-evidence-kind discharge rule, `Drafted`.
- [ ] Each TC `evidence` cell's test-file parts (the parts LLR-366's reader
      binds to the declared tests root) are generated from the test files'
      TC tags and checked current; parts outside the tests root, other
      evidence kinds and parenthetical notes stay authored, kept verbatim.
      The generated cells equal today's on every row.
- [ ] The batch act is held: the lane stops at a green tip with the cells
      removed and asks the operator for the ruling "trace cells removed,
      requirement text unchanged", recorded once in the Deliverable. It
      takes no other act, flips no status and runs no snapshot; the
      Deliverable lists every act owed for adjudication.
- [ ] A migration script removes the cells from an adopter's registries
      (`migrate_carrier.py` is the precedent), and a RESYNC entry (variant
      F, after WI-1022's) gives the steps and the `ADOPTING.md` note.
      `RUNTIME_FLOWS.template.md` and the performance-budget template stop
      naming a `Module` column.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; every
      test importing a changed module runs green, plus
      `test_import_layers`, `test_module_size_ratchet` and
      `test_dogfood_sync`.
