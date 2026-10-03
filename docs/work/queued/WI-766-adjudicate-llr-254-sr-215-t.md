+++
id = "WI-766"
title = "adjudicate: LLR-254, SR-215, TC-024, TC-036, TC-055, TC-209, TC-210, TC-211, TC-247, TC-248 - approved/routed cell(s) amended on merged trunk 122816d..1f1dc64 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-215"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-254", "SR-215", "TC-024", "TC-036", "TC-055", "TC-209", "TC-210", "TC-211", "TC-247", "TC-248"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-215 `AcceptanceCriteria`: 'At a work-item merge and at release preparation, each observation test case has its declared inputs hashed; one whose d…' -> 'Every observation case references a numbered rubric written before its first judgement; existing omissions warn. No res…'
- SR-215 `Rationale`: 'A judgment made by inspection, critique or observation holds only for the state it looked at, and nothing re-fires it o…' -> 'Judgements cost time and model calls and vary across sessions. A fixed rubric makes the pass criterion reviewable; a cl…'
- SR-215 `Requirement`: 'When a work item merges or a release is prepared, the delivered harness shall file one re-judge work item for each obse…' -> 'When a work item merges, a release is prepared or a stage gate is checked, the delivered harness shall file one re-judg…'
- LLR-254 `Detail`: 'A pure sibling of consolidate.py that intake imports. observation_test_cases(root, rev) reads the observation cases at …' -> 'A sibling of consolidate.py imported by intake. observation_test_cases(root, rev) reads observation cases at a revision…'
- TC-024 `Verifies`: 'SR-024;LLR-024' -> 'SR-024;LLR-024;IF-270'
- TC-036 `MinWorkItems`: '' -> '10'
- TC-036 `Rubric`: '' -> 'docs/rubrics/resync-inspection.md'
- TC-036 `Trigger`: '' -> 'files:project-trajectory/ADOPTING.md;project-trajectory/skills/downstream-resync/*'
- TC-055 `MinWorkItems`: '' -> '10'
- TC-055 `Rubric`: '' -> 'docs/rubrics/dashboard-usability.md'
- TC-055 `Trigger`: '' -> 'component:CMP-009'
- TC-209 `MinWorkItems`: '' -> '10'
- TC-209 `Rubric`: '' -> 'docs/rubrics/critique-provenance.md'
- TC-209 `Trigger`: '' -> 'release'
- TC-210 `MinWorkItems`: '' -> '10'
- TC-210 `Rubric`: '' -> 'docs/rubrics/counterpart-review.md'
- TC-210 `Trigger`: '' -> 'release'
- TC-211 `MinWorkItems`: '' -> '10'
- TC-211 `Rubric`: '' -> 'docs/rubrics/decomposition-proportionality.md'
- TC-211 `Trigger`: '' -> 'release'
- TC-247 `Expected`: "Satisfies SR-215's acceptance: a changed, expired or unjudged observation case gets exactly one open re-judge item nami…" -> 'Satisfies SR-215 acceptance: missing or expired evidence is due; other judgements obey their trigger and floor, and eac…'
- TC-247 `Method`: 'checkpoint_drafts driven on a real git repository. An observation case whose declared input changed since its latest re…' -> 'checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inp…'
- TC-248 `Method`: "Driven through intake on a real git repository. A merged work item whose merge changes an observation case's declared i…" -> 'Driven through intake on a real git repository. A merged work item satisfying an observation case’s trigger and closed-…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision
- LLR-255 [project-trajectory/scripts/intake.py;project-trajectory/scripts/gen_release_checklist.py :: intake_after_merge/mint_rejudge/_cmd_rejudge/_rejudge_checklist_line] tests: - — The merge and release checkpoints file the re-judge items
- LLR-265 [project-trajectory/scripts/intake.py :: merged_outcomes/_merged_shape_refusal/_cmd_sweep] tests: - — The merge-slot intake re-run for a merge made outside the s…
- LLR-293 [project-trajectory/scripts/observation_cadence.py :: Cadence] tests: - — The observation cadence policy
- LLR-294 [project-trajectory/scripts/observation_cadence.py :: observation_rubric_findings] tests: - — The observation rubric-reference advisory
- TC-247 -> tests/test_rejudge.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — one `- [ ] <ID> — <what to confirm> (refs)` item per human-verified row
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-090 scripts/intake <- scripts/integrate;scripts/dispatch;scripts/agent_loop: call intake_after_merge (integrate) · mint_gap_rows (dispatch) · context_block (agent_loop, advisory)
