+++
id = "WI-879"
title = "adjudicate: LLR-047, LLR-270, LLR-300, LLR-301, SR-046, SR-227, SR-229, SR-230, TC-267, TC-316, TC-317, TC-318, TC-321 - approved/routed cell(s) amended on merged trunk ed2533c..fb1990a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-046", "SR-227", "SR-229", "SR-230"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-047", "LLR-270", "LLR-300", "LLR-301", "SR-046", "SR-227", "SR-229", "SR-230", "TC-267", "TC-316", "TC-317", "TC-318", "TC-321"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-046 `AcceptanceCriteria`: 'A machine listing prints one name-and-description line per declared capability in declaration order; a direct call nami…' -> 'A machine listing prints one name-and-description line per declared capability in declaration order; a direct call nami…'
- SR-227 `AcceptanceCriteria`: 'With the dial at zero, an adjudication launches exactly as a fresh session: no session id minted, no resume argument, n…' -> 'With the dial at zero, an adjudication launches exactly as a fresh session: no session id minted, no resume argument, n…'
- SR-227 `Requirement`: 'Where the declared adjudicator retention dial is above zero, the delivered adjudication content shall manage each retai…' -> 'Where the declared adjudicator retention dial is above zero, the delivered adjudication content shall manage each retai…'
- SR-229 `AcceptanceCriteria`: 'With the guard off, admission proceeds without reading or writing guard state; with it on, the holder below the thresho…' -> 'Inside an armed blackout window, every claim route, including the unattended dispatcher, refuses a new claim naming the…'
- SR-229 `Requirement`: 'Where the declared coordinator context guard is enabled, the delivered work-item admission, on every route but the unat…' -> 'Where a blackout window is armed, the delivered work-item admission shall refuse a new claim inside that window on ever…'
- SR-229 `Title`: 'Coordinator context-drain admission' -> 'Coordinator claim admission respects a blackout pause'
- SR-230 `AcceptanceCriteria`: 'With the guard off, no exit launches anything. A request from the holder for an existing handoff launches once at an ex…' -> 'With the guard off, no exit launches anything. Outside an armed blackout window, a request from the holder for an exist…'
- SR-230 `Requirement`: 'Where the declared coordinator context guard is enabled, when the coordinator lease holder that has requested a relaunc…' -> 'Where the declared coordinator context guard is enabled, when the coordinator lease holder that has requested a relaunc…'
- SR-230 `Title`: 'Coordinator successor at session exit' -> 'Coordinator successor at session exit outside a blackout pause'
- LLR-047 `Detail`: 'load_capabilities parses the docs/stack.ini [run] section (configparser, interpolation=None, case-preserving optionxfor…' -> 'load_capabilities parses the docs/stack.ini [run] section (configparser, interpolation=None, case-preserving optionxfor…'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- LLR-300 `Detail`: 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…' -> 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…'
- LLR-300 `SR-Refs`: 'SR-229' -> 'SR-229;SR-237'
- LLR-301 `Detail`: 'session_prompt extracts the one fenced session prompt from a handoff, preserving headings inside that fence as prompt t…' -> 'session_prompt extracts the one fenced session prompt from a handoff, preserving headings inside that fence as prompt t…'
- TC-267 `Expected`: "Satisfies LLR-270 (parent SR-227) with the dial on: each runner's resume and occupancy are read from its own output und…" -> "Satisfies LLR-270 (parent SR-227) with the dial on: each runner's resume and occupancy are read from its own output und…"
- TC-267 `Method`: 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…' -> 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…'
- TC-316 `Expected`: 'Exactly one coordinator owns admission, a claim without its lease refuses naming the recovery action, and the drain sta…' -> 'Exactly one coordinator owns admission, a claim without its lease refuses naming the recovery action, and the drain sta…'
- TC-316 `Method`: 'Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease…' -> 'Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease…'
- TC-317 `Expected`: 'Every guarded route to a new claim refuses after the threshold, without blocking close-out.' -> 'Every guarded route to a new claim refuses after the threshold, without blocking close-out. An armed blackout refuses c…'
- TC-317 `Method`: 'Drive the claim boundary through hook, direct import, CLI and wrapper routes at the crossing reading and with no prior …' -> 'Drive the claim boundary through hook, direct import, CLI and wrapper routes at the crossing reading and with no prior …'
- TC-318 `Expected`: 'An owned request starts one successor only at a true exit and remains recoverable on launch failure.' -> 'An owned request starts one successor only at a true exit and remains recoverable on launch failure. During blackout no…'
- TC-318 `Method`: "Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and …" -> "Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and …"
- TC-321 `Expected`: 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…' -> 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…'
- TC-321 `Method`: 'Run test_a_second_coordinator_adjudication_resumes_the_first, test_the_coordinator_route_writes_one_session_log_per_cal…' -> 'Run test_a_second_coordinator_adjudication_resumes_the_first, test_the_coordinator_route_writes_one_session_log_per_cal…'

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
- LLR-047 [project-trajectory/scripts/run_menu.py;project-trajectory/scripts/run.template.sh;project-trajectory/scripts/run.template.cmd;project-trajectory/scripts/run.template.command :: load_capabilities/interactive_menu/direct/launch] tests: (see TC-047; TC-342) — Run capability menu reader
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/primary_out_dir/store_lock/dir_lock/store_load/write_tombstone/load_honoured/is_lease_only/_apply_tombstone/_drop_lease/store_remove/keep_release/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/retire_after_blackout/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/_prepare_warm/_warm_candidates/_warm_keep/take_warm_lease;cli_version/plan_keep/KeepWarmer/_pings_one_turn/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error/auth_failed;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268, TC-322, TC-329, TC-330) — The keep operation retains adjudicator sessions through act…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…
- LLR-300 [project-trajectory/scripts/coordinator_guard.py;project-trajectory/scripts/integrate.py;project-trajectory/scripts/kitlib/shell_line.py :: GuardConfig/guard_config/Occupancy/read_occupancy/lease_dir/take/release/clear/hand_back/record_event/latch_reading/window_refusal/claim_refusal/on_blackout/launch_reason/model_clis/command_name/command_words/_assigned/_invoked/window_check/hooks_state/enable_hooks/on_monitored/on_session_start/on_pre_compact/classify_compaction/hook;claim;segments/Unreadable/Word] tests: TC-315;TC-316;TC-317 — Coordinator context occupancy, lease, and drain latch
- LLR-301 [project-trajectory/scripts/coordinator_guard.py;scripts/coordinator-relaunch.cmd;scripts/coordinator-relaunch.sh :: session_prompt/request_relaunch/on_blackout/blackout_session_end/session_end/window_check/launch_command/launch_detached/exec_claude/main] tests: TC-318 — Coordinator relaunch request and exit acquisition
- LLR-305 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_keep.py;project-trajectory/scripts/adjudicate_brief.py :: AdjudicationRequest/adjudication_keep/SigninRefused/SIGNIN_PROBES/TOKEN_VARIABLES/COMPETING_CREDENTIALS/RUNNER_REFUSAL/_read_token/_token_refusal/launch_credential/refuse_competing/_CASE_INSENSITIVE/_name_key/Prepared/prepare_launch/_resolve_executable/probe_env/compose_env/_compose/_runner_argv/_as_prepared/_launch_env/_redactor/signin_status/require_signin/route_env;dedicated_home;governing_templates] tests: (see TC-322, TC-323, TC-324, TC-330) — Coordinator adjudication shares the keep request and refuse…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
- IF-075 scripts/trace <- scripts/gen_open_items;scripts/adjudicate_brief: call reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine registry's own copy …
