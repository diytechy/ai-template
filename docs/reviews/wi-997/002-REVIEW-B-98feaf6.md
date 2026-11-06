Reviewed: 98feaf6fb1b94c32c7ad67b40bcaf13b733cd14c

### REVIEW-B: WI-997, full lane fb2bb4e5a..98feaf6fb, round 1

Verified. Failure classes hunted first: a fail-open comparison, silent change to test behaviour inside the seed, and a stale or false cell in the repoints.

The seed holds. Over all 217 changed `.py` test files, my own docstring-stripped AST compare of base against tip finds 215 identical and 2 different: `tests/test_trajectory_arch.py` (the new tests) and `tests/conftest.py` (one tag inside the demo test string). Every docstring the seed commit changed differs from base only by tag lines (0 non-tag changes). Identical ASTs also stand in for the collected count, which I did not re-collect. `check_complexity` is unchanged at 183 rows, and the stamps are right: PROCESS.md 99,216 bytes, the skill 4,537, mirrors identical.

The stale parts hold. My walk of all 366 rows through `evidence_items` finds 0 nodes naming no def, 0 parts that are not paths, and only TC-165 and TC-166 with no part. The 8 parts outside `tests/` are the expected records. WI-1000 and WI-999 exist, queued, and cite their TCs; no test tags either TC. D-006's 19-to-4 reading is confirmed.

The check holds. Nine mutants of `_tag_evidence_findings` and `tc_tag_findings` (keep `[case]`, drop `refused`, naive prefix, no `is_dir`, file part matching any tag, Approved only, no second arm, `;` split, class dropped) each failed at least one new test, so the tests would catch those wrong implementations. They drive the real `check_trajectory.py`. A further 16 scenarios run through that CLI behaved as specified, save the two findings below that they confirm. A backslash scenario was my own probe's error (`\t` in TOML) and is discounted. No shared reader is duplicated: `evidence_items` is reused and the `[case]` reduction occurs once.

Done-when map:
- Tags: AST compare above, `seed-evidence.txt`, strict check. Covered, except the log statement.
- Stale parts: covered, but see the TC-333 finding.
- Two moved cases: D-007 and the cells. Covered.
- Check: `tc_tag_findings`, 0 findings on the tree. Covered.
- Regressions: `test_evidence_without_a_tag_is_named`, `test_a_tag_without_evidence_is_named`, `test_a_parametrized_part_matches_its_tests_tag`, `test_a_part_outside_the_tests_root_is_ignored`, `test_a_file_only_part_matches_a_module_tag_and_not_a_tests_tag`, `test_a_draft_tc_is_judged`. Covered.
- Lane's routine: text present at recipes.md:1087, but see the first finding.
- Sizes: covered.
- Spine: LLR-366 and TC-410..412 present, Drafted. The in-lane adjudication and the registry anchor are not at this tip; the plan schedules them at P8, after the rounds, so they are owed, not findings.
- RESYNC: entry present, `check_resync` OK.
- Retirement: header comment above the helper. Covered.
- The log statement is likewise owed at P9.

