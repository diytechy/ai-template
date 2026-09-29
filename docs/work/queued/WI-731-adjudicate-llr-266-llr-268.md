+++
id = "WI-731"
title = "adjudicate: LLR-266, LLR-268, SR-222, SR-227, TC-264 - spine row(s) authored Drafted on merged trunk a20b496..17c54c2 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-266", "LLR-267", "LLR-268", "LLR-269", "LLR-270", "SR-222", "SR-227", "TC-262", "TC-264"]
+++

## Context

Carry-over added 2026-09-29 by the coordinator, from spine-acts batch G. LLR-267, LLR-269, LLR-270 and TC-262 were APPROVED in batch G's WI-724 verdict, but their Status flip was held: the LLR and TC snapshot was refused while WI-726's returned LLR-223 and TC-220 drifted. They are added to `adjudicates` so this brief renders them. Judge them afresh on the current text (WI-729 did not touch them), and flip them in this act if they still hold.

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-222 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Requirement)
- SR-227 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Requirement)
- LLR-266 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-268 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-264 amended in `docs/test/test-cases.toml` (Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-266 [project-trajectory/scripts/session_adapters.py :: adapter_for/CodexAdapter/OpencodeAdapter/json_events] tests: (see TC-262) — One adapter per provider runner captures its structured out…
- LLR-267 [project-trajectory/scripts/session_adapters.py :: ClaudeAdapter.context/CodexAdapter.context/OpencodeAdapter.context] tests: (see TC-263) — Context occupancy is read from the latest request's prompt
- LLR-268 [project-trajectory/scripts/session_adapters.py :: OTEL_SEMCONV/USAGE_KEYS/USAGE_COUNT_KEYS/usage_record/_claude_usage/CodexAdapter.usage/OpencodeAdapter.usage] tests: (see TC-264) — Each adapter maps its runner's usage to the pinned OpenTele…
- LLR-269 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/plan_runner.py :: Call/act/record/call;launch_session;_dp_session] tests: (see TC-265) — One session service launches and records every model call
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/store_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268) — The keep operation retains adjudicator sessions through act…
- TC-262 -> tests/test_session_adapters.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-064 scripts/agent_session <- scripts/agent_loop;scripts/session_service;scripts/plan_runner: call build_argv, run_session, parse_json_result and the console renderers
