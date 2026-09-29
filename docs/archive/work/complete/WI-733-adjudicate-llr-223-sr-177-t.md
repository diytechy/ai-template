+++
id = "WI-733"
title = "adjudicate: LLR-223, SR-177, TC-267 - approved/routed cell(s) amended on merged trunk 69902bc..03debc7 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-177"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-222", "LLR-223", "LLR-286", "SR-177", "SR-193", "TC-267"]
+++

## Deliverable

`VERDICT: MEANING rows=6`, from spine-acts batch I, act seq 11. An independent
Opus adjudicator ruled it. The verdict is
[001-ADJUDICATE-22e7b24.md](../../../reviews/wi-733-adjudicate-llr-223-sr-177-t/001-ADJUDICATE-22e7b24.md).

- **Re-attested and anchored:**
  - SR-177 and SR-193 (CLARITY);
  - LLR-222, LLR-223, LLR-286 and TC-267 (MEANING).

  This includes the batch G and H carry-over.
- **Recorded, not drafted:** WI-735's observations 3 and 4.
  - LLR-223 is silent on a failed, never-classified row. The check already
    fails, naming the row.
  - SR-177's acceptance ends in "the row's stated build gap". Whoever builds
    the aggregation must amend its acceptance and rationale together.

## Context

Carry-over added 2026-09-29 by the coordinator, from spine-acts batches G and H. LLR-222 and LLR-286 were blessed as MEANING in both batches, and SR-193 as CLARITY in batch H, but none could be anchored: the LLR snapshot was blocked by LLR-223 and the SR snapshot by SR-177, and WI-732 has now answered both. They are added to `adjudicates` so this brief shows them. Re-attest them in this act with this row's own amendments.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-177 `Rationale`: 'The charter refuses a declared budget with no measurement behind it: fan-out is complex machinery justified by a throug…' -> 'The charter refuses a declared budget with no measurement behind it: fan-out is complex machinery justified by a throug…'
- LLR-223 `Detail`: 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty Delivered-With with one or more decl…' -> 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty Delivered-With with one or more decl…'
- TC-267 `Method`: 'With the dial on, over the recorded fixtures (claude LIVE; codex and opencode NOT LIVE, built from documented event sha…' -> 'With the dial on, over the recorded fixtures (claude LIVE; codex and opencode NOT LIVE, built from documented event sha…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-196 [project-trajectory/scripts/agent_common.py :: regenerate_index/per_turn_pace/per_turn_context] tests: (see TC-191) — Per-session fan-out utilisation telemetry, unaggregated
- TC-191 -> tests/test_generated_newlines.py::test_the_three_crash_paths_actually_run; tests/test_agent_loop.py::test_done_exit_writes_logs_and_index; tests/test_agent_loop.py::test_stream_json_echo_and_result_parse

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
- IF-179 scripts/agent_common <- scripts/gen_verdict_rollup: call git(root, *argv) -> (code, out); trunk_name(root) -> the primary checkout's branch
