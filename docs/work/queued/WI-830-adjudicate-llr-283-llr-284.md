+++
id = "WI-830"
title = "adjudicate: LLR-283, LLR-284, SR-225, TC-293, TC-294, TC-313 - approved/routed cell(s) amended on merged trunk c0caea0..a8458c2 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-225"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-283", "LLR-284", "SR-225", "TC-293", "TC-294", "TC-313"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-225 `AcceptanceCriteria`: 'With the dial off or undeclared, a closing lane is judged by nothing here and the close reads no record; with the dial …' -> 'With the dial off or undeclared, a closing lane owes no newly written delegated-run record and the close does not read …'
- SR-225 `Rationale`: 'A DERIVED requirement, and labelled so. SN-029 asks that a run released to automation get as far as it honestly can, an…' -> 'A DERIVED requirement, and labelled so. SN-029 asks that a run released to automation get as far as it honestly can, an…'
- SR-225 `Requirement`: 'Where the declared decision-recording dial asks for a record, the delivered loop content shall hold a delegated run to …' -> "The delivered loop content shall keep the owner's verdict on each delegated decision coupled to the work that acts on i…"
- LLR-283 `Detail`: 'kitlib/decisions.py imports nothing and reads no file, git or environment. record_path(run) is DECISIONS_DIR/<run>.toml…' -> 'kitlib/decisions.py imports nothing and reads no file, git or environment. record_path(run) is DECISIONS_DIR/<run>.toml…'
- LLR-283 `Title`: "The decisions record's path, format findings, obligation and session note" -> "The decisions record's owner verdict, format findings and session note"
- LLR-284 `Detail`: '_decision_record_refusal(root, branch, outcomes) is a rung of _merge_refusal, taken through _close_record_refusal direc…' -> '_decision_record_refusal(root, branch, outcomes) is a rung of _merge_refusal, taken through _close_record_refusal direc…'
- TC-293 `Expected`: 'Satisfies SR-225 AcceptanceCriteria: each shape, required-key, reviewed-value and hoist defect is reported by entry, ex…' -> 'Satisfies SR-225 AcceptanceCriteria: each shape, required-key, owner-verdict and hoist defect is reported by entry, ext…'
- TC-293 `Method`: 'The kitlib.decisions call surface over record texts planted in memory, clause by clause, and the owner surface over rec…' -> 'The kitlib.decisions call surface over record texts planted in memory, clause by clause, and the owner surface over rec…'
- TC-294 `Method`: 'A claimed lane in a temporary git repository, closed into a terminal folder, whose record file, when present, is commit…' -> 'A claimed lane in a temporary git repository, closed into a terminal folder, whose record file, when present, is commit…'
- TC-313 `Method`: 'Drive staged and committed ruling transitions over git repositories: with a row citing two pending items, ruling one wh…' -> 'Drive staged and committed ruling transitions over git repositories: with a row citing two pending items, ruling one wh…'

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
- LLR-283 [project-trajectory/scripts/kitlib/decisions.py;project-trajectory/scripts/gen_open_items.py;project-trajectory/scripts/pending.py :: DECISIONS_DIR/MODES/REQUIRED_KEYS/OWNER_KEY/CONFIRMED/OVERRULED/OWNER_VALUES/RETIRED_KEY/_RUN_EXCLUDED/record_path/record_findings/owner_state/_owner_findings/_entries/review_queue/citation/citations/newly_overruled/owed/missing_record_refusal/session_note/_decision_card/_citing_field/OVERRULED_HEADING/decisions_block/decisions_to_review/citing_rows] tests: (see TC-293) — The decisions record's owner verdict, format findings and s…
- LLR-284 [project-trajectory/scripts/integrate.py :: _decision_record_refusal/_close_record_refusal] tests: (see TC-294) — The merge slot refuses a close that owes its decisions reco…
- LLR-303 [project-trajectory/scripts/kitlib/decisions.py;project-trajectory/scripts/kitlib/git.py :: git_paths/git_show/UnreadableBlob/_shown/_open_spec/_owed_overrules/overrule_sync_lines] tests: TC-319 — Commit-local overrule-to-work synchronization
- LLR-304 [project-trajectory/scripts/kitlib/decisions.py;project-trajectory/scripts/migrate_decisions.py :: _retired_verdict/_verdict_action/_string_end/_statements/_comment_start/_migrated_statement/_expected_parse/_same/_checked/migrate_text/_migrate_one/main] tests: TC-320 — Delegated-decisions retired-verdict migration
- TC-292 -> tests/test_decision_record.py::test_each_declared_value_reads_as_itself; tests/test_decision_record.py::test_an_undeclared_dial_reads_off; tests/test_decision_record.py::test_an_unrecognized_value_is_refused_and_read_as_record; tests/test_decision_record.py::test_a_padded_or_mixed_case_value_is_accepted_as_the_reader_reads_it; tests/test_decision_record.py::test_the_reader_and_the_validator_share_one_normalization; tests/test_decision_record.py::test_a_wrong_typed_value_is_refused; tests/test_decision_record.py::test_the_template_ships_off_and_this_repo_records

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-055 scripts/schedule <- scripts/integrate: call frontier over the loaded rows, in deterministic order
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
