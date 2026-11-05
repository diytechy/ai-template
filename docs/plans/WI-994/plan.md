# WI-994 plan, revision 2: test files name their test cases on the `Implements:` line, read by the one back-link reader

Planned against lane `C:/Projects/ai-template.wt/wi-994`, head `b6da86733`.

Read in full: the spec `docs/work/active/wi-994/WI-994-test-files-tag-their-tcs.md` and its `specref` target (review-churn plan item 13). Also read: SR-157 in `docs/requirements/system-requirements.toml`, the TCs verifying it in `docs/test/test-cases.toml`, IF-131, IF-199 and IF-263 in `docs/requirements/interfaces.toml`, CMP-006 in `docs/requirements/components.toml`, `docs/runtime-flows.md`, and the code named below.

Measured for revision 1, in memory, with nothing written. A prototype of the grammar below, run over `tests/`, read 279 `.py` files and 8307 defs and classes and gave **0 findings** in 3.2 s on a loaded box. All 11 token hits are backticked or mid-sentence. No non-`.py` file under `tests/` has an extension in `BACKLINK_EXTS`, and no `test*` def or `Test*` class sits inside a module-scope `if`, `try` or `with`. The commits since then touch only `docs/plans/WI-994/` and telemetry, so the measure stands.

## What this revision changes, and why

**F1 is confirmed.** `test_module_size_ratchet` is not in `SLOW_MODULES`, so `test_module_sizes_exactly_match_the_committed_baseline` runs in the smoke tier, and its `grew` arm refuses any `gen_arch_map.py` count above the pinned 1433. Revision 1 put the reader in the first shipped commit and its stamp four steps later, so that commit could not pass the bar.

**The class is wider than the one stamp.** F1 is one case of "a later row repairs what an earlier commit needs". Checking every row against the bar and the lane cycle found four more, each corrected here:

1. **Revision 1's Commit boundary reasoning was wrong.** It said P2's red tests "could not pass" the bar. Both new-test modules are in `SLOW_MODULES`, so the smoke tier does not run them, and `coordinator-cycle` §3 Intent commits red tests under strict xfail marks, which pass `attest --tests`.
2. **Tests go alone, before the code** (`coordinator-cycle` §3 Intent, step 2). Revision 1 merged tests and reader into one commit. Revision 1's stub in `gen_arch_map.py` also made the tests commit a shipped change, which pulls in a RESYNC entry and a stamp. The stub moves into the test module, so the tests commit touches no shipped file and can owe neither.
3. **Trace fields are authored with the rows, not after the code.** `spine-authoring/references/in-lane.md`: TC `Evidence` and LLR `Module` and symbols "name the tests and symbols the build will create", and interface rows are part of the one change set. Revision 1 filled evidence and IF edits in P7. They move to P1.
4. **An altered interface row has a citing TC** (`in-lane.md`, the closure edges). Revision 1 altered IF-131 and left it uncited. TC-f now cites IF-131 and IF-263 (see decision 16).

**The rule that ends the class.** A row that moves a ratcheted size carries that size's exact stamp and its reason in the same row. A commit can hold several whole rows, but it never splits a row from its stamp, and no row repairs an earlier one. The same holds after this plan: a review-round fix or rebase that moves a count re-stamps in that commit. `test_module_sizes_exactly_match_the_committed_baseline` and the byte-cap tests enforce it at each attest.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The spec's own S5 answer holds, and this revision does not change it. Each step's result:

1. **Mode classes (A2).** None added. The reader is a pure function of the files, and the check keeps no state. No flow in `docs/runtime-flows.md` names `check_trajectory`, `trajectory_arch` or `gen_arch_map` (Flows 1–9), so no flow is edited.
2. **Value domains (A3, A6).** Values are added, in scope, and recorded as interface edits in P1.
   - IF-131 gains `read_test_tags(root, tests_dir, live_tcs)`, which returns `({TC id: sorted node ids}, [finding])`. A finding carries `file`, `line`, `shape` and `detail`, and `shape` is one of `misplaced`, `malformed`, `unknown`, `unreadable`. Those four are the added domain values.
   - IF-263 gains `tc_tag_findings(root, tests_dir)`, which returns finding strings. Its stated input widens from "the spine/config files" to include the test files under the declared tests root.
   - IF-199 is unchanged. `backlink_ids`, `IMPLEMENTS_MARKER` and `BACKLINK_EXTS` are read and not altered.
