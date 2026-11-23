+++
id = "WI-1056"
title = "WI-1055's verdict answered: F-3's five unblessed rows re-landed under an amended SR-221, and SR-248's chain repaired"
workstream = "process"
specref = ""
sr_refs = ["SR-036", "SR-157", "SR-212", "SR-221", "SR-248", "SR-249", "SR-250", "SR-251"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1056`, cut from `refactor_again`
at `3c33b3783`, with the commit hooks on, under the plan
`docs/plans/WI-1056/plan.md` and the coordinator's go-ahead, which approved
it with two corrections: SR-221's and LLR-263's titles say "file" where they
name what the listing is for, and LLR-405 cites LLR-204's declaration
grammar without restating it. No status moved and no act was taken. Ids
minted from the launch range and recorded with `trace.py --bump-ids`:
SR-249, SR-250, SR-251, LLR-408 and TC-485 (SR-252, LLR-409 to LLR-412 and
TC-486 to TC-495 unused). The three new requirements join this row's
`sr_refs`. No decisions record: every choice made is stated by a spine row.
The specref (WI-1055's verdict) is cleared at close, as a terminal row's is.

- `9548c30c1`: the plan.
- `cbe6aab2f`: the build: rows, code, tests, regenerated evidence and views,
  the id watermark, the RESYNC entry and WI-1018's sentence.
- `08639915b`: the trajectory composer re-exports
  `arch_tags.evidence_input_missing` again (the composer test found it
  dropped by the report's move into `arch_tags`).
- `150d7f955`: this close-out.
- The commit after it: review round 1's finding (OpenAI Sol, MAJOR,
  adopted by the coordinator) answered. TC-481's existing test now asserts
  the registry file, the row and the key for the system-requirement and
  test-case refusals too, as for the design and need tiers, with three
  mutation proofs in the table below; TC-481's text was not changed, since
  it no longer overstates.

**1. SR-212, LLR-244 and TC-239.** SR-212's `acceptance_criteria` defines
the architecture rung's reach as LLR-244 states it: a boundary interface
reaches the requirements of the design rows realized in the one file stating
its contract body (the files realizing a row being those its back-link
declarations are in); an interface whose contract body no file states
reaches none; where no source is scanned, an interface reaches the
requirements of the design rows placed in its owner component. Its pass and
fail conditions are unchanged. LLR-244's `detail` is `8e08b3029`'s, with
every code name the accepted text and `8e08b3029` carried (the two arms'
functions, the harness script, the two step names) replaced by what each is.
TC-239's `method` is `8e08b3029`'s, scrubbed the same way, plus the two
scenarios; its `expected` gains their two outcomes. Two tests in
`tests/test_assumption_gate.py`, whose module tag is TC-239's, drive the
architecture arm's step on a scaffold: a boundary interface whose body no
file states reaches nothing (the requirement fails as unreached and the
interface is not named), and the same fixture with the scan profile reading
files only reaches the requirement through the design row placed in the
interface's owner component (the requirement fails naming the interface).
Each child now states only what its parent states:

| LLR-244 clause | SR-212 acceptance, amended |
|---|---|
| reach through the one file stating the body and the back-link index | "the design rows realized in the one file stating its contract body ... back-link declarations" |
| an interface with no body reaches none | "an interface whose contract body no file states reaches none" |
| no source scanned: owner-component placement | "where no source is scanned ... placed in its owner component" |
| the judging rules, advisory with the gate off, the boundary arm | unchanged clauses |

**2. SR-221, LLR-263 and TC-258; WI-1018.** SR-221's `title`,
`requirement`, `acceptance_criteria`, `rationale` and `coincident` say the
listing is for a file whose back-link declarations name a design row, read
by joining those declarations with the test-case registry and with no
hand-kept map; "for a module a design row names" and "derived from the
registries" are gone. LLR-263's `title` ("The file listing: a file's design
rows, ..."), `detail` (`8e08b3029`'s, the stack profile named as such
rather than by its file) and `rationale` (its opening sentence now "SR-221
asks for the tests the spine links to a file, read through the code's
back-links with no hand-kept map") are re-landed under it. TC-258's
`method` and `expected` are `8e08b3029`'s with the command, its flags and
the module names replaced by contract terms; its seven tests already drove
the file listing and are unchanged. Upward: the file listing, every status,
resolution by path, suffix or stem with exits 1 and 2, the registries and
profile from the docs directory with the back-links from the repository
holding it, and "runs no check" each match SR-221's amended acceptance
clause for clause. WI-1018's Context now says SR-221 joined its first set
and left it the same day, so the set excludes it; its `sr_refs` never named
it.

**3. SR-248's chain.** SR-248 keeps discharge alone: one `shall` ("report
as undischarged each design-tier row past its Drafted status that no live
test case verifies"), `sn_refs` SN-002, and no unbounded absolute (the
strict check "exits nonzero" for an undischarged row). SR-249 (new, SN-002
and SN-023) states placement, its acceptance bounded as "a row's being
unplaced changes no check's exit code". SR-250 (new, SN-002 and SN-003)
states the back-link reading LLR-405 serves: no existing requirement stated
it (SR-163 and LLR-204 own the grammar, not which files realize a row).
LLR-403 re-points to SR-249 and states one decision, placement; its
consumer list is cut to the readers TC-480 verifies: the component view's
listing and census, the state view's design-row detail, and the strict
check's count line, which names the first ten unplaced rows and counts the
rest. The build brief and the knowledge-pack advisory are LLR-153's
statements, the no-source-scanned gate reach LLR-244's. The discharge clause
moves to LLR-408 (new, SR-248), which names LLR-201 as the cross-row pass
that runs it ("an LLR its SR parent and TC") and states what that pass
requires of a design row; LLR-201, TC-197 and LLR-201's `sr_refs` are
untouched. TC-485 (new) verifies SR-248 and LLR-408; TC-480 verifies SR-249
and LLR-403. The new requirements carry no `form`, as SR-248 did not, so
the interface-form gates do not judge them, and each records a coincident
argument; the three assumption-gate steps report 0 findings with the gate
on.

**4. LLR-405 and TC-482.** LLR-405 re-points to SR-250. Its `detail` cites
the grammar ("a back-link declaration, as LLR-204's grammar reads one")
without restating its rules, and states what LLR-405 adds: the index over
the source root and the listed headers, read as text and generated on every
read; with the source root absent the listed headers' declarations remain;
a file that cannot be read as text (its bytes not decoding, or its read
failing) and a listed header that is not a file contribute nothing while
the rest is indexed; and the build brief's code map marks a row the index
lacks as having none. Its reader list is cut to the build brief: the file
listing is LLR-263's own statement, the gate's reach LLR-244's, the
consolidation census LLR-210's. TC-482 verifies SR-250, SR-221, LLR-405 and
LLR-263; SR-221 joined so that each design row the case names descends from
a requirement it names, as the SR and design-row pairing rule requires.
TC-482's existing prose-mention case still shows the grammar at work.

**5. LLR-406 and TC-483.** LLR-406 sits under SR-251 (new, SN-002): on
request, the parts of each test case's evidence cell under the declared
tests root are rewritten as the test files' declarations make them, every
other part kept. SR-157 is a reporting obligation, and it keeps the
equality check that holds the column current. LLR-406 now states that with
no test-case registry or no tests root the command writes nothing and
reports which input is missing. That was the one behaviour missing from the
code: the command said "every evidence cell is current". TC-483 verifies
the empty-cell key drop (and a case gaining a key), the re-read refusal
writing nothing, the command's report of the changed cases, and the two
missing inputs.

**6. TC-481 and TC-484.** TC-481 covers the symbol and component cells
beside the file cell, the need tier, the registry file named in every
refusal, and the retired cells classed traced, the row's accepted text the
same with and without them. TC-484 covers the absent registry (reported,
nothing written, the command exiting 0) and the re-read refusal (a quoted
key the line remover cannot see; refused naming the registry, its bytes
unchanged).

**7. Coverage.** Every gap the verdict names on TC-239 and TC-480 to TC-484
is closed by a test carrying that case's tag, and the evidence is
regenerated from the tags (`trace.py --root . --regen-evidence`: "evidence
regenerated for TC-480, TC-481, TC-482, TC-483, TC-484, TC-485"). No list
was cut where a test could verify it, save the consumer lists in item 3
and item 4, each cut to one home per reader. Nothing is deferred.

**8. No code names in row text.** No cell this branch wrote names a code
file, module, function, symbol, flag, step or test name; the re-landed
cells drop the names their accepted and `8e08b3029` text carried. Registry
column names and stage tokens stay. A scan of every changed cell for file
suffixes, flags, snake-case names and the back-link token found none.
(The `evidence` cells are generated pointers to test nodes by definition.)

**Red first.** The one new behaviour,
`test_with_no_registry_or_no_tests_root_the_regeneration_says_so`
(`tests/test_llr_trace_cells.py`, TC-483), failed before the code:
`AssertionError: trace: every evidence cell is current`
(`tests/test_llr_trace_cells.py:241`), `1 failed, 7 deselected in 0.70s`.
After `arch_tags.evidence_input_missing` and the command's report it
passes. Every other new or extended test drives behaviour the code already
had, so it passed on its first run; each was then run against a mutation of
the code it drives, shown failing, the file's original bytes restored, and
run green (the coordinator's ruling, 2026-11-22). No mutation was
committed:

| Test (case) | Mutation | Fails at | Red, then restored |
|---|---|---|---|
| `test_an_interface_with_no_contract_body_reaches_nothing` (TC-239) | `assumption_rules.py`: `if homes is None:` became `if True:`, so an interface with no body reaches through its owner's placement | `tests/test_assumption_gate.py:596`, `_judged(... "no boundary interface reaches it" ...)` | 1 failed in 7.80s; 1 passed in 7.59s |
| `test_with_no_source_scanned_an_interface_reaches_through_its_owner` (TC-239) | `assumption_rules.py`: the owner-component reach's placement replaced by `{}` | `tests/test_assumption_gate.py:610`, `_judged(... ("IF-020",) ...)` | 1 failed in 7.69s; 1 passed in 8.20s |
| `test_a_design_row_is_placed_through_the_interfaces_its_cases_name` (TC-480) | `trace_text.py`: `_PLACEMENT_SHOWN = 10` became `12` | `tests/test_llr_trace_cells.py:97`, `assert "LLR-019, +2 more)" in line ...` | 1 failed in 0.64s; 1 passed in 0.29s |
| `test_the_views_show_where_each_design_row_sits` (TC-480) | `gen_components.py`: the census's `design_rows_unplaced` written as 0 | `tests/test_llr_trace_cells.py:135`, `assert doc["derived"]["design_rows_unplaced"] == 1` | 1 failed in 0.42s; 1 passed in 0.30s |
| same (TC-480) | `traj_parse.py`: the state view's `or "unplaced"` became `or ""` | `tests/test_llr_trace_cells.py:140`, `assert details["LLR-003"]["meta"] == "Placed: unplaced"` | 1 failed in 0.45s; 1 passed in 0.33s |
| `test_an_unplaced_design_row_changes_no_exit_code` (TC-480) | `trace.py`: exit 1 after the count line when a row is unplaced | `tests/test_trace.py:792`, `assert proc.returncode == 0, ...` | 1 failed in 10.00s; 1 passed in 9.04s |
| `test_a_design_row_is_discharged_by_a_case_of_any_kind` (TC-485) | `coherence.py`: only an automated case's `Verifies` discharges | `tests/test_llr_trace_cells.py:161`, `assert [f for f in findings if f.startswith("LLR ")] == [` | 1 failed in 0.44s; 1 passed in 0.31s |
| same (TC-485) | `coherence.py`: the Drafted exemption removed | `tests/test_llr_trace_cells.py:161`, the same assertion | 1 failed in 0.42s; 1 passed in 0.30s |
| `test_every_refusal_names_the_file_the_row_and_the_key` (TC-481) | `spine_carrier.py`: the undeclared-key finding given `""` for the file | `tests/test_llr_trace_cells.py:222`, `assert str(reg) in why and ...` | 1 failed in 0.44s; 1 passed in 0.31s |
| `test_the_loader_refuses_a_key_a_requirement_tier_does_not_declare` (TC-481; review round 1) | `spine_carrier.py`: the undeclared-key finding given `""` for the file on every tier | `tests/test_llr_trace_cells.py:177`, `` assert str(reg) in why and "LLR-001" in why and "`module`" in why `` | 1 failed in 0.50s; 1 passed in 0.36s |
| same (TC-481; review round 1) | `spine_carrier.py`: the file left out on the requirement and test-case tiers only | `tests/test_llr_trace_cells.py:188`, `` assert str(sr) in why and "SR-000" in why and "`owner`" in why `` | 1 failed in 0.43s; 1 passed in 0.35s |
| same (TC-481; review round 1) | `spine_carrier.py`: the file left out on the test-case tier only | `tests/test_llr_trace_cells.py:195`, `` assert str(tc) in why and "TC-001" in why and "`module`" in why `` | 1 failed in 0.45s; 1 passed in 0.44s |
| `test_the_retired_design_cells_stay_classed_traced` (TC-481) | `acceptance_record.py`: `CodeSymbol` dropped from the design tier's traced cells | `tests/test_llr_trace_cells.py:239`, `assert acceptance_record.spine_cell_class(LLR_REL, column) == "traced"` | 1 failed in 0.44s; 1 passed in 0.28s |
| `test_the_index_reads_past_what_it_cannot_read` (TC-482) | `gen_arch_map.py`: the source scan decodes as Latin-1 | `tests/test_llr_trace_cells.py:316`, `assert arch_inputs.implements_index(tmp_path) == {` | 1 failed in 0.48s; 1 passed in 0.40s |
| same (TC-482) | `arch_inputs.py`: an absent source root returns `{}` before the headers are read | `tests/test_llr_trace_cells.py:322`, `assert arch_inputs.implements_index(tmp_path) == {"LLR-003": ["docs/reg.toml"]}` | 1 failed in 0.51s; 1 passed in 0.38s |
| `test_the_build_brief_marks_a_design_row_no_declaration_names` (TC-482) | `intake.py`: the code map's undeclared marking became `""` | `tests/test_llr_trace_cells.py:338`, `assert [ln for ln in lines if ln.startswith("- LLR-002 [no Implements: tag]")], text` | 1 failed in 0.44s; 1 passed in 0.38s |
| `test_an_emptied_cell_loses_its_key_and_the_command_names_the_cases` (TC-483) | `arch_tags.py`: an emptied cell written as an empty string | `tests/test_llr_trace_cells.py:401`, `assert _main(... "--regen-evidence") == 0` | 1 failed in 0.48s; 1 passed in 0.30s |
| same (TC-483) | `arch_tags.py`: the report counts the cases without naming them | `tests/test_llr_trace_cells.py:402`, `assert capsys.readouterr().out.splitlines() == [` | 1 failed in 0.40s; 1 passed in 0.29s |
| `test_a_rewrite_that_does_not_re_read_is_refused_and_writes_nothing` (TC-483) | `arch_tags.py`: the re-read check replaced by `if False:` | `tests/test_llr_trace_cells.py:428`, `assert "REFUSED" in str(code) and ...` | 1 failed in 0.41s; 1 passed in 0.29s |
| `test_an_absent_registry_is_reported_and_nothing_is_written` (TC-484) | `migrate_carrier.py`: an absent registry returns no report line | `tests/test_llr_trace_cells.py:570`, `assert report == [...]` | 1 failed in 0.39s; 1 passed in 0.27s |
| `test_a_migration_that_does_not_re_read_is_refused_and_writes_nothing` (TC-484) | `migrate_carrier.py`: the re-read check replaced by `if False:` | `tests/test_llr_trace_cells.py:583`, `with pytest.raises(SystemExit) as exc:` | 1 failed in 0.39s; 1 passed in 0.28s |

The size ratchet asked for a decomposition rather than a bump when the
command's report first landed in `trace.py`: the report line moved into
`arch_tags.evidence_regen_report` beside the writer, `check_trajectory`
re-exports it in place of `write_evidence`, and `trace.py` ends 4 lines
under its baseline, re-stamped down (3788 to 3784) in the same commit.

**Tests.**

- The 85 test modules that import a changed module or are spine-linked to
  one (`trace.py --tests-for`), with the modules holding every touched
  case's tests and `test_import_layers`, `test_module_size_ratchet` and
  `test_dogfood_sync`, at the build commit's tree:
  `46 failed, 3003 passed, 2 skipped, 18 warnings in 839.92s (0:13:59)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> <the 85 modules>" rev="cbe6aab2f" -->
  One failure was this branch's: the composer test
  (`test_trajectory_arch.py::test_the_composer_exposes_every_public_name_of_the_modules_it_composes`),
  fixed in `08639915b`; that module with the ratchet, layer and trace-cells
  modules then read `198 passed in 95.18s (0:01:35)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> tests/test_trajectory_arch.py tests/test_module_size_ratchet.py tests/test_import_layers.py tests/test_llr_trace_cells.py" rev="08639915b (its tree before the commit)" -->
- The other 45 fail identically on the base. The five modules holding them
  (`test_intake_held_act` 22, `test_intake_settled` 19,
  `test_snapshot_readers` 1, `test_assumption_gate`'s release half 2,
  `test_done_when_blessing` 1) were run on this branch and again with its
  changes stashed at `9548c30c1`: `45 failed, 192 passed in 165.00s` and
  `45 failed, 190 passed in 234.14s`, the same node ids failing (the two
  extra passes are TC-239's new tests). Forty-two of them stop at "the
  held-act mint was refused: docs/archive/last_accepted/... cannot be read
  at <sha>". They are not this row's to fix.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> tests/test_intake_held_act.py tests/test_intake_settled.py tests/test_snapshot_readers.py tests/test_assumption_gate.py tests/test_done_when_blessing.py" rev="the build tree, and 9548c30c1 with the changes stashed" -->
- `trace.py --root . --strict`, exit 0: `orphans=0 integrity=0`.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="08639915b (with the close-out's tree, before its commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1053 work item(s), 922 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="08639915b (with the close-out's tree, before its commit)" -->
- `check.py --run-step` for `assumption-gate`, `crossing-allocation` and
  `interface-allocation`: "0 finding(s), the assumption gate is on" each.
- `scripts/check_resync.py`: "OK, 9 shipped path(s) changed; entry anchored
  at 3c33b378305cad4121c89c4c0c21b721eae1c288"; `check_docs.py --root .
  --stale`: "0 broken".
- The commit checks, `run_menu.py smoke`, exit 0 (both strict lints, the
  docs check and the RESYNC check above, then the smoke tier):
  `3735 passed, 3 skipped, 18 warnings in 145.71s (0:02:25)`. Its budget
  line reads CPU 744.2 s against 540, a WARN only, not charged to the lane;
  wall 146.6 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="08639915b (with the close-out's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched), base `3c33b3783` to `cbe6aab2f`:
`docs/requirements/system-requirements.toml` 318,619 -> 323,434 (+4,815);
`docs/requirements/low-level-requirements.toml` 560,663 -> 562,370 (+1,707);
`docs/test/test-cases.toml` 693,595 -> 698,439 (+4,844);
`project-trajectory/RESYNC_PACK.md` 752,486 -> 754,083 (+1,597).

**Acts owed for the fourth sitting.**

- *Amendments to `Accepted` rows (text only, status unchanged):*
  SR-212 `acceptance_criteria`; LLR-244 `detail`; TC-239 `method` and
  `expected`; SR-221 `title`, `requirement`, `acceptance_criteria`,
  `rationale` and `coincident`; LLR-263 `title`, `detail` and `rationale`;
  TC-258 `method` and `expected`.
- *Routed traced changes to `Accepted` rows:* none. No `Accepted` row's
  `sr_refs`, `verifies`, `sn_refs` or `boundary_refs` moved, and the
  regenerated evidence changed only `Drafted` cases. (SR-221 is now also
  verified by the `Drafted` TC-482; the change is on TC-482.)
- *First acceptance, `Drafted`, new or rewritten:* SR-248 (rewritten);
  SR-249, SR-250 and SR-251 (new); LLR-403, LLR-405 and LLR-406
  (rewritten); LLR-408 (new); TC-480, TC-481, TC-482, TC-483 and TC-484
  (rewritten); TC-485 (new).

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, to answer
the third automated adjudication sitting's verdict (WI-1055, Gemini Neon,
the specref). The sitting blessed 15 amendments and accepted 5 rows, but
ruled five of F-3's (WI-1023) amendments MEANING without the bless mark and
returned nine of F-3's new rows. Its act was refused (SR-207) while the five
unblessed rows drifted in all three registries it copies.

**The operator's ruling (2026-11-22, given in the coordinator's session):**
as at WI-1049, revert the five unblessed amendments to their accepted text
and take the act now; this row re-lands them, answered, for a fourth
sitting. So, in the commit that files this row, the accepted cells the
sitting read went back to the recorded text: LLR-244's `detail`, LLR-263's
`detail` and `rationale`, SR-212's `acceptance_criteria`, TC-239's `method`
and TC-258's `expected` and `method`. The amended text this row re-lands is
at `8e08b3029` (`git show 8e08b3029:<registry>`). Until it merges, those
rows describe the code as it was before F-3 (and, for LLR-244, before F-2).

**Why one row.** The repairs could land apart, but they stay together and
land as one branch before the fourth sitting (decided at the scope
critique). They answer one verdict, and the sitting judges each chain
whole, so a partial landing would return to it as drift beside unanswered
findings. The chains also cross. SR-221's listing reads the back-link
index LLR-405 states, and TC-482 verifies both LLR-405 and LLR-263.
LLR-244's reach goes through the same index and through LLR-403's
placement where no source is scanned. Splitting the rows would put one
fact's wording on two branches.

**Planning.** `planmode = "single"`: the plan settles two choices before
any edit. First, how SR-248 splits, with each successor's id from the
launch range. Second, which SR states generation for LLR-406: an existing
row, or a new one from the range. It also names each test-case repair's
tests.

The findings, quoted from the verdict:

- **SR-212** (MEANING, not blessed): "the amended acceptance states only
  back-link file reachability and omits the no-source-scanned
  owner-component placement fallback (and no-contract-body rule) that its
  child LLR-244 relies on, leaving parent and child contradicting each
  other when no source is scanned."
- **LLR-244** (MEANING, not blessed): "(1) its no-source-scanned fallback
  exceeds and contradicts unamended parent SR-212's back-link-only
  acceptance condition, and (2) neither the no-contract-body-reaches-none
  clause nor the no-source-scanned fallback is verified by TC-239."
- **TC-239** (MEANING, not blessed): "it leaves unverified both LLR-244's
  no-contract-body-reaches-none clause and its no-source-scanned
  owner-component placement fallback."
- **LLR-263** (MEANING, not blessed): "parent SR-221 was not amended and
  still requires listing 'for a module a design row names ... derived from
  the registries', creating an upward contradiction that LLR-263's own
  Rationale still echoes in its opening sentence."
- **TC-258** (MEANING, not blessed): "TC-258 claims to verify unamended
  SR-221 alongside LLR-263 while SR-221 still requires registry-only
  derivation from modules named by design rows."
- **SR-248** (RETURN): "Requirement contains two `shall` keywords / two
  separate obligations (violating §2(a) and LLR-134's one-obligation rule
  ...), omits back-link file reading from Requirement while putting it in
  AcceptanceCriteria for LLR-405, and uses an unbounded absolute ('never
  fails a check') in AcceptanceCriteria."
- **LLR-403** (RETURN): "bundles two decisions (placement and discharge)
  though its Title and Rationale cover only placement, leaves its
  Drafted-LLR orphan rule unreconciled with LLR-201, and leaves four of its
  five named placement consumers unverified in TC-480."
- **LLR-405** (RETURN): "its Requirement [SR-248's] does not call for a
  back-link file index; Detail leaves what distinguishes a literal
  back-link declaration from prose (or citation of the shared grammar) and
  absent-root/unreadable-file behavior unspecified; and its build-brief
  code-map marking for undeclared rows is unverified in TC-482."
- **LLR-406** (RETURN): "a registry-rewriting generator is scope outside
  violation-reporting SR-157 and belongs under an appropriate
  generation/regeneration SR ... and omits behavior when the tests root or
  test-case registry is absent."
- **TC-480** (RETURN): it "does not verify the additional placement
  consumers LLR-403 claims (state view, build brief context block,
  knowledge-pack advisory, and no-source-scanned interface-form gate)."
- **TC-481** (RETURN): it "tests only a file cell on a design row (not
  symbol or component), omits the need tier and checking that refusals name
  the file alongside row and key, and never verifies that retired
  design-row cells stay classed traced with no accepted-text drift on
  removal."
- **TC-482** (RETURN): it "omits verifying absent-root/unreadable-file
  index behavior and LLR-405's build-brief empty-declaration marking."
- **TC-483** (RETURN): it "omits verifying that a cell becoming empty drops
  its key, omits verifying the re-read verification refusal writing
  nothing, and omits driving the command interface and checking that it
  reports the changed cases."
- **TC-484** (RETURN): "neither the absent-registry refusal (reported with
  nothing written) nor the re-read verification refusal ... is exercised."

SR-221's stale wording was first noted at F-3's review and put on WI-1018's
list; the verdict makes it a blocker for LLR-263, so it moves here and
WI-1018 drops it.

## Done-when

- [x] SR-212's acceptance criteria state the reach LLR-244 states (through
      the one file stating an interface's contract body; an interface with
      no body reaches none; where no source is scanned, through the design
      rows placed in the interface's owner component), and LLR-244's
      `detail` is re-landed from `8e08b3029` consistent with it. TC-239's
      method is re-landed and it verifies both clauses the verdict names,
      with a test for each. On the three `Accepted` rows only the text
      changes, never the status; the tests are this row's to write.
- [x] SR-221 (`Accepted`) is amended so the listing is for a file, read by
      joining the back-link index with the test-case registry, not "for a
      module a design row names ... derived from the registries"; LLR-263's
      `detail` and `rationale` (its opening sentence corrected) and TC-258's
      `expected` and `method` are re-landed under it. Text only. WI-1018
      drops SR-221 from its set.
- [x] SR-248 becomes rows of one obligation each (discharge; placement; and
      the back-link reading LLR-405 serves, where no SR states it), with no
      unbounded absolute in an acceptance criterion; LLR-403 states one
      decision, its discharge clause reconciled with LLR-201 or moved; each
      placement consumer LLR-403 names is verified, or the list is cut to
      what is.
- [x] LLR-405's `detail` cites the shared declaration grammar for what makes
      a back-link and states the absent-root and unreadable-file behaviour;
      TC-482 verifies those and the build brief's marking of an undeclared
      row.
- [x] LLR-406 sits under an SR that states generation, not SR-157, and
      states the behaviour with no tests root or no test-case registry;
      TC-483 verifies the empty-cell key drop, the re-read refusal writing
      nothing, and the command's report of the changed cases.
- [x] TC-481 covers the symbol and component cells, the need tier, the file
      named in the refusal, and the retired cells' traced classing; TC-484
      covers the absent-registry report and the re-read refusal.
- [x] Every coverage gap the verdict names on TC-239 and TC-480 to TC-484
      is closed on this branch by an automated test carrying that case's
      tag, and the evidence is regenerated from the tags. A test for new
      or newly stated behaviour is shown failing before the code that
      passes it. A list cut instead (LLR-403's consumers) cuts the row's
      text to match. Nothing is deferred to another row.
- [x] No row text this branch writes names a code file, function or symbol.
      The Deliverable lists every act owed for adjudication.
