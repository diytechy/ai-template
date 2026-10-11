+++
id = "WI-904"
title = "adjudicate: LLR-270, TC-268 - approved/routed cell(s) amended on merged trunk 54f74c2..22f322d (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-270", "TC-268"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- LLR-270 `SR-Refs`: 'SR-227' -> 'SR-227;SR-238'
- TC-268 `Method`: 'Assert a keep-warm ping is due only with the dial and its minutes on, for an active ANTHROPIC session idle past the min…' -> 'Assert a keep-warm ping is due only with the dial and its minutes on, for an active ANTHROPIC session idle past the min…'
- TC-268 `Verifies`: 'SR-227;LLR-270;IF-044;IF-065' -> 'SR-227;SR-238;LLR-270;IF-044;IF-065'

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
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/primary_out_dir/store_lock/dir_lock/store_load/write_tombstone/load_honoured/is_lease_only/_apply_tombstone/_drop_lease/store_remove/keep_release/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/retire_after_blackout/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/_prepare_warm/_warm_candidates/_warm_keep/take_warm_lease;cli_version/plan_keep/KeepWarmer/KeepWarmer._raise_unended/_pings_one_turn/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error/auth_failed;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268, TC-322, TC-329, TC-330) — The keep operation retains adjudicator sessions through act…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…
- LLR-305 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_keep.py;project-trajectory/scripts/adjudicate_brief.py :: AdjudicationRequest/adjudication_keep/SigninRefused/SIGNIN_PROBES/TOKEN_VARIABLES/COMPETING_CREDENTIALS/RUNNER_REFUSAL/_read_token/_token_refusal/launch_credential/refuse_competing/_CASE_INSENSITIVE/_name_key/Prepared/prepare_launch/_resolve_executable/probe_env/compose_env/_compose/_runner_argv/_as_prepared/_launch_env/_redactor/signin_status/require_signin/route_env;dedicated_home;governing_templates] tests: (see TC-322, TC-323, TC-324, TC-330) — Coordinator adjudication shares the keep request and refuse…
- LLR-306 [project-trajectory/scripts/coordinator_adjudicate.py :: DEFAULT_ROUTE/resolve_route/lane_refusal/reserve_verdict/bind_requested/_release/adjudicate/signin/main] tests: (see TC-321) — Coordinator adjudication entry attributes a current verdict…
- TC-266 -> tests/test_session_keep.py
- TC-267 -> tests/test_session_keep.py;tests/test_adjudicator_token.py::test_an_auth_failure_records_the_call_failed_and_keeps_the_session;tests/test_adjudicator_token.py::test_an_auth_failure_on_a_first_mint_leaves_no_record;tests/test_adjudicator_token.py::test_another_failure_still_retires_the_session;tests/test_blackout_window.py::test_the_first_keep_call_after_a_window_retires_by_the_predicate;tests/test_blackout_window.py::test_a_draining_sessions_chain_does_not_survive_the_window;tests/test_blackout_window.py::test_a_wrap_up_inside_the_window_resumes_the_retained_session;tests/test_blackout_window.py::test_no_keep_warm_ping_fires_inside_the_window;tests/test_blackout_window.py::test_a_keep_warm_tick_first_after_the_window_retires_and_never_refreshes

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/dispatch;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict;scripts/plan_coverage;scripts/review_brief: call parse_verdict: typed verdict findings, where a finding is a bullet whose bracket names one of the module's de…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