3. **Output-on-input dependencies (A4).** One new cell, recorded here as the skill allows when planning:

   | Output | Inputs today | Input added |
   |---|---|---|
   | `check_trajectory` WARN/ERROR lines and exit code | registries, work specs, source AST, stack profile | the files under `[paths] tests` (the TC registry was already an input) |
   | Map column, reverse coverage, CodeSymbol crosscheck, `check_test_first` | `[paths] src` | none |
   | `trace.py --tests-for`, review-bar inputs | TC `evidence` cells | none |

4. **Descent (A8).** Requirement descent: one new LLR under SR-157 (P1). Component descent: both modules are CMP-006 and already joined over IF-131, so there is no cut, no sub-component, no edit to `docs/requirements/components.toml` and no new boundary. The default is IF-131's `data` cell. If in-lane adjudication rules a separate seam instead, P7 adds that row and nothing else moves.

The change is carried by P3 and P4 (the input, the domain values and the contract bodies) and P1 (the interface rows). It needs no refactor, so `beyond` does not apply. `gen_arch_map.py` grows past its stamp by a reviewed bump (see "Budgets"). Its decomposition debt stays with its named owner.

## Decisions the spec leaves to the build

Each point below is a place where the spec, read against the code, needs an answer. The critic should check them first.

1. **D1's "same output before and after" cannot be a stored golden.** D14 puts an `Implements:` line in `gen_arch_map.py`, so `scan_backlinks` over the scripts gains the new LLR's entry. Every `lineno` below the reader shifts in `implements_report`, and `known_names` gains the new functions. Any later WI would also stale a stored copy. The clause therefore holds as *the same functions give the same output over the same tree*, in two parts:
   - a durable regression (P2): a frozen oracle in the test, which is the pre-change line rule transcribed, recomputes both reports over the live tree and must equal them, with `inspect.signature` pins on all four functions;
   - a one-off differential (P3): the base commit's `gen_arch_map.py`, taken by `git show` into the review scratch, against the lane's copy, both over the lane's `project-trajectory/scripts`, stated in the log.
2. **`_tests_dir` cannot be called from `trajectory_arch`.** It lives in `check_trajectory.py`, which imports `trajectory_arch`. The call site passes the value in: `tc_tag_findings(root, _tests_dir(root))`. Nothing moves.
3. **The reader needs the repo root.** `_walk_roots` makes paths relative to `root.parent`, so a nested `[paths] tests = qa/tests` would give `tests/x.py`, not the repo-relative node id the grammar states. The reader takes `root` and the declared value, keeps `_walk_roots` for the hidden-path rule, and computes `path.relative_to(root)`.
4. **Vacuity.** D3's "no tests root or no TC registry and no tags" is read as three vacuous conditions, matching the Trust section's ruling. No tests root returns `[]`, and so does no TC registry (`spine_carrier.resolve` gives None), before any file is read. A registry that exists with only `-000` rows is not vacuous: every tag in that repo is `unknown`. `[arch-map] mode = files` is **not** a vacuity condition, so the CodeSymbol crosscheck's guard is not copied.
5. **Which loop.** "Beside the CodeSymbol crosscheck" names where the function sits in `trajectory_arch.py`. Its call joins the promotable loop with `contract_body_findings`, feeding `if_tc_errors`, and not the advisory loop that holds `codesymbol_crosscheck_findings`, which never reaches the exit code. `if_tc_errors` also reaches the no-work-items return. The `--staged` branch returns before this point and is unchanged. The call is one more term in the existing `for msg in (…)` expression, so it adds no branch, and `check_trajectory.main`'s row in `docs/complexity-baseline` holds.
6. **Fail-closed reads.**
   - Files are read with `encoding="utf-8-sig"`. `ast.parse` refuses a leading U+FEFF (measured), so a plain UTF-8 read would call a valid BOM'd file unreadable.
   - The parse catches `SyntaxError` and `ValueError`, and the tokenize pass catches `tokenize.TokenError`.
   - Any `.py` under the root that fails is `unreadable`, conftest and fixture modules included. The closed rule cannot be proven over a file that cannot be read.
   - So a deliberately unparseable fixture module under an adopter's tests root is refused. The RESYNC entry says so: move it out of the root, or change its suffix.
