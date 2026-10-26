Reviewed: f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110

## WI-979 — REVIEW-B (independent, full lane deebc18f6..f0a05a1b4)

**Verified.** `git rev-parse HEAD` printed f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110 in the lane worktree, and the worktree stayed clean through the review. I checked these failure classes first, worst first: (1) silent wrong content in an adopter scaffold, meaning a broken link, a rubric citing a record the adopter cannot read, or a pointer to a skill path its agent lacks; (2) fail-open or over-reach in the adjudicator brief, meaning the new spine-questions §4 reaching SN or SR sittings, or forcing a RETURN at every LLR sitting; (3) drift between the kit template and this repo's copy.

What I found right:
- The rubric template and `docs/rubrics/architecture-decomposition.md` are byte-identical (checked with `diff`), and the copy is pinned in BOILERPLATE_COPIES.
- The MAPPING row seeds the rubric once, with SR-186 as its purpose reference.
- I bootstrapped a real scaffold (`bootstrap.py --dest <r2-979-B>/scaffold --agents codex`). It holds the rubric and `.agents/skills/architecture-decomposition/SKILL.md`, and the scaffold's own `check_docs` reported 0 broken links.
- I removed the README's one-sentence link in that scaffold, and check_docs then reported the rubric as an orphan. So the RESYNC entry's claim that an adopter must add the link is true, and the scaffold copy was restored afterwards.
- The rubric's quoted references all resolve in an adopter's tree, and it cites no id of this repo's records:
  - `process.md §3 "Decompose, don't paraphrase"` and `§6 "Review threat model"`;
  - `process-options.md "(d2) Record the stopping boundary"`;
  - `prompts/spine-questions.md §3 "Record the stopping boundary"`.
- The five clarifications sit in the anchors that ask them:
  - ownership model in A6;
  - invariants, enforceability, migration and the separately counted crossings with the unknown remainder in A7;
  - *not supplied* and *not assessable* in A4, plus *insufficient evidence for approval* in A7.
- No B pattern was added; the rubric still has B1 to B4.
- A8 separates obligation descent (tests 1 to 4) from component descent (no information-hiding cut pays its way after A1/A4/A7). Its stopping record names the candidate children, the evidence, the remaining uncertainty and the revisit trigger.
- spine-questions §4 is appended with `<!-- tiers: LLR -->`, and sections 0 to 3 keep their numbers. `tier_questions({"SR"})` excludes it and `tier_questions({"LLR"})` carries it. Its applies-when is stated in the line itself.
- I checked the round-1 fixes against their pre-fix patches, read with `git log -p --format=%h`. The new pins fail on each pre-fix text:
  - cffd9f275's §4 line had no applies-when, and `test_the_arch_section_points_at_the_rubric_and_restates_nothing` asserts that clause;
  - its skill said "two descent tests", which `test_architecture_decomposition_skill_walks_four_steps_and_cites_the_rubric` refuses;
  - its plan-single line sat before the delta bullets, and the ordering assertions refuse that;
  - its bootstrap docstring lacked the destination, and `test_the_scaffold_layout_an_adopter_reads_names_every_seeded_rubric` asserts it.
- The plan-single line names every `bootstrap.AGENTS` skills_dir. `DELTA_QUESTION`, the S5 wording and the plan rubric's delta paragraph are unchanged; the paragraph was compared against deebc18f6.

**Requirement and interface counterparts.** This lane adds members on two seams and changes neither seam's form:
- IF-035, the skill directory: its `data` form is SKILL.md frontmatter plus co-located files. The new skill carries every listed field, so the counterpart is retained.
- IF-262, the scaffold mapping: its form is a source, a destination and an optional requirement reference. The new row uses that form, so the counterpart is retained.

SR-186, SR-165, SR-146 and SR-112 are not amended, and none needs to be:
- the rubric's A8 is the judgement behind SR-186's stopping record;
- the skill's step 4 records the stopping decision in the existing scoped record, or in SR-165's component-registry partition record, and adds no field;
- the prompt, fragment and skill copies keep the forms SR-146 and SR-112 constrain.

No SN, SR, LLR or TC row is added or changed, so no registry sweep or decomposition-child record is owed. kit-change-review K1 to K3 hold: no requirement cell changed, no Implements tag was added, and no Status flipped.

