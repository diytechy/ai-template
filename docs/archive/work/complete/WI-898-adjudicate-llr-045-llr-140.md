+++
id = "WI-898"
title = "adjudicate: LLR-045, LLR-140, LLR-207, LLR-262, SR-154, SR-156, TC-082, TC-205 - approved/routed cell(s) amended on merged trunk 1f87388..b676630 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-154", "SR-156"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-045", "LLR-140", "LLR-207", "LLR-262", "SR-154", "SR-156", "TC-082", "TC-205"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-884's in-lane amendment sittings ruled every listed row MEANING and blessed it: sitting 003 (`docs/reviews/wi-884/003-ADJUDICATE-8b9cb0c.md`) re-attested SR-154, SR-156, LLR-045, LLR-140, LLR-207 and LLR-262, and sitting 004 (`docs/reviews/wi-884/004-ADJUDICATE-4110810.md`) re-attested TC-082 and TC-205 (docs/archive/last_approved/acts.toml). At the landing b6766302 the system, low-level and test registries are byte-equal to their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-154 `AcceptanceCriteria`: 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…' -> 'A declared review policy of N schedules N independent reviewer sessions; the declared (family x model x tier) pair-rows…'
- SR-156 `AcceptanceCriteria`: 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…' -> 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…'
- LLR-045 `Detail`: 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…' -> 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…'
- LLR-140 `Detail`: 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…' -> 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…'
- LLR-207 `Detail`: 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…' -> 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…'
- LLR-262 `Detail`: "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`); ses…" -> "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`), and…"
- TC-082 `Expected`: 'Managed scheduling matches policy with redacted logged routing; bad prompts fail preflight; unmanaged mode stays legacy…' -> 'Managed scheduling matches policy with redacted logged routing; bad prompts fail preflight; unmanaged mode stays legacy…'
- TC-082 `Method`: "Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases. The queue's phases are…" -> "Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases. The queue's phases are…"
- TC-205 `Expected`: "Satisfies SR-156: the serial seam's verdict rung is computed from committed evidence a logged reviewer session produced…" -> "Satisfies SR-156: the serial seam's verdict rung is computed from committed evidence a logged reviewer session produced…"
- TC-205 `Method`: "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…" -> "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…"
- TC-205 `Verifies`: 'SR-156;LLR-207;IF-175' -> 'SR-154;SR-156;LLR-140;LLR-207;LLR-262;IF-175'

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
- LLR-044 [project-trajectory/scripts/agent_route.py :: load_registry/resolve_enabled/parse_env/select] tests: (see TC-046) — Agent pair-row routing
- LLR-045 [project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/agent_brief.py :: main/reviewer_prompt/narrow_scope_line/narrow_reviewer_prompt/full_scope_line/review_round_brief/review_template_refusals/close_round_scope/phase_tier] tests: (see TC-082) — Managed review dispatch
- LLR-046 [project-trajectory/scripts/score_reviews.py :: SEVERITIES/substance/fired_tripwires/record_round/_finding/parse_verdict] tests: (see TC-083) — Review substance scorer
- LLR-048 [project-trajectory/scripts/agent_brief.py :: load_critique_srs/build_scope_srs/critique_brief/critique_prompt] tests: (see TC-048) — Independent critique dispatch
- LLR-081 [project-trajectory/scripts/agent_route.py :: escalate/failure_action] tests: (see TC-084) — Fixed review escalation
- LLR-082 [project-trajectory/scripts/agent_loop.py :: main/critique_rounds/critique_failure_action] tests: (see TC-085) — Bounded critique rework

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