7. **Absent or older sibling.** IF-131's body says every entry point is optional and "an absent or older copy" degrades to silence. That contradicts the Trust section for this reader. `tc_tag_findings` keeps the module's `gen_arch_map is None` guard, because no supported route removes a kit-owned file. It takes **no** `hasattr` guard, so a stale copy fails loudly rather than reading as "no tags". The Contract IF-131 body states the exception (P3).
8. **What counts as a declaration outside a read position.** The token opening its line or its comment is a declaration, with or without ids, and is `misplaced`. The rule is applied to each `tokenize` COMMENT token's text, so a trailing `def test_x():  # Implements: TC-1` is refused too ("any comment"). A token after prose outside a read position is a mention. The token-after-prose malformed shape applies only at read positions and only when a TC id follows the token.
9. **A backtick before the token is a mention, at read positions too.** Without this, a test docstring saying `` `Implements: TC-12` `` would be refused by the token-after-prose rule. The grammar says it is a mention.
10. **A wrap with no trailing comma.** The grammar lists "a list wrapped onto the next line". `Implements: TC-1,` fails on its own line. `Implements: TC-1` followed by a bare `TC-2` line does not, so the reader also refuses the line straight after a valid declaration when a spine id opens it (the opening rule applied up to the first `IMPLEMENTS_RE` match). This mirrors `_refuse_ambiguous_continuation`, which holds the same rule for `Contracts:`. A blank line ends the check.
11. **"Nothing else on the line" is literal.** `/* Implements: TC-1 */` in a non-Python file is `malformed` because of its `*/`. The message says to use a line comment or give the tag its own line.
12. **Names.** No new function starts `test_`: `read_test_tags` and `tc_tag_findings`. A `test_*` name re-exported into a module that a test file imports risks pytest collecting it.
13. **`EXAMPLE.md` §5.** Its Rust test sits beside the code in one snippet, but a file-level tag is read only under the tests root. The test moves to a labelled `tests/` file so that `// Implements: TC-001` is true of what the kit reads.
14. **`ADOPTING.md` line 226** says "put the id in the test name", the retired rule. D13 does not list it, but leaving it would contradict the one home, so P6 changes that phrase.
15. **Spine row text.** LLR-364's shape keeps the `module` and `code_symbol` cells, which the CodeSymbol crosscheck needs. "No code named in the row text" is applied to `title`, `detail`, `rationale` and the TC rows' prose.
16. **IF-131 is cited, and its allowlist line stays.** No TC cites IF-131 today, and `in-lane.md` wants a citing TC on an altered row, so TC-f's `verifies` names IF-131 and IF-263: its tests drive `check_trajectory` through that seam. Revision 1's "the new TCs cover one entry point, not the seam" is withdrawn. The `docs/if-tc-coverage-allow` line is left alone. A listed seam gaining a TC is `if_tc_allow_hygiene_findings`' warn-only housekeeping (14 listed seams already read that way), and IF-131 sits inside the pinned seeded 116, so pruning it would move `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`'s pin for no gain to this row.
17. **The tests' stand-in lives in the test module.** P2's reader tests call one helper, `getattr(gen_arch_map, "read_test_tags", lambda root, tests_dir, live_tcs: ({}, []))`. So each test goes red at its own assertion, as a shipped stub would, with no shipped file touched. P3 deletes the helper's fallback with the marks, and the tests then call the reader directly, so nothing of it outlives one commit.

Found outside this row, not changed: IF-131's `requestors` still says `scripts/check_trajectory`, though the caller has been `trajectory_arch` since the split. No interface row declares that pair. It is intra-CMP-006, and the in-lane adjudication can rule on it.

