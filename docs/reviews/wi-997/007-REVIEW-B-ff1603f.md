Reviewed: ff1603f4e07bc8b7c687953b32046d5494486d65

### REVIEW (independent, convergence stance) - WI-997 full lane - 2026-11-06

Verified: The worst classes this change admits are a silent fail-open of the equality check (a part or tag dropped from the comparison), a non-tag code change hidden among about 2100 tag edits, and an approved row changed beyond its grant. I hunted those first. The checkout is the reviewed commit, and the lane worktree is unchanged after every run. The declared tests pass and `check_trajectory.py --strict` is clean with 0 equality findings. On a copy of the real tree, removing a real tag reads `TC-410: evidence without a tag: ...` with exit 1, and removing a real part reads `TC-410: tag without evidence: ...` with exit 1; a comma separator also reds. Fourteen mutants of `_tag_evidence_findings` and `tc_tag_findings` each fail a named test: no `[case]` reduction, no refused filter, no `is_dir` guard, no prefix filter, a test part falling back to the file tag, Approved rows only, no tag-without-evidence arm, a raw prefix, a module tag covering tests, the class dropped from a node, unsorted output, a file part covering tags beneath it, a whole-repository read, and judged placeholder rows. The three lane-added witness tests (`test_a_test_part_does_not_match_a_module_tag`, `test_a_declaration_outside_the_tests_root_is_not_read`, `test_a_placeholder_row_is_outside_the_equality_rule`) and `test_a_test_repeating_its_modules_case_needs_its_own_part` each fail on their stated wrong implementation. `test_a_tests_evidence_arrives_with_its_tag_stated_at_one_home` fails on the four documents as they stood at `68100ad87^` and passes at the tip. My own stripped-AST comparison over the whole range (not only the seed commit) covers 217 changed test files: only `tests/conftest.py` (a tag inside a scaffold fixture string), `tests/test_prompts.py` (the one-home test and its moved pins) and `tests/test_trajectory_arch.py` (the equality tests) differ, with no line-ending drift. No live TC holds a stale node or a non-path part; only TC-165 and TC-166 have no part.

Done-when coverage:
- The tags: `docs/plans/WI-997/seed-evidence.txt` (216 files, 0 AST differences, 7720 ids before and after) and my range-wide AST pass. A sample of tags read correct. The clause "stated in the log" is outside this reading scope: no `docs/log.d` row for WI-997 exists yet, and that record is close-out work.
- The stale parts: my probe finds none. The four repoints are the same tests, moved or renamed; `test_facade_reexports_pending_compatibility_names` loops the three former names. The record in the lane's decisions was not read, by stance.
- The two moved cases: the cells read `(owed by WI-1000)` and `(owed by WI-999)`, both rows exist and cite the TC, and neither file takes a tag. Covered by `test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding`.
- The check: TC-410, TC-411, TC-412 and the strict run. Regressions: each named arm is covered and mutant-confirmed.
- The lane's own routine: `references/recipes.md`, `references/in-lane.md`, pinned by the one-home test.
- Sizes: `check_complexity` unchanged from baseline; the PROCESS.md stamp 99,216 and the skill stamp 4,537 match the files.
- Spine: LLR-366 and TC-410..412 exist with every LLR arm mapped to a test; no code named in the row text. The sitting's record was not read, by stance.
- RESYNC entry: present, with the two findings, the retirement, the seed rule and the forced migration; `EXAMPLE.md` is unscaffolded, so its absence from the file list is right.
- The retirement: comment at `project-trajectory/scripts/trajectory_arch.py:1065`.
- Coverage bound and review bar: met as above.

Interface and requirement record:
- Changed side: IF-263 `data`, owner `scripts/trajectory_arch`. Counterpart: requestor `scripts/check_trajectory`, LLR-365, LLR-366, SR-157. Decision: carried on the module contract line, the check header, LLR-366 and TC-410, which cites IF-263. The version stays v1 because the output is still finding strings. The call site is unchanged. SR-157 is retained unchanged: its acceptance ranges over the rule inventory the checkers publish, so a new rule needs no parent amendment. `_kitspine` was already imported, so no new seam is owed.
- Change intake (PROCESS.md §5): no workaround preserves an unsuitable LLR. LLR-365's repeat clause stays true of the declaration reading and gains a scope sentence; LLR-366 holds the separate decision and retires alone when the evidence column is generated, while LLR-365 outlives it.
- Decomposition: LLR-366's independent decision is the equality of two homes. Splitting it per finding arm adds no independent value, because both arms are one set difference with one reader, one severity and one retirement. TC-410 verifies naming, severity and rung; TC-411 the binding of a part to a declaration; TC-412 scope and vacuity. Each purpose is distinct.

Notes, no finding:
- Coverage extension: a whole-class part (`path::TestC`) and a method in a class not named `Test*` fail closed (a misplaced tag and a named difference), but the RESYNC list of parts with no tag form omits them. A comma-separated cell also fails closed.
- Dismissed under the Review threat model: a `./tests/x.py` part with no tag falls outside the prefix and reads clean. None of the 366 cells uses it, no template or prompt writes it, and with a tag it reads `tag without evidence`.
- `check_doc_refs.py --strict` exits 1 on 193 dangling references, none naming WI-997, LLR-366 or TC-410..412; no base run was compared.

Commands:
- `git rev-parse HEAD` -> ff1603f4e07bc8b7c687953b32046d5494486d65
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gB/wi-997 tests/test_trajectory_arch.py tests/test_trajectory.py tests/test_evidence_join.py tests/test_prompts.py` -> 303 passed, 20 warnings in 49.20s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> clean (998 work item(s), 885 done (89%), 34 cancelled, graph acyclic), exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=138 LLR=332 TC=366 orphans=0 integrity=0 ... interface-findings=0
- `python project-trajectory/scripts/trace.py --strict` -> same summary, exit 0
- `python project-trajectory/scripts/check_complexity.py` -> OK - 183 row(s) over 15, unchanged from baseline
- `python project-trajectory/scripts/check_doc_refs.py --strict` -> 193 dangling reference(s), exit 1 (see notes)
- Probes in `.../gB/probe`: `p1.py` (range AST, stale nodes), `mut.py` `mut6.py` `pre.py` (14 mutants, pre-fix docs), `live.py` (real-tree mutation), all on a scratch export since removed

Findings:
- [MINOR] docs/test/test-cases.toml:3530 -> K3: TC-333 is Approved and the spec grants only a traced-only repoint, yet its `expected` cell lost "and names no skill or repository row" whole; only "no skill" was false, and `test_the_shipped_planner_template_names_the_architecture_skill_by_its_agent_paths_and_no_row_of_this_repo` still asserts no repository row, so a true, tested, approved arm left the cell -> delete only the false words, so the clause reads "is in the catalogue and names no repository row" -> @coordinator
- [MINOR] project-trajectory/scripts/trajectory_arch.py:1080 -> PROCESS.md §3 consolidate: this line is a second spelling of "a path under the declared tests root" beside `module_tests` at project-trajectory/scripts/kitlib/spine.py:726, and the two disagree: driven, `module_tests` returns nothing for a root of `.` or `./qa/tests`, where this check holds the parts -> extract one prefix helper in `kitlib.spine` and call it from both -> @coordinator

VERDICT: CHANGES-REQUESTED findings=2
