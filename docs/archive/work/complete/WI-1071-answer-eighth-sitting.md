+++
id = "WI-1071"
title = "WI-1068's verdict answered: four rows restore dropped clauses, three test cases fixed, LLR-423's overlap resolved"
workstream = "process"
specref = ""
sr_refs = ["SR-022", "SR-046", "SR-070", "SR-178", "SR-224", "SR-229"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1071`, cut from `refactor_again`
at `ec188f984`, with the commit hooks on, from the plan
[`docs/plans/WI-1071/plan.md`](../../../plans/WI-1071/plan.md) (revision 1,
approved by the coordinator on 2026-11-24, D1 to D13 confirmed). No id
minted, no status moved, no act taken and no kit file changed (tests and
registries only, so no RESYNC entry). No decisions record: every choice is
stated by a spine row or by the plan the coordinator approved. The specref
(the eighth sitting's verdict) is cleared at close.

- `1e015b89c`: the plan (Phase 1).
- `86303ad32`: the tests first, each shown red against a one-line mutant;
  the plan's approval line.
- `dcb748c9a`: the row text, the regenerated evidence and the regenerated
  views.
- The close-out commit: TC-533 cites IF-277 (the deviation below), this
  Deliverable, the move to `docs/archive/work/complete/`, the log
  fragment, the views.

**1. The four rows' dropped clauses (Done-when 1).** Each row's live
`detail` was diffed against its acceptance-record copy and every dropped
clause checked in the code. Text only; each row stays `Accepted` and owed.
Its `constrains` link is unchanged (WI-1070 makes the brief show it).

| Row | Dropped clause | Settled | Test |
|---|---|---|---|
| LLR-047 | no interpolation in the run section | restated ("with no interpolation, so a percent sign in a value is literal") | `test_the_run_section_reads_values_literally_and_keeps_a_names_case` (new) |
| LLR-047 | a capability name keeps its case | restated | the same test (`Serve` lists and launches; `serve` exits 2) |
| LLR-047 | an orphan description row and an empty-value command are dropped | restated | `test_an_orphan_description_and_an_empty_command_are_dropped` (new) |
| LLR-039 | front matter as JSON-quoted YAML scalars | restated ("as JSON-quoted strings, which YAML reads as scalars") | `test_front_matter_scalars_are_json_strings` (new) |
| LLR-039 | the freshness check fails after a document edit and on a missing bundle file | restated, the edit bounded to a guide document's first heading or paragraph (an edit elsewhere moves no bundle byte) | `test_check_trips_on_a_guide_edit_and_a_missing_bundle_file` (new) |
| LLR-039 | the legacy opt-out file | restated as the precedence the code holds: with no declared choice a legacy one-word file reading off silences the step, and a declared choice overrides it (no "migration window" wording, D4) | `test_the_legacy_opt_out_file_silences_only_with_no_declared_choice` (new) |
| LLR-039 | small loaders duplicated, no new sibling import | **reported, no longer enforced**: the generator imports the spine carrier and the shared package; the text says nothing of it | none |
| LLR-199 | unplaced design rows in the counted unplaced table | **home: LLR-403** (accepted), which states that the component view lists each unplaced row in its unplaced table, counted in its census; LLR-199's text now names LLR-403 for both placement and the unplaced rows ("as LLR-403 states") | TC-480's `tests/test_llr_trace_cells.py::test_the_views_show_where_each_design_row_sits` |
| LLR-199 | the generated-but-live staleness header | restated (generated, not to be edited by hand, the registries to cite instead, the regeneration command) | `test_the_view_opens_with_the_generated_file_header` (new) |
| LLR-199 | the trunk regeneration wiring | restated under SR-070 alone ("The kit's stack profile declares the file a generated artifact, and the trunk's regeneration step re-derives it"); LLR-142 lists five families and not this view, so it is no home (D2) | `test_the_view_is_declared_generated_and_the_trunk_regeneration_re_derives_it` (new) |
| LLR-281 | the `SHORT` output marker | restated (an output marker is observable behaviour) | `test_check_refuses_a_description_under_the_floor` (extended) |
| LLR-281 | the floor is checked first | restated ("applies the floor before it compares the index ... exits 1 without comparing the index") | `test_the_floor_is_checked_before_the_index_is_compared` (new) |
| LLR-281 | (found by the diff) the line names the length | kept; it was untested | `test_check_refuses_a_description_under_the_floor` (extended: ` 7 characters`) |

LLR-199's two other differences from its record ("registries cannot
distinguish missing decomposition ..." and "NOT DISCHARGED ...") state no
behaviour of their own and were not restored (plan §1). LLR-199's relation
to LLR-403: LLR-403 is the one home of design-row placement, through the
`constrains` cell and through verifying test cases, and of the view's
listing of placed and unplaced design rows; LLR-199 consumes that
placement and points at it rather than restating it.

The verifying test cases now state what their rows state (D12), each with
its inherited code names scrubbed: TC-047 (`method`, `expected`: literal
values, kept case, dropped rows; `--list`, `run_menu.py`, `[run]`,
`RUN_CMD`, `PATH`, `python.exe` gone), TC-042 (`method`, `expected`: JSON
round trip, guide edit, missing file, legacy file; `--check` and
"gen-okf" gone), TC-195 (`method`: THE HEADER and THE TRUNK WIRING
sentences), TC-291 (`method`, `expected`: the SHORT line with its length,
the floor first; `--check` and `short_descriptions` gone). TC-342, TC-460
and TC-465 drive clauses the rows kept and are unchanged.

**2. TC-398 (Done-when 2).** The assertion already existed, so nothing was
red first. `tests/test_adjudicate_act.py::test_a_held_CLARITY_act_whose_text_changed_after_the_verdict_is_refused`
and `::test_a_held_CLARITY_act_whose_link_moved_after_the_verdict_is_refused`
each assert

```python
    for word in ("SR-001", bound, committed):
        assert word in why, (word, why)
```

and `::test_a_binding_over_accepted_cells_alone_refuses_a_row_carrying_a_link`
asserts `("SR-001", old, _sr_digest(repo))`. TC-398's `method` now reads
each refusal "for the row and, where the identities are unequal, for the
digest the binding records and the committed row's digest"; its `expected`
says the moved cell, the moved link and the accepted-cells-only binding
"are unequal identities, and each refuses it naming the row, the digest
its binding records and the committed row's digest". On the coordinator's
routing from WI-1070, its `expected` also says "one judged-text line per
row shown for judgement" (was "per shown row"), since WI-1070's context
rows carry no identity line. Evidence unchanged.

**3. TC-530 (Done-when 3; still `Drafted`).** Its `method` and `expected`
now run two ranges over one project: a second commit adds a constrains
cell, and nothing else, to the requirement and the first design row; a
third adds a dimensions and an out-of-domain cell, and nothing else, to
the second design row. In `tests/test_constrains.py` the combined test is
replaced by `test_a_constrains_only_change_routes_with_no_accepted_cell_moved`
(the walk records `Constrains` in each row's traced half and no accepted
cell; the mint routes both rows by `Constrains` alone and drafts one
adjudication row naming `LLR-001` and `SR-001`) and
`test_a_companion_cell_change_amends_accepted_text_alone` (the walk records
`Dimensions` and `OutOfDomain` in the accepted half and no traced cell; the
mint drafts the row naming `LLR-002` with nothing routed). LLR-420 is not
amended.

**4. TC-571 (Done-when 4; still `Drafted`).** Its `method` adds "Then,
from a fresh copy, move the third design row's detail, add an interface to
its constrains cell and move its phase cell, so a rendered row also moves
a trace cell no adjudicator judges; read the model and render both
surfaces", which is what `test_both_surfaces_label_the_three_groups_alike`
and `test_a_rows_other_trace_cells_come_last` build. Its `expected` now
says where the third row also moves its phase cell, the model lists that
cell after its detail and constrains cell, and both surfaces show it under
the label owing no act, after the other two labels. The three-label test
gains the assertion that the phase cell, before and after, sits under that
label on each surface (D10). LLR-484 is not amended.

**5. The session-variable home (Done-when 5).** LLR-423 (verified by
TC-533) is the one home; its text is unchanged and it and TC-533 stay
`Drafted`.
- LLR-300 (`detail`, text only, still `Accepted`): the claim refusal no
  longer "identifies the claimant by the session id the agent CLI exports
  to its tool processes (CLAUDE_CODE_SESSION_ID)"; it "refuses with no
  lease held or a claimant that is not the holder". Every lease-admission
  obligation stays. Rule 1 scrubbed its inherited code names: the
  function names (`guard_config`, `read_occupancy`, `take`, `release`,
  `clear`, `hand_back`, `session_end`, `on_session_start`,
  `latch_reading`, `window_refusal`, `claim_refusal`, `window_check`,
  `classify_compaction`), the variable, the agent tool's `Agent` and
  `SendMessage` tool names (now its subagent-launch and subagent-message
  calls) and the `SessionStart` and `PreCompact` events (D6).
- TC-316 (`method`, text only, still `Accepted`): "Assert that a claim
  identifies its caller by the session variable the agent CLI exports, and
  refuses, ..." now reads "Assert that a claim refuses, ...". Its
  `verifies` drops IF-277 (D5); IF-277 still reaches TC-533 and TC-534
  through LLR-423 and LLR-424 (`kitlib.spine.interface_reach` over the
  live registries: `IF-277 -> (['LLR-423', 'LLR-424'], ['TC-533',
  'TC-534'])`; it is not in `trace.py --strict`'s unreached list).
- **Deviation from the plan: TC-533's `verifies` gains IF-277.** With
  TC-316's link dropped, `check_trajectory.py --root . --strict` failed:
  "ERROR - 1 IF seam(s) have no citing TC and are not on the migration
  allowlist (docs/if-tc-coverage-allow) ... : IF-277". That rule (OI-43,
  WI-488) counts only a test case's `verifies`, not reach through a
  constraining row, and TC-316 was IF-277's one citing test case. TC-533
  is the test case that checks the variable IF-277 declares, so it cites
  it: `verifies = ["SR-229", "LLR-423", "IF-277"]`. It is `Drafted`, so
  this adds nothing to the act it already owes. Not chosen: an allowlist
  entry (a list edit that makes a check pass), TC-534 (an `Accepted` row,
  a second routed change). After it the check is clean.
- The tests that drove the clause, both now named by TC-533's evidence:
  `tests/test_coordinator_guard.py::test_the_guard_reads_its_caller_from_the_agent_tools_session_variable`
  (already TC-533's) and `::test_a_claim_names_its_caller_by_claude_code_session_id`
  (re-tagged from TC-316).
- LLR-300's other clauses, checked against every test case verifying it
  (TC-315, TC-316, TC-317, TC-339, TC-345, TC-370; plan §5), are each
  driven. Three gaps older than this row were closed by adding cases, not
  by cutting clauses (D7): the threshold's bounds
  (`test_a_malformed_threshold_leaves_the_guard_off`, TC-317, now
  parametrized over a wrong type, -5 and 150); four unreadable forms
  (an unclosed double quote, POSIX dollar quote, backtick substitution and
  PowerShell here-string, added to TC-339's `UNREADABLE` table); and the
  window check's exit (`test_the_window_check_subcommand_exits_nonzero_inside`,
  now tagged TC-339 as well as TC-318 and TC-340). TC-317's and TC-339's
  text did not change. LLR-300 stays one row (D8): a sitting may still
  judge it as several obligations (the blackout hook denials are arguably
  SR-237's own), and a split would be its own row.

**6. The three row rules (Done-when 6).** Every row touched: LLR-039,
LLR-047, LLR-199, LLR-281, LLR-300, TC-042, TC-047, TC-195, TC-291,
TC-316, TC-398, TC-530, TC-571, and TC-533 (evidence only). No text
written here names a code file, module, function, symbol, CLI flag or
test name, and the inherited ones in every cell touched are gone (a scan
of the added lines for underscores, flags, `.py` names and backticks
finds none); `SHORT` is a printed marker, and LLR-403 a row id. Each
clause each row states is driven by a test its test cases name (items 1
to 5). Each amended LLR stays inside its parents (LLR-047 in SR-046,
which gives it the declaration grammar by name; LLR-039 and LLR-199 in
SR-070's generated-view contract; LLR-281 in SR-224; LLR-300 in SR-229 and
SR-237, from which it only lost a clause), and each test case states
nothing beyond the rows it verifies. The hook warned that five rows'
`detail` moved while `Hat-Refs` stayed put; they are left on purpose, since
each row's perspective did not change.

**Red first.** The restored clauses were already enforced, so each new
assertion passed on the code as it stood. Each was shown red against a
one-line mutant of the code it pins, applied by a scratch script outside
the repository that restored the file byte-for-byte before exiting; none
was committed (D1).

| Mutant (one line, reverted) | Test | First red line |
|---|---|---|
| `kitlib/config.py`: the stack-profile parse interpolates | `test_the_run_section_reads_values_literally_and_keeps_a_names_case` | `tests/test_run_menu.py:170: AssertionError: Traceback (most recent call last):` (the list form exits nonzero on `%(home)s`) |
| `run_menu.py`: the loader folds keys | the same | `assert 'serve\t100% of %(home)s\n' == 'Serve\t100% of %(home)s\n'` |
| `run_menu.py`: an empty command is kept | `test_an_orphan_description_and_an_empty_command_are_dropped` | `assert 'serve\t\nblank\t\n' == 'serve\t\n'` |
| `run_menu.py`: an orphan description becomes a command | the same | `assert 'serve\t\ngho... no command\n' == 'serve\t\n'` |
| `gen_okf.py`: the front matter quotes by hand | `test_front_matter_scalars_are_json_strings` | `json.decoder.JSONDecodeError: Extra data: line 1 column 8 (char 7)` |
| `gen_okf.py`: a guide's summary is not derived | `test_check_trips_on_a_guide_edit_and_a_missing_bundle_file` | `tests/test_gen_okf.py:153: AssertionError: gen_okf: OKF bundle up to date (17 file(s)).` |
| `gen_okf.py`: the comparison skips absent files | the same | `tests/test_gen_okf.py:159: AssertionError: gen_okf: OKF bundle up to date (17 file(s)).` |
| `gen_okf.py`: the legacy file is not read | `test_the_legacy_opt_out_file_silences_only_with_no_declared_choice` | `tests/test_gen_okf.py:177: AssertionError` |
| `gen_components.py`: the header's first line emptied | `test_the_view_opens_with_the_generated_file_header` | `AssertionError: GENERATED by scripts/gen_components.py` |
| `trunk_step.py`: the component-view step never applies | `test_the_view_is_declared_generated_and_the_trunk_regeneration_re_derives_it` | `tests/test_gen_components.py:406: AssertionError: assert 1 == 0` |
| `gen_skills_index.py`: the SHORT marker dropped | `test_check_refuses_a_description_under_the_floor` | `ValueError: not enough values to unpack (expected 1, got 0)` |
| `gen_skills_index.py`: the floor's call before the comparison removed | `test_the_floor_is_checked_before_the_index_is_compared` | `assert 'SHORT - terse:' in 'gen_skills_index: STALE - ...INDEX.csv does not match the SKILL.md files; ...'` |
| `record_rows.py`: `Constrains` out of the design rows' routed cells | `test_a_constrains_only_change_routes_with_no_accepted_cell_moved` | `assert {'SR-001': {'Constrains'}} == {'SR-001': {'...'Constrains'}}` |
| `acceptance_record.py`: the companion cells classed traced (dropping them from the accepted table changes nothing, since an unclassified cell reads accepted) | `test_a_companion_cell_change_amends_accepted_text_alone` | `assert set() == {'Dimensions', 'OutOfDomain'}` |
| `trace.py`: the no-act group's cells dropped, its label kept | `test_both_surfaces_label_the_three_groups_alike` | `tests/test_routed_link_owed.py:167: AssertionError` (the new assertion: no phase cell under the label) |
| `coordinator_guard.py`: the threshold's range unbounded | `test_a_malformed_threshold_leaves_the_guard_off` | `[-5]` and `[150]`: `assert GuardConfig(t...window=200000) == GuardConfig(t...window=200000)`; `2 failed, 1 passed` (the wrong type still off) |
| `kitlib/shell_line.py`: an unclosed double quote read as closed | `test_an_unreadable_command_line_is_denied_inside_the_window` | `AssertionError: echo "unbalanced; claude -p x` |

Not red, being no new assertion: TC-398's tests (item 2), the re-tag to
TC-533 and the window-check test's TC-339 tag.

<!-- fig: cmd="python mutant.py (scratch, outside the repository): pytest -q --tb=line on each named test under each one-line mutant" rev="maint/wi-1071 tests as committed in 86303ad32, code at ec188f984 plus each mutant" -->

**Tests run.**

- Every module the touched test cases' tests sit in, with the four ratchet
  modules the brief names (no kit module changed, so no importer runs):
  `tests/test_run_menu.py`, `tests/test_bootstrap.py`,
  `tests/test_gen_okf.py`, `tests/test_gen_components.py`,
  `tests/test_skills_index.py`, `tests/test_coordinator_guard.py`,
  `tests/test_coordinator_guard_e2e.py`, `tests/test_session_keep.py`,
  `tests/test_blackout_window.py`, `tests/test_adjudicate_brief.py`,
  `tests/test_adjudicate_act.py`, `tests/test_coordinator_act.py`,
  `tests/test_held_status.py`, `tests/test_held_status_git.py`,
  `tests/test_amendment_brief_links.py`, `tests/test_constrains.py`,
  `tests/test_routed_link_owed.py`, `tests/test_import_layers.py`,
  `tests/test_module_size_ratchet.py`, `tests/test_complexity_ratchet.py`,
  `tests/test_dogfood_sync.py`: `942 passed, 3 skipped in 745.71s
  (0:12:25)`.
- `trace.py --root . --strict`: exit 1 on one finding outside this row
  (below, "Left for the coordinator"), identical on the base with the
  build's changes stashed; otherwise "Traceability: SN=31 SR=141 LLR=369
  TC=445 orphans=0 integrity=0 ... interface-findings=0 ... form-findings=1";
  "interface coverage: 239 interface(s): 27 through a constraining design
  row, 0 through a constraining requirement, 118 through a naming test
  case, 0 by observation alone, 94 unreached", IF-277 not among the
  unreached.

<!-- fig: cmd="python -m pytest -q -n auto <the twenty-one modules above>; python project-trajectory/scripts/trace.py --root . --strict" rev="maint/wi-1071 at dcb748c9a" -->

After the close-out (the spec moved, TC-533 citing IF-277, the views
regenerated):
- `check_trajectory.py --root . --strict`: exit 0, "check_trajectory:
  clean (1068 work item(s), 941 done (88%), 37 cancelled, graph acyclic)."
- `check_docs.py --root .` after the move: "check_docs: OK - 3707 doc(s),
  3836 intra-repo link(s), 0 broken."
- `run_menu.py smoke`, once: exit 1 at its first step, `trace.py
  --strict`, on the LLR-484 finding outside this row, so the chain (`&&`)
  stopped before the tier. Its remaining steps were then run in the same
  order on the same tree: `check_docs.py --root . --stale` "check_docs:
  OK - 3708 doc(s), 3836 intra-repo link(s), 0 broken."; `check_resync.py`
  "check_resync: OK, no shipped path changed (base ec188f984...)";
  `check_smoke_budget.py --mode warn` exit 0, `3933 passed, 3 skipped, 18
  warnings in 331.13s (0:05:31)`, "smoke budget: CPU 848.4 s vs 540 s
  cpu-seconds; wall 331.8 s vs 600 s wall-seconds; ... -> OVER" (reported
  only; no checks fail on seconds).

<!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict; python project-trajectory/scripts/check_docs.py --root .; python project-trajectory/scripts/run_menu.py smoke; then python project-trajectory/scripts/check_docs.py --root . --stale && python scripts/check_resync.py && python scripts/check_smoke_budget.py --mode warn" rev="maint/wi-1071 close-out tree before its last Deliverable edit" -->

**Acts owed to the next automated adjudication sitting.**
- **Amendments to `Accepted` rows** (text only): LLR-039 `Detail`; LLR-047
  `Detail`; LLR-199 `Detail`; LLR-281 `Detail`; LLR-300 `Detail`; TC-042
  `Method`, `Expected`; TC-047 `Method`, `Expected`; TC-195 `Method`;
  TC-291 `Method`, `Expected`; TC-316 `Method`; TC-398 `Method`,
  `Expected`. Against their recorded copies, LLR-047's, LLR-199's and
  LLR-281's owed amendment also carries slice 1's `Rationale`, and
  LLR-039's, LLR-047's, LLR-199's, LLR-281's and TC-398's were already owed
  from the eighth sitting; their re-sitting reads this text.
- **Routed traced changes to `Accepted` rows**: TC-316 `Verifies` (IF-277
  removed); LLR-039, LLR-047, LLR-199 and LLR-281 `Constrains` (slice 1's,
  unchanged here, still owed).
- **`Drafted` rows owed a first acceptance**: TC-530 and TC-571
  (rewritten); LLR-423 (unchanged) and TC-533 (its evidence gains a test
  and its `verifies` gains IF-277).
- No act: the regenerated `Evidence` of TC-047, TC-195, TC-291, TC-316,
  TC-339, TC-530 and TC-533 (trace cells no adjudicator judges).

**Left for the coordinator.**
- The component view's header and the generator's module docstring still
  say a design row sits at the owner of each interface "a test case
  verifying it names", which LLR-403's placement through `constrains` has
  outgrown (D13). The restored LLR-199 clause names only the header's four
  elements. A shipped file and the committed view change with it, so it
  is a row of its own.
- `trace.py --root . --strict` exits 1 on this branch and on its base, with
  the build's changes stashed, on one finding outside this row: "FINDING
  (requirement form): LLR LLR-484 Detail uses 'such as' — the scope cannot
  be closed, so the row cannot be completed — enumerate it". LLR-484 was
  accepted by the eighth sitting and this row does not amend it. The
  per-commit checks (`run_menu.py smoke`) stop at that step for the same
  reason, so trunk's are red until LLR-484 is amended.
- TC-533 citing IF-277 (above) is a choice the coordinator may overrule.
- LLR-300 stays one row (D8): a sitting may still judge it as several
  obligations, and a split would be its own row.

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, to answer
the eighth automated adjudication sitting's verdict (WI-1068, sitting A,
Gemini Neon; the specref): its second and third `## amendment`
dispositions and its three `## first-acceptance` dispositions. They are
one row because each is small and text-led and none waits on another.
WI-1070 answers the first amendment disposition (the brief's gap).

**Dropped clauses (MEANING, not blessed; each still `Accepted`, owed at
its recorded text).** WI-1024's slice 1 rewrote these rows without code
names, and the sitting found the rewrite dropped obligations:
1. LLR-047: no interpolation in the run-capability parse; capability names
   keep their case; an orphan `.desc` and an empty-value command are
   dropped.
2. LLR-039: a freshness failure on a document edit and on a missing bundle
   file; the legacy opt-out sentinel; JSON-quoted YAML scalars (the rewrite
   says "quoted").
3. LLR-199: the unplaced design rows in the counted unplaced table; the
   staleness header; the trunk regeneration wiring (beside adopting
   LLR-403's placement).
4. LLR-281: the `SHORT` output marker and that the floor is checked first.

For each clause the builder reads the code: a clause the code still
enforces is restated in the row, without code names, unless an accepted
spine row already states it (named in the Deliverable; an interface row is
off-spine and no sitting reads it, so it is not such a home); a clause the
code no longer enforces is reported, and the row's text says what holds.
These rows also carry a `constrains` link WI-1070's brief must show, so
their re-sitting follows both rows.

**TC-398 (MEANING, not blessed).** LLR-359 now says an unequal-identity
refusal names the row and both digests; TC-398's method and expected check
only that it names the row. TC-398 states and a test asserts both digests.

**TC-530 (RETURN; `Drafted`).** Its method adds `constrains` and
`dimensions` (an accepted cell) to one design row in one commit, which
masks whether a `constrains`-only change routes to adjudication with no
accepted cell moved. Its method, expected and tests separate the two.
LLR-420 was accepted by this sitting and is not amended here.

**TC-571 (RETURN; `Drafted`).** Its expected says a row's other moved
trace cells show under the label owing no act, but its method moves them
only on a row that lists no chain. Its method names a rendered row that
also moves another trace cell (the test that drives the three labels
together already does). LLR-484 was accepted and is not amended here.

**LLR-423 and TC-533 (RETURN; `Drafted`).** LLR-423 states that the
coordinator guard identifies a claim's caller by the agent tool's exported
session variable; the accepted LLR-300 states the same, and TC-316 checks
it beside TC-533. One decision gets one home. WI-1024's slice 1 wrote
LLR-423 as a focused row for IF-277 beside the large LLR-300 (its record,
§6 item 1). **Settled at the scope critique:** LLR-423 and TC-533 stay the
one home; the session-variable clause is removed from LLR-300 (text only,
still `Accepted`, owed), whose lease-admission obligations stay, and
TC-316's check of it moves to TC-533 (TC-316 amended in text, owed).
LLR-423 and TC-533 stay `Drafted` for the next sitting.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1071.md`): `planmode` is `single`, and the
session-variable decision's home is settled (above).

## Done-when

- [x] LLR-047, LLR-039, LLR-199 and LLR-281 each state every obligation the
      code enforces that the slice's rewrite dropped, or the Deliverable
      names the accepted row that states it, or reports that the code no
      longer enforces it; text only, each still `Accepted`, owed.
- [x] TC-398 states and a test asserts that an unequal-identity refusal
      names both digests (red first where the assertion is new).
- [x] TC-530 drives a `constrains`-only change, with no accepted cell
      moved, through the amendment walk and the trunk mint, apart from the
      accepted-cell change.
- [x] TC-571's method names a rendered row that moves another trace cell,
      matching its expected.
- [x] The session-variable decision has one home, LLR-423 (verified by
      TC-533): LLR-300 no longer states it and TC-316 no longer checks it,
      and each test that drove it is named by TC-533.
- [x] Each row it touches keeps the three row rules (no code names,
      inherited ones included; one obligation with every clause tested; a
      child within its parent).
