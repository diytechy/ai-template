+++
id = "WI-984"
title = "adjudicate: LLR-031, LLR-155, LLR-156, SN-028, SR-031, SR-137, TC-031, TC-150, TC-152 - approved/routed cell(s) amended on merged trunk 827adec..2aaf9f6 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-031", "SR-137"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-031", "LLR-155", "LLR-156", "SN-028", "SR-031", "SR-137", "TC-031", "TC-150", "TC-152"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-031 `AcceptanceCriteria`: "Every enforcer reads the same value for the same dial through one parse; the hooks' and the checkers' answers agree ove…" -> 'Every enforcer reads the same value for the same dial from one TOML parse, including a dotted key, an inline table and …'
- SR-031 `Coincident`: 'The need asks for every policy dial in one hand-edited, machine-read file whose shape is a checked contract because two…' -> 'The need asks for every policy dial in one hand-edited, machine-read file. Every enforcer reading the same value from i…'
- SR-031 `Rationale`: 'Realizes SN-028 (every policy dial in one home, a single hand-edited, machine-read file, whose two readings are pinned …' -> "Realizes SN-028's one readable policy home. A policy answer calculated more than once can diverge across enforcers, lea…"
- SR-137 `AcceptanceCriteria`: 'A dial declared in both homes produces a refusal naming the key and both files, at every guarded entry point (the dispa…' -> 'A dial declared in both homes produces a refusal naming the key and both homes at every guarded entry point; a wrong-ty…'
- SR-137 `Rationale`: 'Two grammars read this file — `tomllib` in Python and the three git hooks in pure sh, so a Python-less box still fails …' -> 'A single declaration home gives the owner one place to inspect and change each dial. A duplicate declaration can give e…'
- SR-137 `Requirement`: 'The kit shall read every process policy dial from a single policy declaration home whose line shape is a checked contra…' -> 'The kit shall read every process policy dial from a single policy declaration home and refuse a duplicate declaration o…'
- SR-137 `Title`: 'One policy home, with a checked shape' -> 'One policy home with conflict and validity refusal'
- LLR-031 `Detail`: 'The single first-non-comment-line reader the hooks, agent_loop.read_declared, and check_privacy all use so a declared p…' -> 'All policy enforcers, including the agent layer, obtain a declared policy answer from one parsed representation. A priv…'
- LLR-031 `Title`: 'Shared declared-line parse' -> 'Shared declared-policy parse'
- LLR-155 `Detail`: '`process_config` parses `docs/process.toml` once; `declared_policy` reads a dial through it with the legacy file as fal…' -> 'The configuration layer parses the policy declaration once, reads a dial from that parse with its legacy declaration as…'
- LLR-155 `Rationale`: 'Five entry points read policy without passing through `agent_loop.main`, so the refusal has to live where the value is …' -> 'The policy values serve several entry points, so their validation and comparison need one home. A duplicate or invalid …'
- LLR-155 `Title`: 'The config layer: one reader, checked shape, one comparison' -> 'The config layer: one parse, declaration checks, one comparison'
- LLR-156 `Detail`: '`set_process_key` answers THREE states (`wrote`/`unchanged`/`missing`) and the write decides the delete; `add_if_missin…' -> '`set_process_key` retains an in-place edit only when the TOML parse of the edited text equals the old parse with exactl…'
- TC-031 `Method`: "Drive each shipped commit and push hook over the adversarial file-shape table and compare its answer with the checker's…" -> 'Drive each shipped commit and push hook and the checker with a policy file containing a dotted key, an inline table, an…'
- TC-150 `Method`: "Run the process-config suite: it sources the SHIPPED hook's own sh functions and drives them against `tomllib` over a t…" -> 'Run the process-config suite over a duplicated declaration, wrong-typed dials and out-of-range dials, valid policy file…'
- TC-152 `Method`: 'Run the migration cases in the process-config suite: a full conversion deletes every legacy file and lands all three ap…' -> 'Run the migration and bootstrap writer cases: a full conversion deletes every legacy file and lands all three approval …'
- SN-028 `Acceptance`: 'A single declared process-dial file holds every process dial under **bare `[section]` headers**, one `key = value` per …' -> "A single declared process-dial file holds every process dial. Every reader obtains its policy answer from the file's TO…"
- SN-028 `Why`: 'The dials had accreted into ~10 one-word files under `docs/`, an idiom that was never ruled: it was held in place by th…' -> 'The dials had accreted into ~10 one-word files under `docs/`, an idiom that was never ruled. Scattering costs an owner …'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-021 [project-trajectory/hooks/kit-python.sh :: kit_python;kit_policy] tests: (see TC-021) — Hook python probe
- LLR-031 [project-trajectory/scripts/check_privacy.py;project-trajectory/scripts/kitlib/config.py :: _first_declared_line;_load_process_toml;read_privacy_review;hook_policy_answer;policy_declaration] tests: (see TC-031) — Shared declared-policy parse
- LLR-155 [project-trajectory/scripts/agent_policy.py;project-trajectory/scripts/bootstrap.py :: process_config/config_conflicts/approval_through/human_holds;_migrate_dial_key_name] tests: TC-150;TC-151 — The config layer: one parse, declaration checks, one compar…
- TC-021 -> tests/test_pre_commit_hook.py::test_hook_refuses_clearly_when_no_working_python3; tests/test_pre_commit_hook.py::test_hook_never_runs_the_checks_on_an_older_python; tests/test_pre_commit_hook.py::test_hook_runs_on_the_project_venv_over_an_older_python; tests/test_pre_commit_hook.py::test_commit_msg_hook_fails_closed_when_no_python; tests/test_pre_commit_hook.py::test_commit_msg_hook_never_runs_on_an_older_python; tests/test_pre_commit_hook.py::test_every_hook_reads_the_one_interpreter_probe; tests/test_pre_commit_hook.py::test_every_hook_refuses_a_kit_scripts_dir_naming_a_missing_directory; tests/test_pre_push_hook.py::test_pre_push_never_runs_on_an_older_python; tests/test_pre_push_hook.py::test_pre_push_refuses_a_kit_scripts_dir_naming_a_missing_directory; tests/test_process_config.py::test_every_hook_refuses_an_unreadable_policy_file; tests/test_process_config.py::test_every_hook_refuses_a_mixed_config_with_one_text; tests/test_process_config.py::test_every_hook_refuses_a_failed_or_foreign_policy_answer; tests/test_process_config.py::test_the_mixed_refusal_runs_after_the_interpreter_probe; tests/test_shell_portability.py::test_each_hook_runs_the_one_read_once_after_the_probe; tests/test_run_devsetup.py::test_each_run_launcher_searches_what_its_dev_setup_searches[kit-python.sh:hooks]; tests/test_bootstrap.py::test_a_fresh_scaffold_ships_the_probe_and_commits_through_its_hooks
- TC-031 -> tests/test_process_config.py::test_valid_toml_policy_shapes_reach_every_reader; tests/test_process_config.py::test_a_privacy_key_under_another_table_fails_closed_in_every_reader; tests/test_process_config.py::test_an_unreadable_policy_file_is_refused; tests/test_process_config.py::test_every_hook_refuses_an_unreadable_policy_file; tests/test_process_config.py::test_a_mixed_config_is_refused_by_name; tests/test_process_config.py::test_every_hook_refuses_a_mixed_config_with_one_text; tests/test_gate_policy.py; tests/test_push_policy.py; tests/test_pre_push_hook.py::test_the_review_posture_follows_the_one_parse; tests/test_shell_portability.py::test_no_hook_reads_the_policy_as_text
- TC-150 -> tests/test_process_config.py::test_a_mixed_config_is_refused_by_name; tests/test_process_config.py::test_a_wrong_typed_dial_is_refused_not_defaulted; tests/test_process_config.py::test_an_out_of_range_dial_is_refused_not_defaulted; tests/test_approval_level.py::test_a_malformed_dial_is_REFUSED_not_silently_defaulted; tests/test_process_config.py::test_every_guarded_entry_point_refuses_a_mixed_config; tests/test_process_config.py::test_valid_toml_policy_shapes_cause_no_configuration_refusal; tests/test_bootstrap.py::test_the_dial_key_rename_refuses_an_old_key_held_in_an_inline_table

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-014 scripts/bootstrap -> external:downstream adopter: bytes the scaffolded template tree written under the destination root
- IF-035 project-trajectory/skills/ -> scripts/gen_skills_index;scripts/bootstrap: file SKILL.md frontmatter: name, scope, stacks, domains, phases, tags; each other file in the skill directory, mat…
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file TOML tables: attestation, policies, checks, build; a privacy gate key outside [policies] reads as gate on, an…
- IF-039 registries -> scripts/bootstrap: bytes one template file per registry tier
- IF-262 scripts/kitlib/bootstrap_manifest <- scripts/bootstrap: call MAPPING and mapping_entries: the ordered scaffold source, destination, and optional requirement-reference inv…
