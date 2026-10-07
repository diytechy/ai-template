+++
id = "WI-845"
title = "adjudicate: LLR-167, LLR-262, LLR-277, LLR-278, LLR-305, LLR-306, SR-156, TC-257, TC-278 - approved/routed cell(s) amended on merged trunk 0ce475f..68e0ee8 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-156"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-167", "LLR-262", "LLR-277", "LLR-278", "LLR-305", "LLR-306", "SR-156", "TC-257", "TC-278"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-156 `AcceptanceCriteria`: 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…' -> 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…'
- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint that has a brief to…" -> "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint that has a brief to…"
- LLR-262 `Detail`: "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`); ses…" -> "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`); ses…"
- LLR-277 `Detail`: 'spine_carrier.needs_from_text(text, carrier) reads .toml text as its need tables only and .md text as the legacy tables…' -> 'spine_carrier.needs_from_text(text, carrier) reads .toml text as its need tables only and .md text as the legacy tables…'
- LLR-278 `Detail`: 'acceptance_record.merge_approval_refusal calls reattest_scope_refusal and held_reattest_refusal for an adjudication lan…' -> 'acceptance_record.merge_approval_refusal calls reattest_scope_refusal and held_reattest_refusal for an adjudication lan…'
- LLR-305 `Detail`: 'REQUEST. AdjudicationRequest carries root, brief, family, route id, work item, route template and environment, role, th…' -> 'REQUEST. AdjudicationRequest carries root, brief, family, route id, work item, route template and environment, role, th…'
- LLR-306 `Detail`: 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…' -> 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…'
- TC-257 `Expected`: "Satisfies LLR-262: a review session's range may change only its verdict file, checked right after the session and at th…" -> "Satisfies LLR-262: a review session's range may change only its verdict file, checked right after the session and at th…"
- TC-257 `Method`: 'On git repositories, in modules registered as slow: a later commit rewriting a CHANGES-REQUESTED round to APPROVE, asse…' -> 'On git repositories, in modules registered as slow: a later commit rewriting a CHANGES-REQUESTED round to APPROVE, asse…'
- TC-278 `Expected`: "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…" -> "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…"
- TC-278 `Method`: 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…' -> 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…'

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
- LLR-138 [project-trajectory/scripts/agent_common.py :: tracked_pause/pause_reason] tests: (see TC-131) — Tracked pause reader (dual-home)
- LLR-140 [project-trajectory/scripts/integrate.py :: claim/finished_branches/_verdict_gate/integrate_one/audit] tests: (see TC-132) — Local integrator (claim + queue + audit)
- LLR-145 [project-trajectory/scripts/spec_move.py :: move_spec/expected_relink/expected_rebase/archive_dest] tests: (see TC-139) — Link-aware spec-move ritual (move + relink indivisible)
- LLR-150 [project-trajectory/scripts/lane.py :: ensure_worktree/worker_argv/spawn_worker/run_worker/spawn_refresh] tests: (see TC-144) — Lane mechanics: worktree, worker subprocess, §A2 refresh su…
- LLR-151 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/bookkeeping.py :: _dispatch_lock/claim/_claim_refusal/_abandoned_claim;commit] tests: (see TC-145) — Dispatch-lock claim rung + the spine batch claim
- LLR-207 [project-trajectory/scripts/kitlib/verdict.py :: RECORD_PREFIXES/fold_listing/tree_identity/refresh_subject/refresh_attestation/mechanical_close_attestation/work_tip/governing_rev/governing_identity/format_trailer/parse_trailer/round_file/session_log/branch_paths/logged_rounds/round_entries/branch_entries/declared_phases/phases_owed/round_count/format_branch_trailer/branch_trailers] tests: TC-205 — The verdict record: what carries a governing verdict, and w…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md generated block: stage, spine counts, ready frontier, cited items and held rows, uncited items…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