## The reader's shape (P3)

Below `declaration_sites` in `gen_arch_map.py`, as small functions under the complexity threshold (`docs/complexity-baseline` only tightens, so no new row):

- `_tc_id_list(text)`: `text.split(",")`, with each part stripped, a full match of `IMPLEMENTS_RE` and starting `TC-`. There is no second id grammar. An empty list, a trailing comma, `and`, a range, `TC-1 TC-2` and any SN, SR or LLR id all fail it.
- `_tag_line(line)`: `line.partition(IMPLEMENTS_MARKER)`, then `_DECL_OPENING`. It returns the ids through `backlink_ids(line)` for a valid line, and the malformed detail otherwise.
- `_docstring_sites(node, scope, in_test_scope)`: one recursion over `ast.iter_child_nodes`, yielding each def's and class's docstring with its node suffix, or None when it is closed. A `test*` def is a test only while `in_test_scope` holds. A `Test*` class keeps it, any other class or any def clears it, and other statements pass it through. So a test under a module-scope `if` is a test, and a def inside a test is not.
- `_read_python_tags`, `_read_text_tags`: one file each. Line numbers are the docstring node's `lineno` plus the line's offset.
- `read_test_tags(root, tests_dir, live_tcs)`: the walk, `test_*.py` / `*_test.py` against every other `.py`, `BACKLINK_EXTS` for the rest, the union, and findings sorted by file, line and shape.

A malformed line yields one finding and no ids. A valid line naming one live and one unknown id maps the live id and adds one `unknown` finding. Its docstring carries its own `Implements: SR-157, LLR-<new>` line, and no other line in the new code or its comments may open with the token. Imports added: `io`, `tokenize`, stdlib only, so no ledger row.

## Build table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The spine set on reserved ids: one LLR, six TCs with their evidence cells, the IF-131 and IF-263 data edits | D14; D17; SR-157 | IF-131; IF-263 | |
| P2 | The tests alone, under strict xfail marks, with the code-side characterisation pin; no shipped file | D1; D2; D4; D5; D6; D7; D8; D9; D10; D11; D12; SR-157; TC-200 | IF-131; IF-199; IF-263 | P1 |
| P3 | The reader in gen_arch_map.py, with its contract body, its exact size stamp and the stamp's reason | D1; D2; D5; D6; D7; D8; D9; D10; D12; D17; F1; SR-157; TC-200 | IF-131; IF-199 | P2 |
| P4 | The surface: tc_tag_findings through check_trajectory, with its contract body and exact size stamp | D3; D4; D11; D12; D17; F1; SR-157; TC-037; TC-075; TC-077; TC-100 | IF-131; IF-263 | P3 |
| P5 | The RESYNC entry | D15; D16; SR-157 | no interface: reference doc | P3; P4 |
| P6 | One home for the rule, in text, with the byte stamps and the skill sync | D13; F1; SR-157 | no interface: documentation only | P4; P5 |
| P7 | Reconcile the set against settled code, close its edges, take the in-lane adjudication | D14; SR-157 | IF-131; IF-263 | P4 |
| P8 | The log, the timing and the closing checks | D3; D16; D18; SR-157; TC-200 | IF-131; IF-263 | P6; P7 |

Excludes: TC-001; TC-002; TC-003; TC-004; TC-005; TC-126; TC-127; TC-128; TC-174; TC-193; TC-197; TC-255; TC-270; TC-273; TC-275 — they verify SR-157's spine-row rules in `trace.py`, `trace_text.py`, `kitlib/spine.py`, `coherence.py` and `absolute_terms.py` (joins, integrity, form, vocabulary, tier agreement, cell presence); none reads a test-file tag, and this row changes none of those modules. The six new TCs take `Full` with evidence in `SLOW_MODULES`, which agrees with TC-255's rule.
Excludes: TC-086 — it verifies the critique vocabulary and the critique closure ratchet; the ratchet runs in the `--staged` branch, which returns before the new check, so its path is unchanged.
Excludes: TC-155 — it verifies the queue-overlap pre-filter in `check_trajectory.py`, a separate rule over the work registry that reads neither test files nor this finding.
Excludes: D19 — the A+B review bar is what the coordinator runs on the built lane; no build step delivers it. The handoff to review names it.

