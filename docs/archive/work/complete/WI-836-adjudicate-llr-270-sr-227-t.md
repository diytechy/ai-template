+++
id = "WI-836"
title = "adjudicate: LLR-270, SR-227, TC-266 - approved/routed cell(s) amended on merged trunk 681e328..dc0333a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-227"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-270", "SR-227", "TC-266"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-835's in-lane adjudicator, through the retained session, ruled LLR-270 and TC-266 MEANING and blessed them (verdict `docs/reviews/wi-835-coordinator-retained-adjudication/002-ADJUDICATE-a10adc3.md`, act seq 37). It then ruled SR-227 and LLR-270, as further amended, MEANING and blessed them (`003-ADJUDICATE-6ca0b05.md`, act seq 38). The low-level, system and test-case registries are byte-identical to their anchors under `docs/archive/last_approved/` at the landing.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-227 `AcceptanceCriteria`: 'With the dial at zero, an adjudication launches exactly as a fresh session: no session id minted, no resume argument, n…' -> 'With the dial at zero, an adjudication launches exactly as a fresh session: no session id minted, no resume argument, n…'
- SR-227 `Rationale`: 'A DERIVED requirement, and labelled so. SN-025 asks that a configured agent implement toward the vision with no human c…' -> 'A DERIVED requirement, and labelled so. SN-025 asks that a configured agent implement toward the vision with no human c…'
- SR-227 `Requirement`: 'Where the declared adjudicator retention dial is above zero, the delivered loop content shall launch each adjudication …' -> 'Where the declared adjudicator retention dial is above zero, the delivered adjudication content shall manage each retai…'
- SR-227 `Title`: 'Where the retention dial is on, an adjudication resumes a retained session and resets it only when that is safe' -> 'Where the retention dial is on, adjudication routes retain sessions and reset them only when safe'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- TC-266 `Expected`: 'Satisfies LLR-270 (parent SR-227) at the shipped dial: the retention layer is inert and every adjudication is a fresh s…' -> "Satisfies LLR-270 (parent SR-227): the shipped template is inert, this repository's enabled dial has the same shape, an…"
- TC-266 `Method`: 'Read the shipped policy file and its template: both declare [adjudicator] with context_reset_pct = 0 and the same keys,…' -> 'Read the shipped policy file and its template: the template declares [adjudicator] with context_reset_pct = 0, this rep…'

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
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/primary_out_dir/store_lock/dir_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268, TC-322) — The keep operation retains adjudicator sessions through act…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…
- LLR-305 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_keep.py;project-trajectory/scripts/adjudicate_brief.py :: AdjudicationRequest/adjudication_keep/SigninRefused/SIGNIN_PROBES/signin_status/require_signin/route_env;dedicated_home;governing_templates] tests: (see TC-322, TC-323, TC-324) — Coordinator adjudication shares the keep request and refuse…
- LLR-306 [project-trajectory/scripts/coordinator_adjudicate.py :: DEFAULT_ROUTE/resolve_route/lane_refusal/reserve_verdict/adjudicate/signin/main] tests: (see TC-321) — Coordinator adjudication entry attributes a current verdict…
- TC-266 -> tests/test_session_keep.py
- TC-267 -> tests/test_session_keep.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
- IF-075 scripts/trace <- scripts/gen_open_items;scripts/adjudicate_brief: call reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine registry's own copy …