Relationship decisions (the semantic reading; reference checks only support these):
- LLR-366 added under SR-157: counterpart SR-157 retained, because its acceptance puts a rule added at a declaration site in scope by default.
- IF-263 `data` widened: counterpart is the requestor `check_trajectory` and the module's Contract body. The Contract body carries the change in this diff; the requestor needs none, since it calls the same function. TC-410 cites IF-263.
- LLR-365 retained except one sentence (finding 4).
- TC-079 and TC-194 evidence repointed: their method and expected retained, because the moved tests verify the same clauses (TC-194's three names read in `test_facade_reexports_pending_compatibility_names`).
- TC-333 evidence repointed: its expected cannot be retained (finding 2).
- TC-165 and TC-166 evidence: method, expected and automated retained under OI-127 as ruled.
- Decomposition: one LLR, because it states one equality decision. TC-410 verifies the finding kinds, severity and rung. TC-411 verifies how a part reduces and binds. TC-412 verifies what lies outside the rule and vacuity. Each has its own verification purpose, and further splitting would add no independent value, since all three drive one function through one surface.

Coverage-extension notes (fail closed, so no finding): a class part `path::TestC`, a directory part `tests/unit`, and a document part under `tests = .` each read `evidence without a tag` with no tag form. The RESYNC entry's "no tag form" list could name them.

Disclosure: `trace.py` rewrote the git-ignored `docs/test/report.md` in the lane. `git status --short` stays empty and HEAD is unchanged. All probes, the tree copy and the mutants live under the r1B directory.

Commands:
- `git rev-parse HEAD`: 98feaf6fb1b94c32c7ad67b40bcaf13b733cd14c
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp <r1B>/wi-997 tests/test_trajectory_arch.py tests/test_trajectory.py tests/test_evidence_join.py`: 209 passed, 20 warnings in 40.31s
- `python project-trajectory/scripts/check_trajectory.py --strict`: check_trajectory: clean (998 work item(s), 885 done (89%), 34 cancelled, graph acyclic). exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity`: Traceability: SN=31 SR=138 LLR=332 TC=366 orphans=0 integrity=0 ... budget-findings=0 component-findings=0 interface-findings=0
- `python project-trajectory/scripts/trace.py --strict`: same summary line
- `python scripts/check_resync.py`: check_resync: OK, 3 shipped path(s) changed; entry anchored at fb2bb4e5aa87117e3caa53fff296e6d4c14161eb
- `python project-trajectory/scripts/check_complexity.py`: OK - 183 row(s) over 15, unchanged from baseline
- `<r1B>/probe/astcmp.py`: same 215 diff 2
- `<r1B>/probe/docs.py`: non-tag changes 0
- `<r1B>/probe/stale.py`: stale [], nonpath [], empty TC-165 and TC-166
- `<r1B>/probe/mutate.py`: baseline 16 passed; all 9 mutants red
- `<r1B>/probe/scen.py`: 16 scenarios through the real CLI

Findings:

- [MAJOR] project-trajectory/skills/coordinator-cycle/references/recipes.md:1087 -> The new routine contradicts the procedure it sits beside, so a lane cannot follow both. The recipe says a test's tag and its `evidence` part go in one commit, but `project-trajectory/skills/spine-authoring/references/in-lane.md:19` says TC rows come before the build and their `Evidence` names "the tests and symbols the build will create", and the coordinator-cycle SKILL's Intent step commits those rows first. A Drafted TC is judged, so an intent commit made that way reads one strict `evidence without a tag` per part at the bar (`test_a_draft_tc_is_judged` drives it). This lane did exactly that: 26133ae71 names the 13 tests with 0 tags, and the tags arrive at 8323e5e13. Every later lane adding a TC reaches it, and `spine-authoring` is `scope: kit`, so adopters inherit the instruction without this recipe -> state the one rule in one home and link it: amend in-lane.md and the Intent step so an intent row's `Evidence` holds a parenthetical note (the form D-007 confirmed passes) until the commit that writes the test and its tag, or, if intent cells keep naming tests, change the recipe and say which commit may be red. Add a RESYNC line for the shipped skill text -> @coordinator
- [MAJOR] docs/test/test-cases.toml:3530 -> (K1) The lane repointed TC-333's `evidence` at `test_the_shipped_planner_template_names_the_architecture_skill_by_its_agent_paths_and_no_row_of_this_repo`, but TC-333's Approved `expected` still says the planner template "names no skill or repository row". That test asserts the opposite (`"architecture-decomposition/SKILL.md" in raw`, tests/test_plan_pass.py:264), and `project-trajectory/prompts/plan-single.template.md:47` does name the skill. D-005 calls this traced-only because the old test NAME appears in no method or expected, which checks the name, not the case. The clause was already false at base, but this edit binds it to a test proving its inverse. Done-when "The stale parts" says that where no test verifies the case the row reports it as a finding about the TC, not a cell edit -> correct D-005 and report the clause; amend TC-333's `expected` through its authority to state what the template names (the architecture skill by its agent paths, no repository row). The row-text change owes a sitting, so it is not traced-only -> @coordinator
- [MINOR] project-trajectory/scripts/trajectory_arch.py:1087 -> A cell spelled `./tests/test_t.py::test_a` names a path under the tests root, but the raw `startswith(prefix)` reads it as outside the rule, so with no tag the check is silent. Driven: strict exit 0 with no finding, while the same test tagged reads `tag without evidence`. The test pins `./` on the declared root, not on the cell. No live cell uses this spelling, so it is rare, but it fails open on an agent-written cell -> normalize a leading `./` once in `kitlib.spine.evidence_items`, the single reader, beside its existing backslash normalization, so every consumer reads one spelling, and add a `./` cell to `test_a_part_outside_the_tests_root_is_ignored` -> @builder
- [MINOR] docs/requirements/low-level-requirements.toml:1571 -> (K1, for clarity) Approved LLR-365 says "A test repeating its module's test case is no finding", and LLR-366 now makes that same repeat a finding when the cell names only the file. Driven: a module tag and a test tag for TC-001 with a file-only cell gives `tag without evidence: tests/test_t.py::test_a`, strict exit 1, and naming both parts is clean. The behaviour matches the spec; the wording overlaps, and row 1's RESYNC entry gave adopters the same permission, so one who repeated a tag gets a finding the new entry does not list -> add to Drafted LLR-366 that a repeated declaration is still a declaration its cell must name, leave LLR-365's approved text alone, and add that case to the RESYNC entry's list -> @coordinator

VERDICT: CHANGES-REQUESTED findings=4
