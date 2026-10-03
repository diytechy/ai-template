+++
id = "WI-782"
title = "adjudicate: LLR-238, LLR-240, LLR-243, LLR-258, SR-191, SR-192, SR-197, SR-198, SR-199, SR-201, SR-202, SR-203, SR-206, SR-218, TC-227, TC-233, TC-234, TC-235, TC-238, TC-251 - approved/routed cell(s) amended on merged trunk 1273a99..25f7f0a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-191", "SR-192", "SR-197", "SR-198", "SR-199", "SR-201", "SR-202", "SR-203"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-200", "LLR-237", "TC-232", "LLR-238", "LLR-240", "LLR-243", "LLR-258", "SR-191", "SR-192", "SR-197", "SR-198", "SR-199", "SR-201", "SR-202", "SR-203", "SR-206", "SR-218", "TC-227", "TC-233", "TC-234", "TC-235", "TC-238", "TC-251"]
+++

## Deliverable

Act seq 25 (one combined act with WI-783): all 23 rows are re-attested. The independent Claude Opus 5.5 adjudicator ruled the 20 rows WI-771 amended and the three rows it retired.

- **CLARITY:** 9 rows, where "evidences an assumption" became "can falsify an assumption".
- **MEANING, blessed:** 11 rows: the ladder dropped from the brief, the gate, the accepted-risk binding and the per-need view.
- **Retirements:** SR-200, LLR-237 and TC-232, carried in mid-sitting, blessed with their successors SR-201, LLR-238 and TC-233.

LLR-243 and TC-238 were first returned, because the reopening of a risk accepted while the assumption was active had no test. Under the owner's 2026-10-03 S11 direction the return was fixed in this lane, not minted:
- an Opus builder applied the byte-exact fix list (fea1b8f3);
- the adjudicator re-judged it and blessed it (c042a79c), with the probe failing two tests.

Codex Luna (high) cross-review: SOUND at 1b2bbfa4, no findings (`docs/reviews/2026-10-03-wave9/luna-wi782.md`). Verdict: `docs/reviews/wi-782-adjudicate-llr-238-llr-240/001-ADJUDICATE-d040ad7.md`.

## Context

