+++
id = "WI-757"
title = "LLR-290/TC-303 return: state that a retained session's compacted flag and source hold for its later calls, and verify that and the reported-over-inferred precedence"
workstream = "process"
sr_refs = ["SR-227"]
specref = ""
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Deliverable

Batch L's exact return applied: LLR-290 states that once recorded, compacted and its
source hold for every later call of the retained session, a reported entry replaces
an inferred source, and an inferred drop never replaces a reported one; TC-303 says
so; two tests in `tests/test_session_keep.py` pin it (the second rewrites the rollout
without the compacted entry so the stored reported source must hold). Both rows stay
Drafted for this merge's first approval; no code change. Sonnet 5.5: SOUND at
70b00b7e (`docs/reviews/2026-10-02-wave7/sonnet-wi757.md`).

## Context

Drafted by WI-756 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE: exactly the text additions below, copied as written, in the two
Drafted rows, plus two tests. `Status` stays `Drafted`. Do not reword, extend or
"improve" any other part of these cells or of any other cell. No code change:
the code already behaves as the added text says (confirmed at 6e89705b).

THE DEFECT, confirmed at 6e89705b. `_observe_compaction` (`session_keep.py`)
starts each call from the record's `compaction_source` and never clears it
within a record. So once a session's compaction is inferred, every later call's
row carries `compacted: True` and `compaction-source: inferred` without new
evidence. A probe over rollouts [35911], [35911, 15717] and
[35911, 15717, 18000] printed `True inferred` on calls 2 and 3. LLR-290 does not
say this, and a per-call implementation satisfies its text equally. Separately,
LLR-290's "Reported evidence takes precedence over inferred evidence" has no
test with competing evidence.
`test_codex_reported_rollout_compaction_takes_precedence` has no prompt drop.

1. **LLR-290 (Drafted)**, `detail`: after `Reported evidence takes precedence over inferred evidence.` append ` Once recorded, compacted and its source hold for every later call of that retained session, though the call shows no new evidence; a reported entry replaces an inferred source, and an inferred drop never replaces a reported one.`
2. **TC-303 (Drafted)**, `method`: after `a legacy record with no rollout cursor learns the latest prompt and cursor before inferring.` insert ` After an inferred compaction, a later call whose new requests only rise still carries compacted with source inferred; a compacted entry arriving after an inferred source marks it reported, and a later drop leaves a reported source reported.`
3. **Tests** in `tests/test_session_keep.py`, using the existing `_codex_rollout` / `_codex_turn` helpers and the compacted-entry envelope variant from `test_codex_reported_rollout_compaction_takes_precedence`: (a) rollout [35911], then [35911, 15717], then [35911, 15717, 18000]; assert the third call's `compacted` is True with source `inferred`. (b) An inferred source followed by a call whose thread rollout also holds a compacted entry yields `reported`. A further drop after that leaves it `reported`. Nothing else in either row changes.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/store_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268) — The keep operation retains adjudicator sessions through act…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…
- TC-266 -> tests/test_session_keep.py
- TC-267 -> tests/test_session_keep.py
- TC-268 -> tests/test_session_keep.py
- TC-303 -> tests/test_session_keep.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
- IF-173 scripts/integrate <- scripts/dispatch;scripts/handback;scripts/lane: call claim, refresh, integrate, finished_branches, branch_outcomes, lane_worktree, the ACTIVE and WORK constants, …
- IF-088 scripts/pending <- scripts/dispatch: call pending.owner_cards -> PendingItem(kind, line) with kind blocked or spine; the pause kind excluded