**Why some clauses span several rows.** The gate reports these as multi-covered, so each split is stated here.
- D1: P2 writes its regression, and P3 delivers the reader and the differential.
- D2 and D5–D10: P2 writes the tests, and P3 delivers the behaviour.
- D3: P4 delivers the surface, and P8 measures its time and its landing green.
- D4: P2 writes both suites' tests, and P4 turns the surface suite green.
- D11: P2 writes the test, and P4 delivers the behaviour.
- D12: P2 writes the tests, P3 delivers the reader's refusal, and P4 the same refusal reading the real registry.
- D14: P1 authors the rows, and P7 reconciles them and takes the adjudication.
- D16: the list is stated in two places, the RESYNC entry (P5) and the log (P8).
- D17: P1 states the bound, and P3 and P4 hold to it and drive it.
- F1: each row that moves a ratcheted size carries its own stamp, which is the fix: P3 and P4 for SLOC, P6 for bytes.

## Commits and what each one owes the bar

Every row is whole inside one commit. All commits go through `integrate.py attest --bar review --tests tests/test_gen_arch_map.py tests/test_trajectory_arch.py tests/test_trajectory.py`, except C6, which is records-only. The bar's steps are `trace.py --strict`, `check_trajectory.py --strict`, `check_docs.py --stale`, `check_resync.py` and the smoke tier.

| Commit | Rows | Shipped file | Stamps it carries | Why the bar is green at this commit |
|---|---|---|---|---|
| C1 | P1 | none | none | Rows stay `Drafted` and the ids are reserved first, so the watermark pin holds. `check_resync` sees no shipped path. `read_test_tags` named in IF-131's `data` before it exists is `if_data_advisories`' warn-first line, not a failure, and it clears at C3. |
| C2 | P2 | none | none | `check_resync` sees no shipped path, and no script's size moves. Both test modules are in `SLOW_MODULES`, so the smoke count and `max-tests` do not move. `attest --tests` runs them: red cases report `xfailed`, and the characterisation pin passes. |
| C3 | P3, P4, P5 | `gen_arch_map.py`, `trajectory_arch.py`, `check_trajectory.py`, `RESYNC_PACK.md` | `gen_arch_map.py` and `check_trajectory.py` in `tests/test_module_size_ratchet.py`, with the reason in the same commit's log fragment | The stamps match the census. `check_resync` finds the entry anchored at the base. Marks and the stand-in are gone, so the reader and surface tests run for real. `check_trajectory.py --strict` now reads `tests/`, including P2's own new tests. |
| C4 | P6 | the three text files | byte stamps, the skill's size table, `bootstrap.py --dest . --sync` | The entry from C3 covers these shipped paths. `test_capped_doc_baselines_match_the_real_sizes` and the byte-cap tests see the new sizes in the same commit. |
| C5 | P7 | none unless a return moves code | any count a return moves | Row text, verdicts and acts, as the cycle's checkpoint orders them. |
| C6 | P8 | none | none | Record-only: the log fragment and the Done-when ticks. A tick does not unbind the pass record. |

Why P3, P4 and P5 share a commit: `attest` commits one staged round and refuses a tree holding work the index does not, the cycle's code commit removes all the marks, and P5's entry states refusals that only P4 delivers. Review rounds sit between C4 and C5, as the cycle orders them, and each round's fix commit keeps the stamp rule above.

## The steps

### P1. The spine set

Reserve first: `trace.py --reserve-ids WI-994 LLR=1,TC=6`. The lane's spine author writes the set once, from the anchor down, with an arms map. Rows stay `Drafted`. Interface rows have no status.

