Reviewed: 9f35d60eaaaafffd440465bc6d94b836fd036a99

Verified: Independently exercised the prescribed suite, actual convergence CLI render, dispute parsing/binding, rework exclusions and plan-cap refusals. Unknown stance/ruling values fail closed. Skill copies and approved snapshots match. Changed rows have re-attestation entries without Status flips. The substantive defect is missing convergence severity instructions, despite the amended requirement claiming them. No reviewed code was edited and no commit was made.

Commands:

- `git rev-parse HEAD`; `git status --short`: reviewed SHA matched before execution and at close; tracked working tree clean.
- Scoped `git diff c0dfd18231be56b50ac8d75884d49f21e891858a...9f35d60eaaaafffd440465bc6d94b836fd036a99 -- .` with the brief's exclusions and its additional convergence exclusions; targeted `git show`, message-free `git log --format=%h`, `rg`, and `Get-Content`: inspected authored work, specification and cited/historical registry rows. Did not read filed critiques, decisions, session notes or prior code-review verdicts. The independently authored single-plan artifact was read as diff content, not accepted as evidence of implementation correctness.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate` and bytecode writing disabled, ran:

  `& 'C:/Projects/ai-template/.venv/Scripts/python.exe' -m pytest -q -p no:cacheprovider -n 2 --basetemp 'C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/wi-911' 'tests/test_adjudicate_brief.py' 'tests/test_agent_loop_review.py' 'tests/test_coordinator_adjudicate.py' 'tests/test_dispute.py' 'tests/test_evidence_join.py' 'tests/test_plan_coverage.py' 'tests/test_plan_coverage_step.py' 'tests/test_plan_filing.py' 'tests/test_plan_gate.py' 'tests/test_plan_pass.py' 'tests/test_prompts.py' 'tests/test_resync_pack.py' 'tests/test_review_brief.py' 'tests/test_review_brief_git.py' 'tests/test_routing_and_prompts.py'`

  Summary: `525 passed, 18 warnings in 1341.63s (0:22:21)`. One run; no full-suite or smoke-tier run.
- `& 'C:/Projects/ai-template/.venv/Scripts/python.exe' 'project-trajectory/scripts/check_trajectory.py' --strict`: `check_trajectory: clean (922 work item(s), 802 done (87%), 30 cancelled, graph acyclic).`
- `& 'C:/Projects/ai-template/.venv/Scripts/python.exe' 'project-trajectory/scripts/trace.py' --strict-integrity | Select-Object -Last 1`: `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 verified-mechanized=124 verified-demonstrated=6 verified-attested=0 drafts=1 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=244 interface-findings=0 ac-advisories=1 form-findings=1 paraphrase-advisories=3. Report -> docs\test\report.md`
- `& 'C:/Projects/ai-template/.venv/Scripts/python.exe' project-trajectory/scripts/review_brief.py review --wi WI-911 --base c0dfd18231be56b50ac8d75884d49f21e891858a --sha 9f35d60eaaaafffd440465bc6d94b836fd036a99 --scope full --stance convergence --tests tests/test_review_brief.py --scratch C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/probe --rubric docs/rubrics/kit-change-review.md --out C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/rendered-convergence.md`: brief written successfully. Inspection of that actual output: `Actual rendered convergence clause: True` for the clause permitting `convergence-class: no`; `Required new-finding severity restriction present: False`. The brief contains no instruction limiting new BLOCKER/MAJOR findings to the three convergence classes.
- Read-only Python byte/copy comparison: all three changed skill files match both installed copies. PROCESS.md: `96606 -> 97946`, delta `1340`; byte-budget skill: `4468 -> 4453`, delta `-15`. All three amended registry snapshots are byte-identical to their live counterparts. `git ls-files --eol` reports LF for the measured files.
- `git merge-base --is-ancestor e474f51dd c0dfd18231be56b50ac8d75884d49f21e891858a`: exit 0; RESYNC anchor is on the trunk base's ancestry. `git ls-tree c0dfd18 project-trajectory/scripts/plan_gate.py` and the baseline-manifest path: both exist in the base. Message-free history and ancestry checks show pass-record commit `3de85f186` precedes structural move `28d5075c0` and behavior build `a004a7c0c`. No critique verdict was read for this check.
- Red-before runs: exported product/test fixtures with `git archive`, overlaid only the current changed test files, and selected added/changed test functions by AST comparison. All exports and test outputs are under this review's scratch directory. Ran `python -m pytest -q -p no:cacheprovider -n 2 --tb=line --basetemp <distinct literal scratch path> <selected nodes>` against each export. The initial setup named a nonexistent pyproject.toml and was corrected to the repository's actual pytest.ini; it ran no tests. An evidence-reader encoding error after the second historical run was corrected without rerunning that test group.

  Base `c0dfd18`, nodes in `red-nodes.txt`, literal basetemp `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/pre-fix-tests`: `28 failed, 16 passed in 45.67s`. The passing cases are preservation pins (including planner registry output, unchanged verdict filing/counting, ordinary reading scope, and already-refused malformed inputs); they are not claimed as fixed-defect regressions. Actual failures include `the ruling is not one of FIX|DISMISS|ESCALATE`, `assert 1 == 0` for accepted SUCCESSOR exclusion, missing registry paths, and absent stance arguments/clauses. The complete observed failing-node summary is reproduced below.

  Immediate pre-fix checks, located from patches rather than commit messages:
  - Before `353859938`, basetemp `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/temp-353859938`: `1 failed in 11.60s`; actual diff-command test fails with `assert ['docs/decisi...ritique-2.md'] == []` because earlier findings' records are exposed.
  - Before `41a9ab416`, basetemp `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/temp-41a9ab416`: `5 failed in 13.61s`; failures are the ordinary/convergence scope separation, every-tier naming rule and plan-critique reachability instruction. The real ordinary diff-command test fails with `assert ['docs/decisi...ritique-1.md'] == []` because it hides records it should retain.
  - Before `33eb29ffa`, basetemp `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/temp-33eb29ffa`: `1 failed in 3.95s`; `test_the_reviewer_brief_states_the_convergence_stance` fails its assertion requiring a history command that prints no commit message.
  - Before `01614b9df`, basetemp `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/wi-911/gate/A/temp-01614b9df`: `7 failed in 28.79s`; the changed reachability tests fail their required supported-workflow clauses in PROCESS, both rubrics, coordinator skill and reviewer/dispute directions. The second-plan-critique test specifically fails the assertion ending `and a supported workflow or the kit's own routes reach it; anything else is MINOR.`

