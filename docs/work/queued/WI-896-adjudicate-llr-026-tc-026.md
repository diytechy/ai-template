+++
id = "WI-896"
title = "adjudicate: LLR-026, TC-026 - approved/routed cell(s) amended on merged trunk 178aa4e..b059c8a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-026"]
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-026", "TC-026"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-026 `Detail`: 'Runs the agent CLI headless: build_argv substitutes {model} into argv and, when a CmdTemplate carries no {prompt} place…' -> 'Runs the agent CLI headless: build_argv substitutes {model} into argv and, when a CmdTemplate carries no {prompt} place…'
- LLR-026 `Rationale`: 'A large prompt passed as argv dies at the OS command-line cap (8191 characters through a Windows .CMD shim, 32767 via C…' -> 'A large prompt passed as argv dies at the OS command-line cap (8191 characters through a Windows .CMD shim, 32767 via C…'
- LLR-026 `SR-Refs`: 'SR-026' -> 'SR-026;SR-238'
- TC-026 `Expected`: 'Satisfies SR-026 AcceptanceCriteria' -> 'Satisfies SR-026 AcceptanceCriteria; the bounded descendants have ended when the coordinator continues, with no grace p…'
- TC-026 `Method`: 'Run the agent-loop suite; the dispatcher and its workers resume headless (registry + reservations + explicit assignment…' -> 'Run the agent-loop suite; the dispatcher and its workers resume headless (registry + reservations + explicit assignment…'
- TC-026 `Verifies`: 'SR-026;LLR-026' -> 'SR-026;SR-238;LLR-026'

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
- LLR-026 [project-trajectory/scripts/agent_session.py;project-trajectory/scripts/session_adapters.py :: build_argv/run_session/_codex_lastmsg_setup/_win32/_contain_in_job/_spawn_session/_end_launch/_end_suspended/_start_session_io/_feed_stdin/TreeNotEnded/_kill_tree/_end_job_tree/_end_group_tree/_terminate_job/_close_job/_open_job_members/_in_job/_close_handles/_job_active_processes/_job_survivors/_group_survivors/_await_tree_end] tests: (see TC-026) — Headless session launch
- LLR-061 [project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/agent_brief.py :: build_worker_assignment/worker_prompt/assignment_block] tests: (see TC-061) — Explicit WI/train/worktree worker assignment
- LLR-143 [project-trajectory/scripts/dispatch.py :: run] tests: (see TC-137) — Plain-launch drive loop (claim->build->integrate)
- TC-026 -> tests/test_agent_loop.py; tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild; tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild; tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs; tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises; tests/test_session_stdin.py::test_a_member_spawned_during_the_kill_has_ended_when_it_returns; tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise; tests/test_session_stdin.py::test_an_interruption_after_the_resume_ends_the_launching_child; tests/test_session_stdin.py::test_an_interruption_before_the_job_ends_the_suspended_child; tests/test_session_stdin.py::test_an_interruption_in_supervision_ends_the_child; tests/test_session_stdin.py::test_an_interrupted_launch_whose_tree_cannot_be_verified_raises; tests/test_session_stdin.py::test_a_launch_cleanup_that_cannot_terminate_raises; tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error; tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child
- TC-061 -> tests/test_agent_loop_worker.py
- TC-137 -> tests/test_dispatch.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/dispatch;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict;scripts/plan_coverage;scripts/review_brief: call parse_verdict: typed verdict findings, where a finding is a bullet whose bracket names one of the module's de…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-173 scripts/integrate <- scripts/dispatch;scripts/handback;scripts/lane: call claim, refresh, integrate, finished_branches, branch_outcomes, lane_worktree, the ACTIVE and WORK constants, …
- IF-088 scripts/pending <- scripts/dispatch: call pending.owner_cards -> PendingItem(kind, line) with kind blocked or spine; the pause kind excluded