- **LLR**, under SR-157, component CMP-006. In contract voice with no code named: a test file names the cases it runs on the back-link declaration line; the read positions; the union of levels; the four refusals, each naming file, line and shape; a tag can only add a finding; reading test files changes no reading of source files. The `detail` closes with D17's coverage bound in the form LLR-364 uses ("The contract covers …; … are outside it"). `module` is `project-trajectory/scripts/gen_arch_map.py;project-trajectory/scripts/trajectory_arch.py`, and `code_symbol` is `read_test_tags/tc_tag_findings`.
- **Six TCs**, `verifies = ["SR-157", "LLR-<new>"]`, `tier = "Full"` because both test modules are in `SLOW_MODULES`, `evidence` naming P2's nodes by the TC column of its tables:
  - TC-a, the read positions, the union, and the source-side reads unchanged;
  - TC-b, misplaced;
  - TC-c, malformed;
  - TC-d, unknown (`-000`, absent and retired ids; Drafted is clean);
  - TC-e, unreadable;
  - TC-f, the surface (severity, vacuity, the scaffold, the rung), which also names IF-131 and IF-263 in `verifies` (decision 16).
- **`interfaces.toml`:** IF-131's `data` gains `read_test_tags`, and IF-263's `data` gains test-file tags.

The tests' names below are the evidence cells' contract. A builder who renames one keeps the cell current in the same commit. The lane's new tests carry **no** `Implements:` tag: WI-997 seeds tags, and this row tags nothing.

### P2. The tests alone (`tests/test_gen_arch_map.py`, `tests/test_trajectory_arch.py`)

Each red test takes `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`, the evidence class for new behaviour. Three rules keep those reds honest:

- Reader tests go through decision 17's helper. Surface tests drive `check_trajectory` by `run_traj`, which needs no stand-in at all.
- A test compares whole values (`assert findings == [...]`) and never indexes a result. `findings[0]` on an empty list raises `IndexError`, which the mark's `raises` does not admit, and that would red the attest for the wrong reason.
- Each marked test has a positive half that is red before P3, because a strict mark fails on an unexpected pass.

Fixture text lives only in string literals. A new test's own docstring and comments use backticks, because the strict bar reads these files from C3.

Reader tests, `tests/test_gen_arch_map.py`:

| Test | TC | Clause | Fails before the change because |
|---|---|---|---|
| `test_the_tag_reader_reads_each_python_read_position` (module, function, async, method, nested `Test*` class, a test under a module-scope `if`, a parametrized test as one node) | a | D5 | the map is empty |
| `test_tags_at_both_levels_union_and_a_repeat_is_clean` | a | D2 | the map is empty |
| `test_a_non_python_test_file_is_read_at_file_level` (`.rs` file tag; a `.txt` file is not read) | a | D2 | the map is empty |
| `test_each_misplaced_shape_is_named` (parametrized: helper, fixture, class, nested def, method of a non-`Test*` class, `conftest.py` module docstring, non-test module docstring) | b | D6 | no finding |
| `test_a_comment_tag_above_a_test_is_misplaced` (above the test, and trailing) | b | D9 | no finding |
| `test_each_malformed_shape_is_named` (parametrized: empty list, trailing comma, wrap with comma, wrap with no comma, SN, SR, LLR, a mixed list, prose after, `and`, a range, no comma, `/* … */`) | c | D6 | no finding |
| `test_a_one_line_docstring_with_the_token_after_prose_is_malformed` (and the message says to start its own line) | c | D8 | no finding |
| `test_a_backticked_token_is_a_mention` (beside a real tag, which must still map) | c | D2 | the real tag is missing |
| `test_a_fixture_string_opening_a_line_with_the_token_is_no_tag` (an `Implements: SR-001` string, beside a real tag) | a | D7 | the real tag is missing |
| `test_a_tag_naming_no_live_tc_is_unknown` (absent, a `-000` id, and a live id on the same line still mapping) | d | D12 | no finding |
| `test_a_file_that_cannot_be_read_is_refused` (a syntax error, non-UTF-8 `.py`, non-UTF-8 `.rs`, an unparseable `conftest.py`) | e | D10 | no finding |
| `test_a_bom_file_reads_its_tags` | e | D2 | the map is empty |

Each finding test asserts file, line and shape. D7's and the mention test pair the negative with a positive, because a negative alone would pass before the change.

