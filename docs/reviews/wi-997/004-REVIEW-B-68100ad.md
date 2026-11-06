Reviewed: 68100ad8722f9a608067d01bb212c4b82c9253be

## Verified

Failure classes hunted first, in severity order: a silent fail-open of the equality check (a difference that reads clean), the seed changing a test's behaviour or losing docstring text, and the check being vacuous or red on an adopter's normal state. None reached BLOCKER or MAJOR.

The check. I drove the real `check_trajectory.py --strict` on 20 constructed repositories. Nested classes, async tests, subdirectories, a sibling directory beside the root, a trailing note, a `#anchor`, a parenthetical holding a path, a misplaced tag, a helper module, an unsupported file type, a `.` root and a Drafted note cell all read as the spec and LLR-366 state, with the one exception in the first finding. Six mutations of `_tag_evidence_findings` and `tc_tag_findings` on a scratch copy (keep the `[case]`, drop the tag arm, drop `refused`, drop the `is_dir` guard, two wrong prefixes) were each killed by the lane's tests, so the tests fail on a plausible wrong implementation.

The seed. My own AST comparison, base to tip, docstrings stripped: 214 of 217 changed test files are identical. The other three are `tests/conftest.py` (one tag inside the demo fixture's string), `tests/test_prompts.py` and `tests/test_trajectory_arch.py`, whose changes are the new tests and helpers. 2152 docstrings changed, and all but one differ only by a tag line; that one is the `_tc_rows` helper's own docstring, reworded with its new parameter. So no docstring text was lost. Seed commit 753c793e8 exists and is an ancestor of the tip. Through the shipped readers at the tip: 366 live TCs, 2322 parts, 8 outside the tests root (each an existing path), 2310 pairs, 0 reader findings, 0 unequal TCs by my own re-derivation.

Spec items read directly. TC-165 and TC-166 name WI-1000 and WI-999, both queued and matching those rows' SRs, and neither test file carries a tag for them. The retirement comment sits at `project-trajectory/scripts/trajectory_arch.py:1065`. The byte stamps are exact (PROCESS.md 99,216; byte-budget-guard SKILL.md 4,537), and all three skill mirrors are byte-identical. The RESYNC entry carries what the spec requires and follows the WI-994 anchor convention.

Done-when map:
- The tags: my AST and docstring comparison, `docs/plans/WI-997/seed-evidence.txt`, and the strict check. Its log statement is plan step P9, not written at this tip (`docs/log.d` is outside the reading scope): PENDING at close, not counted as a finding.
- The stale parts: `docs/decisions/wi-997.toml` D-002 to D-006, and 0 unequal TCs measured.
- The two moved cases: TC-412 `test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding`, D-007.
- The check: TC-410, and `check_trajectory.py --strict` clean on this tree.
- Regressions: each finding `test_evidence_without_a_tag_is_named`, `test_a_tag_without_evidence_is_named`; parametrized `test_a_parametrized_part_matches_its_tests_tag`; outside the root `test_a_part_outside_the_tests_root_is_ignored`; file-only `test_a_file_only_part_matches_a_module_tag_and_not_a_tests_tag`; Draft `test_a_draft_tc_is_judged`.
- The lane's own routine: `test_a_tests_evidence_arrives_with_its_tag_stated_at_one_home`. Its clauses are absent from `in-lane.md` at the parent 3f6778527 (grep count 0), so it fails on the pre-fix text.
- Sizes: `check_complexity` unchanged from baseline at the tip.
- Spine: rows present and each LLR-366 arm maps to a TC-410 to TC-412 clause; the in-lane sitting has not run, and by `coordinator-cycle` §3 follows the rounds: UNCOVERED at this tip, PENDING at the checkpoint, not counted as a finding.
- RESYNC entry, retirement, coverage bound: read and driven as above.

Requirement/interface relationships (semantic decisions, mine):
- IF-263 `data` changed; its counterparts are LLR-366 and requestor `scripts/check_trajectory`. Carried: TC-410 verifies IF-263 and the module header states the new output. Version v1 retained, justified: the channel and finding-string shape are unchanged, and the addition is two more values of one finding domain.
- IF-131 retained, justified: `read_test_tags` is already in its `data`, and only the caller's use of its first return changes.
- `kitlib.spine.evidence_items` has no IF row and is reused unchanged, so LLR-260 is retained.
- SR-157 is unchanged and its acceptance preserved: its own text puts a rule added at a declaration site in scope.
- LLR-365 is the counterpart that should change; see the finding below.
- Decomposition: LLR-366 is retained as one child because the equality rule is one decision, separate from LLR-365's grammar. It retires alone, and a split by arm adds no independent verification. TC-410 (the two findings and their severity at both rungs), TC-411 (what a part is and binds to) and TC-412 (what falls outside the rule) each verify an independent decision; further splitting adds none.
- Change intake (PROCESS.md §5): LLR-365 is "parent sound; LLR unsuitable" in one sentence, so the route is an LLR amendment preserving SR-157's acceptance. A RESYNC sentence alone leaves the approved row untrue.

Rubric: K1 raised below. K2: no carrier named in LLR-366 or TC-410 to TC-412 row text beyond the tier allowance. K3: both `Implements:` tags match LLR-366's `module` and `code_symbol`; no Status flips (363 Approved, 3 Drafted TCs). B1: every finding below was confirmed by running or reading.

Coverage-extension note: a whole-class part (`tests/test_a.py::TestC`) has no tag form and fails closed with `evidence without a tag`, and the RESYNC entry's "no tag form" list does not name it. No live cell here uses it.

## Commands

- `git rev-parse HEAD` -> 68100ad8722f9a608067d01bb212c4b82c9253be
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2B/wi-997 tests/test_trajectory_arch.py tests/test_trajectory.py tests/test_evidence_join.py tests/test_prompts.py` -> 299 passed, 20 warnings in 42.21s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (998 work item(s), 885 done (89%), 34 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=138 LLR=332 TC=366 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=4 budgets=4 budget-findings=0 ...
- `python project-trajectory/scripts/check_complexity.py --root . --mode enforce` -> check_complexity: OK - 183 row(s) over 15, unchanged from baseline.
- `.../r2B/probe/ast_cmp.py` -> same 214 diff 3
- `.../r2B/probe/doc_cmp.py` -> files 217 docstrings changed 2152 differ beyond tag line 1
- `.../r2B/probe/measure.py` -> rows 366, parts 2322, outside 8, pairs 2310, reader findings 0, unequal TCs 0
- `.../r2B/probe/scen.py` (20 scenarios through `check_trajectory.py --strict`) -> as stated above and in the first finding
- Six mutation runs on a scratch copy of the tip, 18 equality tests each -> base 18 passed; each mutant 1 to 5 failed
- `.../r2B/probe/mt.py` (`kitlib.spine.module_tests`) -> 'qa/tests' finds the file; './qa/tests' and '.' return []

The lane's working tree stayed clean (`git status --short` empty after every run). The full suite and smoke tier were not run, per the round facts.

## Findings

- [MINOR] project-trajectory/scripts/trajectory_arch.py:1087 -> B1: a part spelled `./tests/test_a.py::test_a` names a path under the root but fails `startswith(prefix)`, so with no tag the check exits 0 (driven: rc 0), while the same cell with its tag reads a false `tag without evidence`; no live cell uses the spelling, so this is improbable rather than reachable today -> normalize a leading `./` once in `kitlib.spine.evidence_items` (project-trajectory/scripts/kitlib/spine.py:684), the one owning reader, with a TC-411 case -> @builder
- [MINOR] project-trajectory/scripts/trajectory_arch.py:1080 -> B1: the new tests-root prefix repeats in intent `kitlib.spine.module_tests` (project-trajectory/scripts/kitlib/spine.py:726) and diverges from it, since `module_tests` returns [] for roots `./qa/tests` and `.` where this helper reads them correctly (PROCESS.md §3, "Consolidate, don't duplicate") -> extract one tests-root prefix into `kitlib.spine`, use it at both sites, and have it carry the `.` handling this lane built -> @builder
- [MINOR] docs/test/test-cases.toml:3530 -> K1: TC-333's `expected` still says the shipped planner template "names no skill or repository row", while the test its evidence now names asserts the template does name `architecture-decomposition/SKILL.md`, so D-005's "traced-only" reading leaves an approved row stating the inverse of its own evidence; the staleness predates the lane (489678a52) and nothing at runtime reads the cell -> amend the clause through the checkpoint sitting, as D-009 routes it -> @coordinator
- [MINOR] docs/requirements/low-level-requirements.toml:1564 -> K1, for clarity: approved LLR-365 says "A test repeating its module's test case is no finding", but with a file-only part a repeating test now reads `tag without evidence` under strict (driven: rc 1), which only project-trajectory/RESYNC_PACK.md:10518 states -> amend the sentence to scope it to the declaration read, or point it at LLR-366, at the checkpoint sitting -> @coordinator
- [MINOR] project-trajectory/skills/spine-authoring/references/in-lane.md:25 -> B1: the shipped intent note makes a state no instrument clears, since an `Automated = Yes` TC whose cell still reads `(owed by the tests commit)` with no test and no tag passes the equality check (driven on a Drafted row: rc 0) and trace's cites-no-Evidence rule (the live Approved TC-165 and TC-166 note cells pass at integrity=0), and the "Close the edges before the sitting" list (in-lane.md:42) names no such item, leaving only the sitting's reading -> add one edge to that list: no `(owed by the tests commit)` note remains at the sitting; a note-only `Automated = Yes` cell cannot be made unrepresentable here because the owner-ruled TC-165 and TC-166 form is that same shape -> @coordinator
- [MINOR] project-trajectory/RESYNC_PACK.md:10533 -> B1, for clarity: the entry says one `scope: this-repo` skill changed, but the range changes two, `coordinator-cycle` and `byte-budget-guard` (its stamps) -> name both, as the plural form at RESYNC_PACK.md:10273 does -> @coordinator

VERDICT: APPROVE findings=6
