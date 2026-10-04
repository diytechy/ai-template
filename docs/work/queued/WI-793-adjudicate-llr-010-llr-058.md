+++
id = "WI-793"
title = "adjudicate: LLR-010, LLR-058, LLR-118, LLR-153, LLR-283, LLR-288, SR-225, TC-010, TC-123, TC-147, TC-293, TC-301 - approved/routed cell(s) amended on merged trunk 25b9f57..5be0bc4 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-225"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-010", "LLR-058", "LLR-118", "LLR-153", "LLR-283", "LLR-288", "SR-225", "TC-010", "TC-123", "TC-147", "TC-293", "TC-301"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-225 `AcceptanceCriteria`: 'With the dial off or undeclared, a lane is judged by nothing here and no record is read; with the dial at record or esc…' -> 'With the dial off or undeclared, a closing lane is judged by nothing here and the close reads no record; with the dial …'
- SR-225 `Rationale`: 'A DERIVED requirement, and labelled so. SN-029 asks that a run released to automation get as far as it honestly can, an…' -> 'A DERIVED requirement, and labelled so. SN-029 asks that a run released to automation get as far as it honestly can, an…'
- SR-225 `Requirement`: 'Where the declared decision-recording dial asks for a record, the delivered loop content shall judge a closing lane aga…' -> 'Where the declared decision-recording dial asks for a record, the delivered loop content shall hold a delegated run to …'
- LLR-010 `Detail`: 'Writes the mapped kit files into --dest so the generated harness runs green out of the box.' -> 'Writes the mapped kit files into --dest so the generated harness runs green out of the box. For a non-Python profile, a…'
- LLR-058 `Detail`: 'Derives the dependency-ready frontier from the WI registry + dispatcher reservations (never prose), excludes terminally…' -> 'Derives the dependency-ready frontier from the WI registry, the states of the open items its rows cite and the dispatch…'
- LLR-118 `Detail`: 'The RENDERED half of the Modified/Draft attestation regime whose gate SR-049 derives. gen_open_items renders (a) every …' -> 'The rendered half of the attestation regime under SR-049. The page renders, in this order: the pending open items that …'
- LLR-153 `Detail`: 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…' -> 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…'
- LLR-283 `Detail`: 'A kitlib module importing nothing, whose functions read no file, git or environment. record_path(run) is DECISIONS_DIR/…' -> 'kitlib/decisions.py imports nothing and reads no file, git or environment. record_path(run) is DECISIONS_DIR/<run>.toml…'
- LLR-288 `Detail`: 'Load IF-073 gates into internal scheduler data. The shared readiness predicate refuses a queued gated row, including mu…' -> 'Attach to each work row the id and title of every open item its needs cite. The shared readiness predicate, which mutex…'
- TC-010 `Method`: "Run the bootstrap suite; a fresh scaffold's harness runs green." -> "Run the bootstrap suite; a fresh scaffold's harness runs green, including a node scaffold whose pending toolchain open …"
- TC-123 `Method`: 'Drive gen_open_items over temp repos: assert a pending registry row renders as a brief and a RULED row does not; that D…' -> 'Drive gen_open_items over temp repos: assert a pending registry row a queued work item cites renders as a brief beside …'
- TC-147 `Method`: "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…" -> "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…"
- TC-293 `Expected`: 'Satisfies SR-225 AcceptanceCriteria: each shape, required-key and hoist defect is reported by entry, extra keys are not…' -> 'Satisfies SR-225 AcceptanceCriteria: each shape, required-key, reviewed-value and hoist defect is reported by entry, ex…'
- TC-293 `Method`: 'The kitlib.decisions call surface over record texts planted in memory, clause by clause. (a) SOUND: a record with two c…' -> 'The kitlib.decisions call surface over record texts planted in memory, clause by clause, and the owner surface over rec…'
- TC-301 `Method`: "On a temporary spec registry, hold a queued row through a pending open item's wi_refs, verify the frontier and simulati…" -> 'On a temporary work registry, hold a queued row through a needs open-item edge while the item is pending: the frontier …'

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
- LLR-282 [project-trajectory/scripts/agent_policy.py :: decision_recording/DECISION_RECORDING_MODES/mode_word] tests: (see TC-292) — The decision_recording dial reads off when undeclared and r…
- LLR-283 [project-trajectory/scripts/kitlib/decisions.py;project-trajectory/scripts/gen_open_items.py;project-trajectory/scripts/pending.py :: DECISIONS_DIR/MODES/REQUIRED_KEYS/REVIEWED_KEY/REVIEWED_TRUE/REVIEWED_FALSE/record_path/record_findings/reviewed_state/review_queue/owed/session_note/_decision_card/decisions_block/decisions_to_review] tests: (see TC-293) — The decisions record's path, format findings, obligation an…
- LLR-284 [project-trajectory/scripts/integrate.py :: _decision_record_refusal/_close_record_refusal] tests: (see TC-294) — The merge slot refuses a close that owes its decisions reco…
- TC-292 -> tests/test_decision_record.py::test_each_declared_value_reads_as_itself; tests/test_decision_record.py::test_an_undeclared_dial_reads_off; tests/test_decision_record.py::test_an_unrecognized_value_is_refused_and_read_as_record; tests/test_decision_record.py::test_a_padded_or_mixed_case_value_is_accepted_as_the_reader_reads_it; tests/test_decision_record.py::test_the_reader_and_the_validator_share_one_normalization; tests/test_decision_record.py::test_a_wrong_typed_value_is_refused; tests/test_decision_record.py::test_the_template_ships_off_and_this_repo_records
- TC-293 -> tests/test_decision_record.py; tests/test_decisions_to_review.py::test_a_malformed_hoist_is_shown_as_a_finding_not_a_crash; tests/test_decisions_to_review.py
- TC-294 -> tests/test_decision_record_merge.py::test_a_recording_dial_refuses_a_close_without_its_record; tests/test_decision_record_merge.py::test_the_off_dial_reads_nothing; tests/test_decision_record_merge.py::test_a_lane_carrying_its_record_passes_the_rung; tests/test_decision_record_merge.py::test_a_malformed_entry_is_reported_and_does_not_refuse; tests/test_decision_record_merge.py::test_a_partial_close_without_its_record_is_refused_too; tests/test_decision_record_merge.py::test_a_partial_close_carrying_its_record_passes_the_rung; tests/test_decision_record_merge.py::test_a_dial_typo_is_refused_as_configuration_before_any_record; tests/test_decision_record_merge.py::test_a_padded_or_mixed_case_dial_reads_as_its_word

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-055 scripts/schedule <- scripts/integrate: call frontier over the loaded rows, in deterministic order
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