Surface tests, `tests/test_trajectory_arch.py`, all TC-f except where named:

| Test | Clause | Fails before the change because |
|---|---|---|
| `test_tag_findings_warn_plain_and_error_under_strict` (exit 0 with a WARN line; exit 1 with an ERROR line naming file, line and shape; and on a repo with no work items) | D3 | no WARN, exit 0 under `--strict` |
| `test_the_tag_check_is_vacuous_with_no_tests_root_or_no_registry` (paired with the same tree holding a registry, which gives a finding) | D3 | the paired half has no finding |
| `test_a_nested_tests_root_reports_repo_relative_paths` | D3 | no finding |
| `test_a_draft_tc_is_clean_and_an_absent_one_is_refused` (TC-d: a `Drafted` row clean with its node mapped; a `-000` row refused; a row deleted from the registry, the retired shape, refused) | D11; D12 | the refused halves have no finding |
| `test_the_tag_check_on_a_bootstrapped_scaffold` (`scaffold` fixture: a clean tag; a bad tag fails `check.py --stage DevStg-Impl` in the trajectory step and stays a WARN below that rung) | D3; D17 | no finding |

The characterisation pin, `tests/test_gen_arch_map.py`, TC-a, **unmarked**:

- `test_the_code_side_readers_keep_their_output_over_the_scripts_tree`: the oracle of decision 1, plus signature pins. It describes already-correct behaviour, so it is green before the change by design, and the plan claims no red. As the cycle requires, its docstring states the adequacy witness: the wrong implementation it catches is a reader that loosens `_DECL_OPENING` or widens `scan_backlinks` to test ids. To show it can fail, the builder alters `_DECL_OPENING` in scratch once, sees it red, restores it, and states that in the log.

### P3. The reader

As "The reader's shape" above, plus, in this row:

- The fixture helper's fallback and the reader tests' marks go. `test_backlink_ids_is_the_one_definition_of_a_declaration` (TC-200) stays green.
- Contract IF-131 body in `gen_arch_map.py`'s header names the reader and states decision 7's exception.
- **The stamp:** `tests/test_module_size_ratchet.py` `"gen_arch_map.py"` takes the exact new count, with a dated `+N (1433 -> M)` comment giving the reason. Red before the stamp: `test_module_sizes_exactly_match_the_committed_baseline`, on the `grew` arm.
- **The stamp's reason in the log:** `docs/log.d/WI-994-test-files-tag-their-tcs.md` starts here, with its `## <date> — <title>` heading and the bump's reason, because the ratchet asks for the reason in the log. P8 completes the fragment.
- The base differential of decision 1, run once, with its result in the fragment.

### P4. The surface (`trajectory_arch.py`, `check_trajectory.py`)

The real function, about 20 SLOC beside `codesymbol_crosscheck_findings`. Live ids come from `spine_carrier.load(root / TC_CSV, "TC-ID", False)`, which drops `-000`, with no status filter. The vocabulary has no retired status, since a retired row is deleted.

- The name goes in `__all__` and in `check_trajectory`'s binding list, and the call joins the loop (decision 5).
- The rule gets a paragraph in `check_trajectory`'s module docstring beside the seam-TC coverage paragraph.
- `Implements: SR-157, LLR-<new>` goes on `tc_tag_findings`.
- Contract IF-263 body in `trajectory_arch.py`'s header widens its inputs.
- The surface tests' marks go.
- **The stamp:** `"check_trajectory.py"` takes its exact new count and comment, and the fragment takes the reason. Red before it: the same ratchet test. `trajectory_arch.py` stands at 960 against the 1000 threshold, so it stays under and takes no baseline row.

`tests/test_trajectory.py` runs by name for TC-037, TC-075, TC-077 and TC-100, since `main` changes.

### P5. The RESYNC entry

Heading: `### Test files name their test cases on the `Implements:` line [since <merge-base>]`, followed by the pack's "*(Anchored at the preceding commit: the change lands in the commit after it.)*" line. A commit cannot name its own sha, and `check_resync.py` requires the anchor at the base. D15's "anchored at the trunk commit carrying the reader" is that convention. The entry is re-anchored if the lane rebases, which `check_resync` counts as zero new headings.

