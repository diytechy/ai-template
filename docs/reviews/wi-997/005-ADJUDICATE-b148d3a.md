Adjudicated: b148d3aef

## amendment

Judged on the cells as shown: TC-333 `Expected` (JUDGED-TEXT sha256:7146d23f859a7c0a) and LLR-365 `Detail` (JUDGED-TEXT sha256:3515f325e8b419c3), against the ef2d68610 anchor. The rung is released. Before deciding whether to bless, I read both rows against the build at this tip: `check_trajectory.py --strict` is clean, `trace.py --strict-integrity` is clean, and every test the new clauses lean on is defined once.

- [MEANING+BLESS] TC-333 Expected -> before: the shipped planner template "is in the catalogue and names no skill or repository row", which a test has to check -> after: the shipped planner template "is in the catalogue", and every other clause is unchanged -> not the same: a check is removed. A template that names a repository row fails the old text and passes the new one. I would bless the new text. The removed limb was stated by no row of TC-333's chain (SR-146, SR-154, SR-235; arms-map gaps 6 and 7), and a TC states only what its rows state. Its "names no skill" half was also false of the build: the template names the architecture skill, as the still-cited node `test_the_shipped_planner_template_names_the_architecture_skill_by_its_agent_paths_and_no_row_of_this_repo` asserts. Leaving that node in the Evidence cell pins a little more than the cell now claims, which is harmless. It is the same allowance the WI-994 sittings made. The TC names no carrier and keeps every other clause verbatim.
- [MEANING+BLESS] LLR-365 Detail -> before: "A test repeating its module's test case is no finding", unqualified, about test-file declarations -> after: the same sentence, followed by "That reading judges the declarations alone: their equality with the Evidence cell is a separate rule" -> not the same: the old text says a repeat raises no finding at all. The new text narrows that to this reading and admits that the equality rule may report a repeat (LLR-366: the repeating test's cell must name that test too, or it reads "tag without evidence"). A build that raises a finding for a repeat fails the old text and can pass the new one. I would bless it. It is what makes LLR-365 and LLR-366 agree instead of contradict each other on the same input. It names a registry cell, which the LLR tier may name, and no carrier. TC-411 now verifies LLR-365 and states the clause, and `test_a_test_repeating_its_modules_case_needs_its_own_part` holds both phases (arms-map gap 5, closed). Every approved sentence stays byte-exact.

The rung is released and no row is held. The two rows are in different registries and both are blessed, so no CLARITY row waits on either. The later act re-attests TC-333 and LLR-365.

VERDICT: MEANING rows=2

## first-approval

Read at b148d3aef against SR-157's chain. LLR-365's amended text was ruled in the section above. I read the equality rule as built (`trajectory_arch._tag_evidence_findings` and `tc_tag_findings`) and found it agrees with LLR-366 sentence by sentence:
- live rows include Drafted rows and exclude `-000`;
- a part is its path, or its path and node with the `[case]` dropped and the class kept;
- the tests-root prefix gives `.` every path;
- parts in a file refused as unreadable are skipped;
- with no tests root, the equality half is skipped and the check is vacuous.

All 17 nodes cited by TC-410 to TC-412 exist, and their evidence module is slow, so the three `Full` tiers agree. The arms map's seven gaps are closed at this tip:
- gaps 1 to 3 by `test_a_test_part_does_not_match_a_module_tag`, `test_a_declaration_outside_the_tests_root_is_not_read` and `test_a_placeholder_row_is_outside_the_equality_rule`, each with its clause;
- gap 4 by TC-410's expected naming both kinds;
- gap 5 by TC-411 verifying LLR-365;
- gaps 6 and 7 by TC-333's cut, ruled above.

The repository's own strict check is clean with the rule armed at DevStg-Impl.

Stopping boundary. LLR-366 adds one decision LLR-365 does not make: that the test-file declarations and the Evidence cell, two homes of one fact, are held equal. LLR-365 is about reading a declaration; LLR-366 is about comparing two finished readings. Splitting LLR-366 by finding kind would repeat its part definition twice. The three TCs split by verification purpose: TC-410 covers attribution, severity and the rung; TC-411 covers the part-matching semantics; TC-412 covers the scope and vacuity bounds. None repeats another, and splitting further would only copy parametrize ids into rows.

- [APPROVE] LLR-366 -> for each live test case, Drafted included, the declarations under the declared tests root equal the parts of its Evidence cell. A part is its file, or its file and test with the class kept and the parametrization dropped. A file part binds only to a file-level declaration and a test part only to that test's declaration. A repeat is still a declaration. Parts outside the root, a note and an unreadable file's parts add nothing. Each difference is "evidence without a tag" or "tag without evidence", naming the case and node. Findings warn plain and error strict, gating from DevStg-Impl, and absent inputs are vacuous -> upward, a disagreement between the two homes is a broken join that SR-157 asks to be reported with its at-fault row; sideways, it reads through LLR-260's cell reading and LLR-365's declaration reading without restating either (its rationale says so); downward, TC-410 to TC-412 reach every arm -> ready: every sentence is observable and true of the build, the row names only registry cells and the `.` root, carries no `shall` and no Hat-Refs, and its phase is the current one.
- [APPROVE] TC-410 -> each "evidence without a tag" and "tag without evidence" difference names its case and node, warns plain and errors strict; a Drafted case is judged; a new project warns below the implementation rung and fails at it -> four existing nodes drive exactly these, through the check, and IF-263 is the call they cross -> ready.
- [APPROVE] TC-411 -> parametrized, file-only, class-method, whitespace-separated and non-Python parts are matched as LLR-366 defines; a test part does not match a module declaration; a repeating test reads "tag without evidence" with a file-only cell and is clean with both parts -> seven existing nodes, one per clause, and its LLR-365 citation verifies the separate-rule sentence -> ready.
- [APPROVE] TC-412 -> parts outside the root, a `.` root, a declaration outside the root, a placeholder row, absent inputs, an unreadable file beside a readable one, and a note-only cell each behave as LLR-366 bounds them -> six existing nodes, one per clause -> ready.

OUTCOME: APPROVE rows=4

SITTING: JUDGED kinds=amendment;first-approval