**Done-when map.**
- Rubric, MAPPING row, byte-identical pinned copy and scaffold destination: covered by test_architecture_decomposition_rubric (manifest pin), test_dogfood_sync and test_bootstrap `test_scaffold_contains_expected_files`.
- The five clarifications, each in its anchor, with no new B: covered by `test_each_clarification_is_asked_in_its_anchor` and `test_no_failure_pattern_is_added_for_them`.
- A8's two descent rules and its record fields: covered by `test_a8_separates_requirement_descent_from_component_descent`.
- References resolve in an adopter's tree, and check_docs is clean: covered by `test_references_read_in_an_adopters_repo`, and by my scaffold check_docs run.
- The skill: four steps, scope kit, cites the anchors, points to deep-module-design, description triggers, INDEX.csv: covered by test_skills_index (the new test) and by the generated INDEX.
- Copies materialized, and `--check-agents` clean: covered by the run below.
- spine-questions §4: covered by test_prompts (new test) and by test_adjudicate_brief's heads.
- plan-decomposition G5: covered by `test_the_plan_rubric_judges_the_delta_line_against_the_shared_rubric`.
- scope-critique S5 pointer: covered by test_review_brief.
- plan-single line, its path, the DELTA_QUESTION pin and CATALOG: covered by test_plan_pass.
- The RESYNC entry: checked by reading it. It covers all five required points, and its orphan claim was checked in the scaffold.
- trace and check_trajectory strict: both clean (below).
- `run.cmd smoke`: not run by this reviewer, because the round facts forbid it. The declared targeted set stands in for it.

**Commands.**
- `git rev-parse HEAD` -> f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp <r2-979-B>/wi-979 tests/test_architecture_decomposition_rubric.py tests/test_dogfood_sync.py tests/test_bootstrap.py tests/test_skills_index.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_review_brief.py tests/test_plan_pass.py tests/test_profile.py` -> `367 passed, 2 skipped in 425.12s (0:07:05)`. One skip is environment-gated (posix-shell).
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (976 work item(s), 864 done (89%), 34 cancelled, graph acyclic).` (exit 0)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 ... interface-findings=0 ...` (exit 0)
- `python project-trajectory/scripts/gen_skills_index.py --check-agents` -> `gen_skills_index: OK - 22 per-agent skill copy(ies) match source.`
- `python project-trajectory/scripts/check_docs.py` -> `check_docs: OK - 3175 doc(s), 3760 intra-repo link(s), 0 broken (1 orphan warning(s)).`
- `python project-trajectory/scripts/bootstrap.py --dest <r2-979-B>/scaffold --agents codex`, then the scaffold's `scripts/check_docs.py` -> `check_docs: OK - 22 doc(s), 89 intra-repo link(s), 0 broken (1 orphan warning(s)).` The one orphan is `docs/test/report.md`, which is not from this lane.
- The same scaffold with the README link removed -> `WARN - orphan doc (no path from an entry root): docs/rubrics/architecture-decomposition.md`. The scaffold file was then restored.

**Findings.**

- [MINOR] project-trajectory/skills/architecture-decomposition/SKILL.md:20 -> for clarity: "Each step's result answers one clause of the delta question" is not literally true. Step 2's domain-and-interface result answers two clauses ("add a value" and "cross a new boundary"), and step 4's descent result answers none, so a planner mapping step to clause one-to-one misplaces the boundary clause. -> reword it to say "the steps' results answer the delta question's four clauses", keeping the clause-by-clause mapping that follows -> @owner
- [MINOR] project-trajectory/rubrics/architecture-decomposition.template.md:175 -> for clarity: A7's *insufficient evidence for approval* outcome is never mapped onto the Verdict section's machine line (line 239 onward). A4 meanwhile says an unanswerable question "is never read as a defect", so a critic cannot tell whether that outcome is an APPROVE, a CHANGES-REQUESTED with a finding, or neither. (K1, intent stated clearly.) -> add one sentence to the Verdict section naming the machine line, and the finding severity if any, that *insufficient evidence for approval* produces (for example: one MAJOR line naming the missing evidence under A7) -> @owner
- [MINOR] tests/test_skills_index.py:125 -> the same `_RECORD_ID` pattern and the four A8 test labels are declared twice: in tests/test_skills_index.py:125-132, and in tests/test_architecture_decomposition_rubric.py:32 and :93. When one copy is updated (a new record prefix, a renamed A8 test), the other silently stops pinning what it claims (PROCESS.md §3, "Consolidate, don't duplicate"). -> have test_skills_index read the labels from the rubric module's constants (or from a shared conftest helper) instead of redeclaring them -> @owner

VERDICT: APPROVE findings=3
