+++
id = "WI-972"
title = "adjudicate: LLR-269, LLR-270, TC-265, TC-268 - approved/routed cell(s) amended on merged trunk c06a7e1..a7fec6d (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-222", "SR-227", "SR-239"]
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-269", "LLR-270", "TC-265", "TC-268"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-269 `Detail`: "A role hands a Call its data (root, role, the route's template, model and prompt, provider, tier, route id, source even…" -> "A role hands a Call its data (root, role, the route's template, model and prompt, provider, tier, route id, source even…"
- LLR-269 `SR-Refs`: 'SR-222;SR-227;SR-239' -> 'SR-222;SR-227;SR-239;SR-243'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- TC-265 `Method`: "Drive the service's act and call steps with an injected launch: a codex call returns its last-message text and its whol…" -> "Drive the service's act and call steps with an injected launch: a codex call returns its last-message text and its whol…"
- TC-268 `Method`: 'Assert a keep-warm ping is due only with the dial and its minutes on, for an active ANTHROPIC session idle past the min…' -> 'Assert a keep-warm ping is due only with the dial and its minutes on, for an active ANTHROPIC session idle past the min…'

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
- LLR-266 [project-trajectory/scripts/session_adapters.py :: adapter_for/CodexAdapter/OpencodeAdapter/json_events/HOME_VARIABLES/TOKEN_VARIABLES/cli_named/home_env] tests: (see TC-262) — One adapter per provider runner captures its structured out…
- LLR-267 [project-trajectory/scripts/session_adapters.py :: ClaudeAdapter.context/CodexAdapter.context/OpencodeAdapter.context/_codex_home/_codex_rollout] tests: (see TC-263) — Context occupancy is read from the latest request's prompt
- LLR-268 [project-trajectory/scripts/session_adapters.py :: OTEL_SEMCONV/USAGE_KEYS/USAGE_COUNT_KEYS/usage_record/_claude_usage/CodexAdapter.usage/OpencodeAdapter.usage] tests: (see TC-264) — Each adapter maps its runner's usage to the pinned OpenTele…
- LLR-269 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/plan_runner.py :: Call/_one_thread/_thread_argv/act/record/call/spool_dir/lane_branch/lane_wis/is_call_log;launch_session;_dp_session] tests: (see TC-265) — One session service launches and records every model call
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py;project-trajectory/scripts/kitlib/config.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/primary_out_dir/store_lock/dir_lock/store_load/load_honoured/is_lease_only/store_remove/keep_release/APPLY_WAIT/_compaction_seen/_marker_name/keep_marker/publish_marker/Pending/_pending/_parse_marker/fold_marker/fold_markers/_released/_landing/Honoured/_folded/_busy/_observation/due_routes/retire_stale_lease/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/retire_after_blackout/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/_prepare_warm/_warm_candidates/_warm_keep/take_warm_lease/scoped_route/retire_scope/review_retention/ReviewRetention/_record_name/_read_record/_variant/_nonempty_str/_conforms;cli_version/plan_keep/KeepWarmer/KeepWarmer._ping/KeepWarmer._record_finished/KeepWarmer._raise_unended/KeepWarmer.finish/_pings_one_turn/_warm_routes/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error/auth_failed;adjudication_keep/review_keep_scope/review_keep_templates/draw_session_route;run;reviewer_dials] tests: (see TC-266, TC-267, TC-268, TC-322, TC-329, TC-330) — The keep operation retains adjudicator and loop reviewer se…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks, build; one key = value per line
- IF-044 scripts/agent_route <- scripts/agent_loop;scripts/session_service;scripts/plan_runner;scripts/coordinator_adjudicate: call resolve_enabled(tokens, registry) -> enabled entries, errors; resolve_entry(token, registry) -> entry or why;…
- IF-064 scripts/agent_session <- scripts/agent_loop;scripts/session_service;scripts/plan_runner: call build_argv, run_session, parse_json_result and the console renderers
