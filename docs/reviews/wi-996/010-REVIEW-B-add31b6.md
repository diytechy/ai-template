Reviewed: add31b6be27158e4d0269762340bbfafc65b4ad0

Full-lane review of WI-996 (f24a68ca2..add31b6be), convergence stance, rubric docs/rubrics/kit-change-review.md. I read no earlier verdict, decisions record, plan critique or lane commit message. Pre-fix code came from `git log -p --format=%h` patches only.

**Verified.** I hunted these failure classes first, worst first: (1) fail-open, where a marked (red) test lands on trunk or a mark is removed with no red-before; (2) a refusal that moves the branch or the index; (3) false refusals on supported routes.

- **Landing arm.** `kitlib/red_mark.landing_refusal` runs in `integrate.refresh` after `add -A` on the merged, regenerated staged tree and before `_attest_commit`. It runs for both the `landing` and `no-bar` bars, and `undo` resets to the work tip. `integrate_one` and `dispatch._refresh_or_quarantine` both reach it through `refresh`.
- **Attest arm.** `_attest_preflight` reads `[bars] review` and `[bars] red_mark` from one parse of the lane checkout, and only after the lane checkout has been confirmed equal to the index. It then runs `attest_refusal` on the derived set before any bar.
  - The reference is the newest verified `review` record in `_lane_base..branch`, else `base^{tree}` with no record.
  - Removal requires digest equality with the record and that T names P. Digest equality means set equality, so the reference's set named P too.
  - Files gone from the staged tree are not judged, as the table says.
  - Unread range or tree refuses.
- **Real-code probes.**
  - The recipe §3 hand-landing command, run verbatim on this worktree, prints "no red mark staged" (exit 0).
  - A `tree_counts` scan of HEAD finds 0 marked files under both `tests/` (284 test files) and the whole tree (466 test-type files). So neither this repo nor a `tests = .` adopter carrying the kit is refused by its own landing arm.
- **Regression test checked against pre-fix code.** I extracted HEAD to scratch and swapped in the pre-fix `red_mark.py` (8c3c7a7c7^). `test_a_tests_root_of_dot_counts_only_the_files_the_review_set_reads` then FAILS: `landing_refusal` names README.md, docs/stack.ini, notes.txt and pkg/__pycache__/test_cached.py. It passes at HEAD.
- **add31b6be fix (text only).** The recipes §3 step exists, sits between the squash and the commit bar, and is pinned by `tests/test_prompts.py::test_the_hand_landing_checks_the_staged_squash_for_a_red_mark`.
- **Consolidation is sound.** These shared pieces each now have one home, with no new duplicate:
  - `read_blobs`, extracted from `write_blobs`;
  - `normal_test_paths`, extracted from `tests_digest`;
  - `declared_roots`, extracted from `review_set._roots`;
  - `is_test_file`/`hidden_rel`/`BACKLINK_EXTS`, moved from `gen_arch_map` and shared by the tag reader;
  - the `[bars]` parse, where `_review_bar_command` was deleted.
- **Housekeeping.** The skill copies are byte-identical across `project-trajectory/`, `.claude/` and `.agents/`. The byte-budget rows are restamped to the measured sizes (PROCESS.md 100,417; byte-budget-guard SKILL 4,548). The ratchet entries were re-stamped downward. `check_test_first.py` is untouched.