Done-when coverage:

- D1, every deliverable in its target: inspected the skill/recipes, rubric anchors, record-at-event rule, spine and Terra guidance, reviewer/dispute templates and ruling parser/coverage changes. Passing prompt tests cover the wording corrections and real composition. UNCOVERED: the ordinary code-review convergence brief's severity restriction; finding 1. The existing convergence test pins tags, not that restriction.
- D2, synchronized skill: direct byte comparison of source, .claude and .agents copies passed.
- D3, critique registries, stance/default/refusals, SUCCESSOR and accepted-citation coverage: passing test_review_brief, test_review_brief_git, test_dispute, test_coordinator_adjudicate, test_plan_coverage and test_plan_filing cases; baseline/historical failures above establish red-before evidence. Acts 117/118 and exact snapshots record the amended rows' re-attestation. Existing plan-cap regression still requires DISMISS.
- D4, shipped changes and no forced migration: inspected the single RESYNC entry and verified its trunk anchor; prescribed test_resync_pack cases passed. It names all shipped changes and preserves old verdict parsing and ordinary defaults.
- D5, plan gate precedes build: gate exists in base and committed pass record precedes build, as independently checked above. This review did not reread the plan critiques to rejudge their approval.
- D6, baseline manifest on trunk first: manifest exists in the specified trunk base.
- D7, green landing bar: prescribed replacement suite and strict trajectory passed; strict integrity has zero integrity findings. Landing-only smoke/budget and trace --strict were not run, as instructed by the launcher, so their landing-tip result is not independently claimed here.

Independent semantic decisions on changed relationships:

- SR-233 -> LLR-311 -> TC-332: carry the reachability and convergence extension, retaining SN-006's unchanged acceptance/approval; a derived review-scope policy does not change the need's unattended outcome. Correspondence fails specifically at finding 1. LLR-311 owns the shared review-policy definition/directions; further splitting its representations would add no independent policy decision.
- SR-234 -> LLR-314/LLR-315 -> TC-334 and IF-290: carry SUCCESSOR through the one parser and template and through the accepted binding tests. Retain LLR-315's range/finding assembly contract: the allowed ruling value changes, not what constitutes a complete findings request. LLR-314 independently decides grammar/cardinality; LLR-315 independently decides complete brief assembly. Further splitting either by one literal ruling or one template field would add no independent behavior. IF-290's requestor correction is appropriate; its counterpart callable signatures remain valid because no parser parameter or return shape changes.
- SR-236 -> LLR-069 -> TC-069: carry accepted SUCCESSOR for the same finding on the rework path. Retain SR-155's plan comparison obligation and SR-154's plan-cap dismissal requirement: the default resolving set remains DISMISS-only, while the rework caller explicitly requests the wider set. This is an authorized policy extension, not a workaround preserving an unsuitable child design. Preserve the identity, pending/malformed-verdict and ordinary plan-coverage regressions. The rationale ambiguity needs the wording amendment in finding 2.
- LLR-313 -> unchanged SR-146/SR-154/SR-235 and amended TC-333, with IF-288/IF-289: carry the stance and critique-input render changes and tests. Retain the parent strict-fill, independent-review, durable-verdict and plan-cap acceptance; no approval or verdict grammar is relaxed. Retain IF-288's registry subcommand summary and IF-289's exit-code summary: detailed optional arguments remain in the owning contract body, and 0/2 semantics do not change. LLR-313's existing rendering/filing boundary remains the owning action; splitting each flag or registry label would add no independent decision. No new child decomposition is introduced.