The body takes D15's **What changed** and **What to do** as written, adding the unparseable-fixture sentence (decision 6) and `/* … */` (decision 11). D16's "Not in this row" list is stated in the entry. **Kit-owned files — overwrite:** `scripts/gen_arch_map.py`, `scripts/check_trajectory.py`, `scripts/trajectory_arch.py`. **Adopter-merged files:** the `AGENTS.md` and PROCESS text.

Red before it: `scripts/check_resync.py` exits 1 naming the three scripts, the moment P3 and P4 stage.

### P6. Text

- `PROCESS.md` §3 line 179: the tag rule replaces "test names embed the verified ID". This is the one statement of it.
- `AGENTS.template.md` lines 82–84: follows and links.
- `EXAMPLE.md` §5: decision 13, and line 225's sentence.
- `ADOPTING.md`: decision 14.
- `docs/registry-machinery-reference.md` §5: a test-file tags paragraph before §5.1, naming the rule and `check_trajectory` as enforcer.
- `docs/enforcement-audit.md`: a row beside line 80.

Run the `byte-budget-guard` procedure before and after. `AGENTS.template.md` stands at **9,998 of 10,000**, so the added link must be paid for in the same file. PROCESS.md is watched and is re-stamped with its delta. If a size moves, this row restamps the skill's table in `project-trajectory/skills/` and runs `bootstrap.py --dest . --sync` for its mirrors, in the same commit, or `skills-sync` refuses it. `test_capped_doc_baselines_match_the_real_sizes` and the byte-cap tests decide it. These are the only tests that can go red here, and they are red until the stamp is in.

### P7. Reconcile and adjudicate

This runs at the cycle's checkpoint, after a counted round with no BLOCKER or MAJOR. The spine author reconciles the set against settled code. Then the closure check runs: parents, the arms map, TC to LLR and SR, interface citations, `trace.py --strict` and `check_trajectory.py --strict`. One combined sitting then judges the LLR, the TCs and the IF edits (D14). A ruling for a new IF row is applied here. No new test: the sitting is the evidence.

### P8. Log and closing checks

- `docs/log.d/WI-994-test-files-tag-their-tcs.md` gains D3's added wall time (`check_trajectory.py --strict` before and after, on a quiet box, on a `fig:` line with its producing command and revision), D16's "Not in this row", and the characterisation pin's deliberate red.
- D18: confirm `docs/work/queued/WI-997-tag-this-repos-test-files.md` is on trunk (it is, at `512b9e6e7`) and tick the item.
- `run.cmd smoke`, whose `check_trajectory.py --strict` is D3's "lands green": 0 findings on the real tree, the new tests included.
- Trunk-only views (`docs/interface-reference.md`, `docs/cli-reference.md`, `components.derived.toml`, `PROJECT_STATE.html`) are not committed on the lane. They regenerate at landing through `trunk_step.py --regen`. No Done-when asks for one fresh. The module-size stamp stays with the lane.

## Budgets

- `gen_arch_map.py`: exact ratchet at 1433 SLOC. The reader adds about 90, a reviewed bump stamped in P3 with its reason in the ratchet comment and the log. The spec fixes the reader's home, so no split is planned.
- `check_trajectory.py`: exact ratchet at 1656, about +2, stamped in P4.
- `trajectory_arch.py`: unbaselined at 960. If it would cross 1000 the surface is trimmed; it is not baselined.
- New functions and tests stay under the cognitive threshold (`check_complexity` also reads `tests/`).
- Wall time: about 3 s on a loaded box, 1.3 s in the spec's measure, per `check_trajectory` run over this repo. The commit bar reports it, and the log states the quiet figure.

## Coverage bound

D17's inside set is driven: a builder's or re-sync's tags by P2's reader tests, a retired row by the deleted-row case, and the scaffold by the scaffold test. Its outside set is stated in the LLR (P1) and is not tested. Dot-directories and `__pycache__` stay unread through `_walk_roots`, which matches pytest's default `norecursedirs`.