**Requirement/interface counterparts (the reviewer's semantic decision).**

- **SR-156 acceptance (Approved, amended; changed side) against its children LLR-207 (amended) and LLR-368 (new, Drafted), and TC-421..426.**
  - The amendment states the obligation the spec found missing ("Neither SR-156 nor LLR-207 states the red-before obligation"). An LLR-368 with no parent text would be untraced. The spec gave the shape to spine authoring at intent, so this sits within the K3 grant.
  - Status is not flipped. Under PROCESS.md §4 the drift waits for a re-attest against last_approved.
  - LLR-207 carries the corresponding change: code_symbol swaps `_review_bar_command` for `_lane_mark_refusal` and adds the two verdict readers, and the detail gains one sentence.
  - LLR-368 is retained as one row. Its declaration, count, table and landing arm are one decision (one module, one declared mark). Splitting would duplicate the declaration states across rows and add no independently failing obligation; TC-421..426 already split the verification.
- **IF-022.** Its contract text (`docs/stack.ini` header) changed. The row's `data` ("sections: ... bars ...") is retained, which is justified: the row names sections and the key lives in the contract text. `docs/interface-reference.md` is a `[generated]` trunk-lane artifact, so the trunk step regenerates it at landing and a work branch must not commit it.
- **IF-175 (verdict).** Retained. The new `last_review_record` and `normal_test_paths` fall under the existing "the review-attestation walk" and "the bar attestation grammar, verifier and tests digest". Its requestor list does not name `kitlib/red_mark`, but that list is already non-exhaustive (`agent_brief`, `plan_gate` and `session_keep` import verdict and are not listed). I retain it as it is.
- **IF-154, IF-173 and IF-080.** Retained. The verbs and exit-code contract are unchanged, and only their refusal sets grow. TC-424 and TC-425 verify them.
- **No IF row for the new kitlib module.** Consistent with the precedent of `config`, `git`, `spine` and `registry`.

**Done-when map.**
1. Template/stack.ini/IF-022 text: TC-421 tests (template value, no `@`, comment words, own declaration, contract). interface-reference is regenerated by the trunk step, as above.
2. One parse and five refusal states, for attest and refresh: `test_the_bar_and_the_mark_come_from_one_parse`, `test_attest_refuses_each_undeclared_state_before_the_bar` and `test_refresh_refuses_each_undeclared_state_before_the_bar`.
3. Attest table rows, each covered in tests/test_red_mark_lane.py:
   - added named/unnamed;
   - removal with a matching record, with no record, over another set, and with T not naming P;
   - a deleted file;
   - a plain commit then an empty attest (both the red and the green variant);
   - a wrapped mark;
   - unreadable range/reference/staged;
   - branch and index unchanged.
4. Refresh on both arms, plus a mark-free tree: `test_refresh_refuses_a_marked_tree_naming_each_file_and_count`, `test_a_tree_with_no_marks_refreshes_as_today`.
5. Fixtures declare `red_mark` (conftest, test_integrate_attest, test_integrate_station, and others). A grep of `tests/` finds no `[bars]` writer without it, and `RED_MARK` is built by concatenation. The decisions-record list is not checked (the convergence stance forbids reading docs/decisions).
6. Skill/recipes/PROCESS text: pinned in tests/test_prompts.py.
7. RESYNC entry: present, anchored `[since f24a68ca2]`, with the three steps and the files to overwrite.
8. Landing consequence in the decisions record: not checked (stance).
9. Coverage bound: TC-426 routes (merge-refresh, partial close, rebase, scaffold).
10. check_test_first unchanged: confirmed, not in the diff.

**Commands.**
- `git rev-parse HEAD` -> add31b6be27158e4d0269762340bbfafc65b4ad0
- The declared pytest set (36 files, `-n 2`, literal `--basetemp`) -> `1857 passed, 78 skipped in 2775.68s (0:46:15)`. The skips are environment-gated (posix-shell, 76) plus 2 others.
- `check_trajectory.py --strict` -> `check_trajectory: clean (999 work item(s), 889 done (89%), 34 cancelled, graph acyclic).` (exit 0)
- `trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=334 TC=380 orphans=0 integrity=0 ... interfaces=258 interface-findings=0 ...`. This rewrote the gitignored docs/test/report.md in the worktree, the only side effect.
- `pytest -rs tests/test_red_mark.py tests/test_red_mark_lane.py` -> `85 passed in 121.08s` (no skips).
- Extra affected files not in the declared set (test_held_status_git, test_id_landing, test_integrate_unload, test_loop_provenance, test_plan_gate, test_import_layers, test_module_size_ratchet, test_prompts, test_gen_arch_map, test_review_set, test_review_set_walk, test_agent_loop_review_gate, test_review_brief_git, test_trace_coherence, test_trajectory_arch, test_check_harness, test_complexity_ratchet) -> `685 passed, 4 skipped in 991.53s`.
- Pre-fix red check (scratch extract, pre-fix red_mark.py from 8c3c7a7c7^) -> `-k tests_root_of_dot`: `1 failed`, which is the expected red.
- The recipes §3 hand-landing command, verbatim -> `no red mark staged`, exit=0.

**Coverage-extension note (no severity).** A `[paths] tests` whose case differs from the tree's directory on a case-insensitive checkout would make the git pathspec match nothing. That is outside the declared set, and the review set reads the same prefix.

**Findings.**
- [MINOR] project-trajectory/scripts/kitlib/red_mark.py:147 -> `tree_counts` reads every blob under the tests root into memory through one `cat-file --batch` and only then drops non-test files. For an adopter with large fixture data under `tests/`, or a `tests = .` root (the whole repository), each `attest` reads it all twice (staged plus reference) and each refresh once. -> Filter the listed paths by `kspine.is_test_file` before the batch read: give `read_blobs` a path predicate, or list first and read only the test files. Same result, bounded memory (rubric B1: confirmed by reading `read_blobs`/`_listed_blobs`; efficiency) -> @owner
- [MINOR] docs/requirements/system-requirements.toml:742 -> for clarity: SR-156's new acceptance clause ends "an undeclared mark refuses both", and "both" has no clear antecedent. Read after "a mark is removed ... only against the lane's last review record", it can mean "refuses the landing and the removal", which understates the rule: an undeclared mark refuses every review attestation, not just a removal (K1). -> Write "an undeclared mark refuses every review attestation and every landing" -> @owner
- [MINOR] docs/test/test-cases.toml:4216 -> for clarity: TC-423's `expected` ("... and their stated refusals follow the low-level contract") and TC-426's (line 4249, "The stated ... outcomes hold") defer the outcome to other rows instead of stating what is observed, so the TC cell alone cannot be checked against its tests (K1). -> State the observed outcomes, for example: "an equal count passes unjudged; a raised count passes only when the set names the file; a lowered count on a present file passes only over a same-set review record naming it; each refusal names the file and condition" -> @owner

VERDICT: APPROVE findings=3