Observed base-version failing-node summary:

```text
FAILED tests/test_dispute.py::test_a_malformed_or_incomplete_verdict_is_refused[RULING: F1 FIX ok\nRULING: R2 SUCCESSOR\n-gives no reason]
FAILED tests/test_dispute.py::test_a_successor_ruling_is_accepted_and_parsed
FAILED tests/test_dispute.py::test_an_unknown_ruling_is_refused_naming_the_four_rulings
FAILED tests/test_plan_coverage.py::test_a_cited_ruling_that_does_not_dismiss_refuses
FAILED tests/test_plan_coverage.py::test_a_successor_ruling_citing_its_verdict_passes
FAILED tests/test_coordinator_adjudicate.py::test_a_dispute_verdict_ruling_a_finding_successor_is_valid_and_bound
FAILED tests/test_prompts.py::test_a_spec_promise_reaches_only_what_supported_routes_produce
FAILED tests/test_prompts.py::test_the_coordinator_skill_gates_the_confirming_round_by_reachability
FAILED tests/test_plan_coverage.py::test_a_successor_ruling_of_another_finding_refuses
FAILED tests/test_prompts.py::test_the_dispute_brief_offers_successor_and_never_for_a_convergence_class_finding
FAILED tests/test_prompts.py::test_the_reviewer_brief_ties_severity_to_reachability_and_classifies_out_of_set_inputs
FAILED tests/test_prompts.py::test_the_reviewer_brief_states_the_convergence_stance
FAILED tests/test_prompts.py::test_the_convergence_render_excludes_every_record_of_earlier_findings
FAILED tests/test_prompts.py::test_the_llr_questions_ask_for_contract_voice_and_keep_the_trace_cells_binding
FAILED tests/test_prompts.py::test_every_tier_receives_the_one_naming_rule - ...
FAILED tests/test_prompts.py::test_the_record_at_event_rule_has_one_home - As...
FAILED tests/test_review_brief.py::test_the_scope_critique_names_the_registries_beside_the_spec
FAILED tests/test_review_brief.py::test_a_convergence_round_renders_the_one_fixed_stance_line
FAILED tests/test_review_brief.py::test_an_absent_stance_renders_the_ordinary_round
FAILED tests/test_review_brief.py::test_a_narrow_round_refuses_the_convergence_stance
FAILED tests/test_review_brief.py::test_a_convergence_brief_carries_the_stance_and_its_marking
FAILED tests/test_review_brief.py::test_only_a_convergence_brief_leaves_the_decisions_record_and_critiques_out_of_its_reading_scope
FAILED tests/test_review_brief.py::test_the_scope_rubric_names_every_registry_the_critique_brief_renders
FAILED tests/test_review_brief_git.py::test_the_reading_scope_never_shows_a_record_of_earlier_findings
FAILED tests/test_plan_filing.py::test_at_the_cap_a_successor_ruling_never_passes
FAILED tests/test_plan_filing.py::test_the_plan_critique_brief_ties_severity_to_reachability
FAILED tests/test_plan_filing.py::test_the_second_plan_critique_is_in_convergence_and_never_sees_the_first
FAILED tests/test_prompts.py::test_the_review_threat_model_dismisses_contrived_scenarios_and_gates_every_class
```

- [MAJOR] project-trajectory/prompts/reviewer.template.md:71 -> K1; Done-when gap reachable through the supported third-round/post-checkpoint `review --scope full --stance convergence` recipe: the rendered paragraph permits new BLOCKER/MAJOR findings tagged `convergence-class: no` but never states that only reachable fail-open, data-loss or Done-when gaps may receive those severities. This contradicts owner item 4 and the amended SR-233 acceptance, LLR-311 and TC-332; the existing convergence test stays green because it checks tagging rather than this restriction. The recipe also removes the by-hand addendum that supplied the rule. -> State the required severity restriction in this single owning prompt and extend its rendered-brief regression assertion to require it; this fixes the model-input trust boundary itself rather than adding a compensating downstream guard (antidote skill) -> @builder convergence-class: yes
- [MINOR] docs/requirements/system-requirements.toml:1841 -> K1, for clarity: SR-236's amended requirement and acceptance let an accepted SUCCESSOR resolve the same finding's exclusion, while its retained rationale still says a disputed finding remains open unless its accepted dismissal decided it; that exclusive wording leaves the rationale ambiguous about the newly authorized disposition. -> Amend and re-attest the rationale to distinguish in-lane resolution by accepted DISMISS or SUCCESSOR from the successor's remaining work, preserving the same-finding identity constraint -> @system-engineer
VERDICT: CHANGES-REQUESTED findings=2