Carried in by the coordinator 2026-10-03, mid-sitting: SR-200, LLR-237 and TC-232, the three approved rows WI-771 retired (successors SR-201, LLR-238 and TC-233; records under `docs/log.d/retired/`). Intake's amendment walk reads only rows still present in the live registry, so a removal mints no adjudication. The combined act's copy was refused naming them, so this sitting judges the removals too.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-191 `Rationale`: 'A requirement states what the system does at its own interface, and a stakeholder need states what a person experiences…' -> 'A requirement states what the system does at its own interface, and a stakeholder need states what a person experiences…'
- SR-192 `Rationale`: 'A stand-in for an outside party — a scripted model runner, a fresh scaffold in a temporary directory, a model judging a…' -> 'A stand-in for an outside party — a scripted model runner, a fresh scaffold in a temporary directory, a model judging a…'
- SR-197 `AcceptanceCriteria`: 'A test case naming only assumptions is valid and is not an orphan; a test case naming no requirement, design row or ass…' -> 'A test case naming only assumptions is valid and is not an orphan; a test case naming no requirement, design row or ass…'
- SR-197 `Coincident`: "The need asks for a premise's evidence counted apart from the system's; a test case naming the assumptions it evidences…" -> "The need asks for the tests that can show a premise false counted apart from the system's evidence; a test case naming …"
- SR-197 `Rationale`: "Evidence about an assumption is not evidence about the system's behavior, and counting both in one field would merge th…" -> "A test that can show an assumption false is not evidence about the system's behavior, and counting both in one field wo…"
- SR-197 `Requirement`: 'The delivered harness shall accept a test case that evidences assumptions in place of, or beside, the requirements and …' -> 'The delivered harness shall accept a test case that names the assumptions its failure shows false in place of, or besid…'
- SR-197 `Title`: 'A test case evidences assumptions in a field of its own' -> 'A test case names the assumptions it can falsify in a field of its own'
- SR-198 `AcceptanceCriteria`: 'A test case is an observation test case when it is recorded as not automated — a judgment the harness cannot rerun — wh…' -> 'A test case is an observation test case when it is recorded as not automated — a judgment the harness cannot rerun — wh…'
- SR-198 `Rationale`: "An observation — a person reading a render, a critique of a rendered view, a measurement taken across an adopter's firs…" -> "An observation — a person reading a render, a critique of a rendered view, a measurement taken across an adopter's firs…"
- SR-198 `Requirement`: 'The delivered harness shall report an observation test case that omits the inputs its judgment reads, its result lifeti…' -> 'The delivered harness shall report an observation test case that omits the inputs its judgment reads, its result lifeti…'
- SR-199 `Coincident`: 'The needs ask for each premise showing whether a current result evidences it; the observation result recorded apart, wi…' -> 'The needs ask for each premise showing whether it has been shown false; the observation result recorded apart, with its…'
- SR-201 `AcceptanceCriteria`: 'A falsified assumption is reported with the requirements citing it, the needs they serve and the test cases evidencing …' -> 'A falsified assumption is reported with the requirements citing it, the needs they serve and the test cases that can sh…'
- SR-201 `Requirement`: 'When an assumption is recorded as falsified, or an observation result evidencing it fails, the delivered harness shall …' -> 'When an assumption is recorded as falsified, or an observation result fails on one of the test cases whose failure show…'
- SR-202 `AcceptanceCriteria`: 'An assumption with a recorded accepted risk and no current evidence is read as covered by that risk; the acceptance is …' -> "An assumption with a recorded accepted risk is read as covered by that risk; the acceptance is bound to the assumption'…"
- SR-202 `Requirement`: 'When a sample for an assumption relied on under an accepted risk fails, or the text of the assumption or of a need it s…' -> 'When a sample for an assumption relied on under an accepted risk fails, or the text of the assumption or of a need it s…'
- SR-203 `AcceptanceCriteria`: 'For each assumption in the batch the brief shows its cells, the requirements citing it with their text, the needs deriv…' -> 'For each assumption in the batch the brief shows its cells, the requirements citing it with their text, the needs deriv…'
- SR-203 `Coincident`: 'The needs ask for an owner approving a premise for what it lets the requirements claim; the brief showing each assumpti…' -> 'The needs ask for an owner approving a premise for what it lets the requirements claim; the brief showing each assumpti…'
- SR-203 `Rationale`: "An assumption is approved for what it lets the requirements claim, so the approver's decision is whether those requirem…" -> "An assumption is approved for what it lets the requirements claim, so the approver's decision is whether those requirem…"
- SR-203 `Requirement`: 'The delivered approval brief shall present each assumption and surrogate awaiting approval with the requirements citing…' -> 'The delivered approval brief shall present each assumption and surrogate awaiting approval with the requirements citing…'
- SR-206 `AcceptanceCriteria`: 'With the gate enabled, an assumption with a current passing monitored or automated result passes; one whose only curren…' -> 'With the gate enabled, a relied-on assumption recorded as active passes, whatever results it has or lacks; one recorded…'
- SR-206 `Coincident`: 'The needs ask for a release gate that holds each relied-on premise to current evidence or an accepted risk; the failure…' -> 'The needs ask for a release gate that holds each relied-on premise to whether it has been shown false; the failure nami…'
- SR-206 `Rationale`: 'A passed sparse sample shows only that a problem was not found in that sample — small random panels find anywhere from …' -> 'A passed observation shows only that a problem was not found in what was observed, so no result proves an assumption ho…'
- SR-206 `Requirement`: 'Where the assumption gate is enabled, the delivered harness shall fail the release gate for each assumption a system re…' -> 'Where the assumption gate is enabled, the delivered harness shall fail the release gate for each assumption a system re…'
- SR-206 `Title`: 'With the assumption gate on, release requires current evidence or an accepted risk for every relied-on assumption' -> 'With the assumption gate on, release blocks on a relied-on assumption shown false unless an accepted risk covers it'
- SR-218 `AcceptanceCriteria`: "For each need the view lists every assumption cited by the need's requirements, once, with its validity, its evidence l…" -> "For each need the view lists every assumption cited by the need's requirements, once, with its approval status, its val…"
- SR-218 `Coincident`: "The needs ask for a reviewer seeing each outcome's premises and whether they are evidenced; the per-need view of each a…" -> "The needs ask for a reviewer seeing each outcome's premises and whether any has been shown false; the per-need view of …"
- SR-218 `Rationale`: 'The need promises that a reviewer can see what each outcome relies on and whether it has been checked. The per-assumpti…' -> 'The need promises that a reviewer can see what each outcome relies on and whether any of it has been shown false. The p…'
- SR-218 `Requirement`: 'The delivered state view shall show, for each stakeholder need, the assumptions its requirements rely on, with each ass…' -> 'The delivered state view shall show, for each stakeholder need, the assumptions its requirements rely on, with each ass…'
- SR-218 `Title`: 'The state view shows, for each need, the assumptions it relies on and their evidence' -> 'The state view shows, for each need, the assumptions it relies on and whether any has been shown false'
- LLR-238 `Detail`: 'falsification_worklist(das, srs, tcs, records) takes each assumption whose standing reads falsified, or whose latest ob…' -> 'falsification_worklist(das, srs, tcs, records) takes each assumption whose standing reads falsified, or whose latest ob…'
- LLR-240 `Detail`: "assumption_rules.assumption_chain(da_id, reg) gathers an assumption's cells, its citing requirements with their text, t…" -> "assumption_rules.assumption_chain(da_id, reg) gathers an assumption's cells, its citing requirements with their text, t…"
- LLR-243 `Detail`: 'release_gate_findings(das, srs, levels, risks, tcs) fails each assumption cited by at least one requirement whose evide…' -> 'release_gate_findings(das, srs, risks) fails each assumption cited by at least one requirement whose standing reads fal…'
- LLR-258 `Detail`: 'traj_parse.need_assumptions(root) derives, for each need, the assumptions cited by its requirements, each once, with it…' -> 'traj_parse.need_assumptions(root) derives, for each need, the assumptions cited by its requirements, each once, with it…'
- TC-227 `Expected`: "Satisfies SR-197's acceptance clause that wherever evidence is counted, assumption evidence is counted apart from requi…" -> "Satisfies SR-197's acceptance clause that wherever evidence is counted, the test cases that can falsify an assumption a…"
- TC-233 `Method`: 'falsification_worklist called on in-memory rows. A falsified assumption cited by two requirements serving three needs, …' -> 'falsification_worklist called on in-memory rows. A falsified assumption cited by two requirements serving three needs, …'
- TC-234 `Expected`: "Satisfies SR-202's acceptance: the acceptance bound to the texts at acceptance; any later change, even one re-approved …" -> "Satisfies SR-202's acceptance: the acceptance bound to the texts at acceptance; any later change, even one re-approved …"
- TC-234 `Method`: 'Driven on a real git repository, in a module registered as slow. An assumption with an accepted risk is approved in an …' -> 'Driven on a real git repository, in a module registered as slow. An assumption with an accepted risk is approved in an …'
- TC-235 `Expected`: "Satisfies SR-203's acceptance: each assumption presented with its citing requirements, derived needs, landing crossings…" -> "Satisfies SR-203's acceptance: each assumption presented with its citing requirements, derived needs, landing crossings…"
- TC-235 `Method`: 'The approval brief rendered for a scope holding an assumption, a fidelity assumption with its surrogate, and a lone sur…' -> 'The approval brief rendered for a scope holding an assumption, a fidelity assumption with its surrogate, and a lone sur…'
- TC-238 `Expected`: "Satisfies SR-206's acceptance: current monitored or automated evidence, a sampled result under a declared sampling mode…" -> "Satisfies SR-206's acceptance: an active relied-on assumption passes whatever its results; a falsified one passes only …"
- TC-238 `Method`: 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow. A relied-on assu…' -> 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule cal…'
- TC-238 `Verifies`: 'SR-206;LLR-243' -> 'SR-206;LLR-243;IF-216'
- TC-251 `Expected`: "Satisfies SR-218's acceptance: per need, each relied-on assumption once with validity, evidence level and citing requir…" -> "Satisfies SR-218's acceptance: per need, each relied-on assumption once with status, validity, falsifier, falsifying ca…"
- TC-251 `Method`: "The dashboard generated on a scaffold with needs, requirements, assumptions and records. Each need's detail lists every…" -> "The dashboard generated on a scaffold with needs, requirements, assumptions and records. Each need's detail lists every…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-218 [project-trajectory/scripts/kitlib/spine.py;project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/migrate_carrier.py;project-trajectory/scripts/kitlib/bootstrap_manifest.py;project-trajectory/registries/assumptions.template.toml :: OFFSPINE_TABLE/OFFSPINE_KEYS/MAPPING] tests: - — The assumptions registry: tiers, schema, carrier, template …
- LLR-219 [project-trajectory/scripts/assumption_rules.py;project-trajectory/scripts/trace.py :: assumption_row_findings/STANDING_VALUES/DA_REQUIRED] tests: - — Assumption row findings: required cells, vocabularies, land…
- LLR-220 [project-trajectory/scripts/acceptance_record.py;project-trajectory/scripts/baseline_snapshot.py :: SNAPSHOTTED/SNAPSHOT_TIERS/APPROVAL_ACT_CSVS] tests: - — Assumptions and surrogates in the acceptance record, inside…
- LLR-221 [project-trajectory/scripts/assumption_rules.py :: surrogate_findings/SUR_REQUIRED] tests: - — Surrogate findings: required cells, emulated parties, fidel…
- LLR-225 [project-trajectory/scripts/acceptance_record.py :: SPINE_TRACED_CELLS/SPINE_APPROVED_CELLS/OFFSPINE_TRACED_CELLS] tests: - — Each new cell's class: traced or approved content
- LLR-229 [project-trajectory/scripts/kitlib/spine.py;project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/migrate_carrier.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/coherence.py;project-trajectory/registries/test-cases.template.toml :: tc_citation_findings/_tc_verifies_required] tests: - — The test case's assumption references and the conditional V…

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
