+++
id = "WI-905"
title = "adjudicate: LLR-045, LLR-140, LLR-207, LLR-262, LLR-269, LLR-270, LLR-305, SR-154, SR-156, TC-205, TC-266, TC-322 - approved/routed cell(s) amended on merged trunk b3ef428..c10cce0 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-154", "SR-156", "SR-222", "SR-227", "SR-238"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-045", "LLR-140", "LLR-207", "LLR-262", "LLR-269", "LLR-270", "LLR-305", "SR-154", "SR-156", "TC-205", "TC-266", "TC-322"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-154 `AcceptanceCriteria`: 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…' -> 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…'
- SR-156 `AcceptanceCriteria`: 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…' -> 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…'
- LLR-045 `Detail`: 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…' -> 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…'
- LLR-140 `Detail`: 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…' -> 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…'
- LLR-207 `Detail`: 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…' -> 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…'
- LLR-262 `Detail`: "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`), and…" -> "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`), and…"
- LLR-269 `Detail`: "A role hands a Call its data (root, role, the route's template, model and prompt, provider, tier, route id, source even…" -> "A role hands a Call its data (root, role, the route's template, model and prompt, provider, tier, route id, source even…"
- LLR-269 `SR-Refs`: 'SR-222' -> 'SR-222;SR-227;SR-239'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- LLR-270 `Rationale`: 'Retention is one more thing a call does, not a second launch path, so resume, occupancy, reset and keep-warm all go thr…' -> 'Retention is one more thing a call does, not a second launch path, so resume, occupancy, reset and keep-warm all go thr…'
- LLR-270 `SR-Refs`: 'SR-227;SR-238' -> 'SR-227;SR-238;SR-239'
- LLR-270 `Title`: 'The keep operation retains adjudicator sessions through act and record, inert at dial 0' -> 'The keep operation retains adjudicator and loop reviewer sessions through act and record, inert at dial 0'
- LLR-305 `Detail`: 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…' -> 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…'
- LLR-305 `SR-Refs`: 'SR-227' -> 'SR-227;SR-239'
- TC-205 `Expected`: "Satisfies SR-156: the serial seam's verdict rung is computed from committed evidence a logged reviewer session produced…" -> "Satisfies SR-156: the serial seam's verdict rung is computed from committed evidence a logged reviewer session produced…"
- TC-205 `Method`: "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…" -> "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…"
- TC-266 `Expected`: "Satisfies LLR-270 (parent SR-227): the shipped template is inert, this repository's enabled dial has the same shape, an…" -> 'Satisfies LLR-270 (parents SR-227 and SR-239): the shipped dials are inert and share their declared structure; an off a…'
- TC-266 `Method`: 'Read the shipped policy file and its template: the template declares [adjudicator] with context_reset_pct = 0, this rep…' -> 'Read the shipped policy file and its template: the template declares adjudicator context_reset_pct 0 and this repositor…'
- TC-266 `Verifies`: 'SR-227;LLR-270;IF-248;IF-065' -> 'SR-227;SR-239;LLR-270;IF-248;IF-065'
- TC-322 `Expected`: 'The loop hands keep planning the route, work item, environment, template, and deadline-derived lease inputs. Every reta…' -> 'The loop hands keep planning route, work item, environment, configuration, deadline-derived lease inputs, and scope. Ev…'
- TC-322 `Method`: 'Run test_the_loop_composes_the_same_keep_request_as_before, test_switching_retained_classes_with_nothing_edited_keeps_t…' -> 'Run the existing retained-class identity cases and test_a_retained_reviewers_identity_is_its_own_template. Assert the r…'
- TC-322 `Verifies`: 'SR-227;LLR-270;LLR-305;IF-282' -> 'SR-227;SR-239;LLR-270;LLR-305;IF-282'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-026 [project-trajectory/scripts/agent_session.py;project-trajectory/scripts/session_adapters.py :: build_argv/run_session/_codex_lastmsg_setup/_win32/_contain_in_job/_spawn_session/_end_launch/_end_suspended/_start_session_io/_feed_stdin/TreeNotEnded/_kill_tree/_end_job_tree/_end_group_tree/_terminate_job/_close_job/_open_job_members/_in_job/_close_handles/_job_active_processes/_job_survivors/_group_survivors/_await_tree_end] tests: (see TC-026) — Headless session launch
- LLR-044 [project-trajectory/scripts/agent_route.py :: load_registry/resolve_enabled/parse_env/select] tests: (see TC-046) — Agent pair-row routing
- LLR-045 [project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/agent_brief.py :: main/reviewer_prompt/narrow_scope_line/narrow_reviewer_prompt/full_scope_line/review_round_brief/review_template_refusals/review_template/review_round_templates/close_round_scope/phase_tier] tests: (see TC-082) — Managed review dispatch
- LLR-046 [project-trajectory/scripts/score_reviews.py :: SEVERITIES/substance/fired_tripwires/record_round/_finding/parse_verdict] tests: (see TC-083) — Review substance scorer
- LLR-048 [project-trajectory/scripts/agent_brief.py :: load_critique_srs/build_scope_srs/critique_brief/critique_prompt] tests: (see TC-048) — Independent critique dispatch
- LLR-081 [project-trajectory/scripts/agent_route.py :: escalate/failure_action] tests: (see TC-084) — Fixed review escalation

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
