Reviewed: f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110

Verified: Independently checked the scoped three-dot diff, WI-979's full spec and item-12 specref, its cited owner ruling and dry-run draft, PROCESS sections 3–6 and 8, and the cited registry rows. Prioritized silent wrong decomposition guidance, inappropriate returns at ordinary LLR amendments, approval without sufficient evidence, and overwriting adopter-owned content. No confirmed defect found. K1–K3 and B1 were assessed: no requirement cells, approval statuses, or realization back-links change. The five clarifications are in A4/A6/A7; A8 keeps the four obligation tests and supplies a distinct cost-based component stop. A7 withholds approval where evidence cannot settle a comparison. The scoped change introduces guidance, not the deferred architecture gates or audit action.

Requirement/interface decisions: SR-186 and SR-165 retain their acceptance and approval; the rubric adds judgment guidance without replacing the existing scoped stopping record or component derivation record. The changed IF-035 skill membership and IF-262 mapping membership retain their counterparts' existing directory and ordered mapping contracts: source/destination/reference entries and skill frontmatter retain their forms. SR-112's generated fan-out and SR-146's strict prompt filling/catalogue contracts also remain applicable and were exercised. No unsuitable LLR is preserved by a workaround, and no child requirement text needs re-attestation. Existing behavioral regression tests remain; the old no-skill assertion is intentionally replaced by the now-required skill pointer while retaining the delta-question pin.

Decomposition judgment: the rubric independently owns the judgment criteria; the skill owns the authoring procedure; the spine pointer routes LLR adjudication; the scope pointer routes pre-claim critique; G5 supplies a citable plan-review decision; and the planner pointer routes skill discovery. Each has a distinct decision or verification purpose. Further splitting any pointer adds no independent decision, splitting the skill duplicates its ordered procedure, and splitting the rubric separates criteria that must be compared together. The scaffold mapping, materialized copies and generated indexes carry these same artifacts rather than introduce competing definitions.

Done-when coverage (numbered in spec order):

1. Rubric/template, MAPPING, byte identity and scaffold destination: test_the_manifest_seeds_it_once_with_its_purpose, the dogfood boilerplate case, test_scaffold_contains_expected_files, and live bootstrap inspection.
2. Five clarifications and unchanged B1–B4: test_each_clarification_is_asked_in_its_anchor and test_no_failure_pattern_is_added_for_them, plus semantic reading of A4/A6/A7.
3. Two descent rules and record fields: test_a8_separates_requirement_descent_from_component_descent plus independent reading of the four tests and component comparison.
4. Adopter references: test_references_read_in_an_adopters_repo, scaffold/profile runs, and check_docs (zero broken links).
5. Four-step kit skill, existing homes, anchor citations and code-level pointer: test_architecture_decomposition_skill_walks_four_steps_and_cites_the_rubric and the existing frontmatter/description/index tests; independently read all four steps.
6. Materialized skills: --check-agents and actual scaffold byte comparisons.
7. LLR-only section 4, original numbering: test_the_arch_section_points_at_the_rubric_and_restates_nothing and actual first-approval/combined adjudicator brief tests.
8. G5 and unchanged delta paragraph: test_the_plan_rubric_judges_the_delta_line_against_the_shared_rubric and diff inspection.
9. S5 pointer and original question: extended test_the_scope_rubric_names_every_registry_the_critique_brief_renders.
10. Planner pointer, agent paths, delta pin and catalogue: rendered planner-brief test, agent-path/ordering test, all three live scaffold skill paths, and catalogue freshness.
11. One RESYNC entry: independently read its add-only seeding, agent selection, overwrite list, optional adopter rubric pointers and no-migration instructions; live rerun preserved edited adopter rubric.
12. Verification: ran the launcher's expressly substituted targeted pytest command and strict trajectory check, not the prohibited smoke/full suite; additionally ran the required integrity instrument. Literal smoke and trace --strict were not separately run; no claim is made that this review executed them.

The tests drive the affected shipped interfaces where executable: real bootstrap/scaffold flows, rendered planner/adjudicator briefs, catalogue generation, and skill fan-out. Text pins are supporting evidence, with semantic reading supplying the judgment they cannot mechanize. The three wording/placement regression tests each passed on current text and failed against cffd9f275 text via in-memory Path.read_text substitution. The scaffold-layout test passed currently and failed with cffd9f275's actual bootstrap docstring. The clarification and descent tests passed currently and rejected the original rubric draft. No reviewed worktree file was changed.

Commands:

- git rev-parse HEAD; git status --short: exact reviewed commit; clean checkout.
- git diff deebc18f6dc053423ee31dec37537583fcb58908...f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110 -- . with the brief's eight exclusions; targeted git diff, Get-Content, Select-String and rg reads: inspected product changes and requirement surface; no registry/status changes. Failed wildcard/console-encoding exploratory reads were replaced with targeted successful reads.
- git log -p --format=%h deebc18f6dc053423ee31dec37537583fcb58908..f0a05a1b4a5fb5e0fe48df22c02ce1adca05e110 -- the changed prompt, skill, bootstrap and dogfood paths: inspected fixes without commit messages or earlier verdicts.
- With GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt/review-tmp/2026-10-25d-leg22 and PYTHONDONTWRITEBYTECODE=1: C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-25d-leg22/r2-979-A/wi-979 tests/test_architecture_decomposition_rubric.py tests/test_dogfood_sync.py tests/test_bootstrap.py tests/test_skills_index.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_review_brief.py tests/test_plan_pass.py tests/test_profile.py: 368 passed, 1 skipped in 322.84s (0:05:22).
- C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict: check_trajectory: clean (976 work item(s), 864 done (89%), 34 cancelled, graph acyclic). Exit 0; advisory warnings are not represented as failures.
- trace.py --strict-integrity through runpy, redirecting only its report write into this review directory and retaining full console output in trace-console.txt: Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=132 verified-demonstrated=6 verified-attested=0 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md. Exit 0 (printed report path is the instrument's original label; actual write was redirected).
- gen_skills_index.py --check-agents: gen_skills_index: OK - 22 per-agent skill copy(ies) match source.
- gen_prompt_catalog.py --check: gen_prompt_catalog: fresh (14 prompts).
- check_docs.py: check_docs: OK - 3175 doc(s), 3760 intra-repo link(s), 0 broken (1 orphan warning(s)). Also reported the existing report orphan and status-length advisory.
- Inline Python regression probes using the actual test functions and git show cffd9f275:<path>: 3 current passes and 3 pre-fix failures; bootstrap layout current PASS/pre-fix FAIL; clarification and A8 current PASS/draft FAIL.
- Live bootstrap.py --dest <review-directory>/scaffold-probe with supported --agents both, gemini and codex, then plain add-only rerun: rubric and all three agent paths exist and match source bytes; adopter rubric preserved. Initial inspection of pytest scratch found a rubric but no selected-agent copies, so the separate live scaffold supplied that evidence.
- git diff --check with the same scope: one trailing blank line in docs/plans/WI-979/critique-2.md, a process record; no product defect.

Coverage-extension note: an exploratory unsupported --agents claude,codex,gemini input was rejected by argparse before bootstrap ran; subsequent supported selections supplied the live-flow evidence. This fail-closed input is not a finding.

VERDICT: APPROVE findings=0
