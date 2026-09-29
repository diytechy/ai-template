+++
id = "WI-730"
title = "adjudicate: LLR-222, LLR-223, SR-177, SR-193, TC-220 - approved/routed cell(s) amended on merged trunk a20b496..17c54c2 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-177", "SR-193"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-222", "LLR-223", "LLR-286", "SR-177", "SR-193", "TC-220", "TC-222"]
+++

## Deliverable

`VERDICT: MEANING rows=7`, from spine-acts batch H, act seq 10. An independent
Opus adjudicator ruled it. The verdict is
[001-ADJUDICATE-3e8a87d.md](../../../reviews/wi-730-adjudicate-llr-222-llr-223/001-ADJUDICATE-3e8a87d.md).

- **Re-attested and anchored:** TC-220 and TC-222.
- **Blessed but not anchored:** SR-193 (CLARITY), LLR-222 and LLR-286. The
  SR and LLR registries could not be copied.
- **Not blessed:**
  - SR-177: its rationale states an aggregation obligation wider than its
    acceptance;
  - LLR-223: its contradiction sentence covers any Delivered-With beside a
    waiver, where SR-193, TC-220 and the code report it only for a joint row.

  These two block the SR and LLR snapshots. Both are carried in WI-731's
  Dispositions draft.

## Context

Carry-over added 2026-09-29 by the coordinator, from spine-acts batch G (WI-724/WI-726/WI-728, act seq 9). TC-222 and LLR-286 were blessed in batch G (MEANING) but could not be anchored, because the LLR and TC snapshot was refused while LLR-223 and TC-220 drifted. They are added to `adjudicates` so this brief shows them. LLR-222 was already in scope. Re-attest them in this act together with this row's own amendments once the snapshot can take the LLR and TC registries.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-177 `Rationale`: "The charter refuses a declared budget with no measurement behind it, and SN-027 is that finding inverted — the system's…" -> 'The charter refuses a declared budget with no measurement behind it: fan-out is complex machinery justified by a throug…'
- SR-193 `Rationale`: 'An empty cell asserts nothing, so a requirement citing no assumption cannot be read as one that needs none: the absence…' -> 'An empty cell asserts nothing, so a requirement citing no assumption cannot be read as one that needs none: the absence…'
- LLR-222 `Title`: "The requirement's assumption citations and coincident waiver: schema, carrier and template" -> "The requirement's assumption citations, joint-delivery siblings and coincident waiver: schema, carrier and template"
- LLR-223 `Detail`: 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty Delivered-With whose entries are dec…' -> 'sr_classification_advisories(srs, das) returns (failures, advisories). A non-empty Delivered-With with one or more decl…'
- TC-220 `Expected`: "Satisfies SR-193's acceptance: bridged, joint, coincident, unclassified and contradictory combinations classified as st…" -> "Satisfies SR-193's acceptance: bridged, joint, coincident, unclassified and contradictory combinations classified as st…"
- TC-220 `Method`: 'sr_classification_advisories and da_citing_srs called on in-memory rows. A requirement citing declared assumptions is b…' -> 'sr_classification_advisories and da_citing_srs called on in-memory rows. A requirement citing declared assumptions is b…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-196 [project-trajectory/scripts/agent_common.py :: regenerate_index/per_turn_pace/per_turn_context] tests: (see TC-191) — Per-session fan-out utilisation telemetry, unaggregated
- LLR-222 [project-trajectory/scripts/kitlib/spine.py;project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/migrate_carrier.py;project-trajectory/scripts/acceptance_record.py;project-trajectory/registries/system-requirements.template.toml :: SPINE_TIER_KEYS/SPINE_COLUMN/KEY/SPINE_APPROVED_CELLS] tests: - — The requirement's assumption citations, joint-delivery sibl…
- LLR-223 [project-trajectory/scripts/assumption_rules.py :: SR_CLASSES/sr_classification_advisories/da_citing_srs] tests: - — The requirement classification advisories
- LLR-225 [project-trajectory/scripts/acceptance_record.py :: SPINE_TRACED_CELLS/SPINE_APPROVED_CELLS/OFFSPINE_TRACED_CELLS] tests: - — Each new cell's class: traced or approved content
- TC-191 -> tests/test_generated_newlines.py::test_the_three_crash_paths_actually_run; tests/test_agent_loop.py::test_done_exit_writes_logs_and_index; tests/test_agent_loop.py::test_stream_json_echo_and_result_parse
- TC-220 -> tests/test_assumption_rules.py

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
