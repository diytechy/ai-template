+++
id = "WI-965"
title = "adjudicate: LLR-021, LLR-031, SR-031, TC-021, TC-031 - approved/routed cell(s) amended on merged trunk ddb924a..141657b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-019", "SR-020", "SR-031"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-021", "LLR-031", "SR-031", "TC-021", "TC-031"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-962's in-lane sitting
`docs/reviews/wi-962/003-ADJUDICATE-b11fab7.md` blessed all five rows as
MEANING+BLESS, and the lane's act turn took act seq 144. At the landing
141657bb0 the system, low-level and test registries are byte-equal to
their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-031 `AcceptanceCriteria`: 'Every enforcer reads the same value for the same dial; the two delivered reader grammars return the same answer over th…' -> "Every enforcer reads the same value for the same dial through one parse; the hooks' and the checkers' answers agree ove…"
- SR-031 `Coincident`: 'The need asks for every policy dial in one hand-edited, machine-read file whose shape is a checked contract because two…' -> 'The need asks for every policy dial in one hand-edited, machine-read file whose shape is a checked contract because two…'
- LLR-021 `Detail`: 'kit_python is the one interpreter probe sourced by pre-commit, commit-msg and pre-push. It runs the two project virtual…' -> 'kit_python is the one interpreter probe sourced by pre-commit, commit-msg and pre-push. It runs the two project virtual…'
- LLR-021 `SR-Refs`: 'SR-019;SR-020' -> 'SR-019;SR-020;SR-031'
- LLR-031 `Detail`: 'The single first-non-comment-line reader the hooks, agent_loop.read_declared, and check_privacy all use so a declared p…' -> 'The single first-non-comment-line reader the hooks, agent_loop.read_declared, and check_privacy all use so a declared p…'
- TC-021 `Expected`: 'Each hook refuses without a traceback, names the developer-setup install step and the 3.11 floor, and runs neither its …' -> 'Each hook refuses without a traceback, names the developer-setup install step and the 3.11 floor, and runs neither its …'
- TC-021 `Method`: 'Drive pre-commit, commit-msg and pre-push with non-runnable python3/python stand-ins and, where installed, a real pre-3…' -> 'Drive pre-commit, commit-msg and pre-push with non-runnable python3/python stand-ins and, where installed, a real pre-3…'
- TC-021 `Verifies`: 'SR-019;SR-020;LLR-021' -> 'SR-019;SR-020;LLR-021;IF-298'
- TC-031 `Method`: "Run the process-config and policy suites: every enforcer reads one value per dial from docs/process.toml, the hooks' sh…" -> "Drive each shipped commit and push hook over the adversarial file-shape table and compare its answer with the checker's…"
- TC-031 `Verifies`: 'SR-031;LLR-031' -> 'SR-031;LLR-031;IF-037'

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
- LLR-019 [project-trajectory/hooks/pre-commit :: pre-commit] tests: (see TC-019) — Pre-commit floor
- LLR-020 [project-trajectory/hooks/pre-push :: pre-push] tests: (see TC-020) — Pre-push outgoing scan
- LLR-021 [project-trajectory/hooks/kit-python.sh :: kit_python;kit_policy] tests: (see TC-021) — Hook python probe
- LLR-031 [project-trajectory/scripts/check_privacy.py :: _first_declared_line;_load_process_toml;_policies;read_privacy_review;hook_policy_answer] tests: (see TC-031) — Shared declared-line parse
- TC-019 -> tests/test_pre_commit_hook.py; tests/test_commit_floor_census.py
- TC-020 -> tests/test_pre_push_hook.py

### Interface seams via the touched modules
- IF-005 scripts/check_privacy -> scripts/check: stdout one line per leak: <location>: [<label>] <excerpt>, then one summary line naming the scan and the armed layers
- IF-148 scripts/check_privacy -> scripts/check: exit-code 0 clean or both layers off · 1 one or more findings in the tracked-file sweep
- IF-032 external:git -> scripts/check_privacy: git staged diff, commit message, outgoing range
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-040 scripts/check -> project-trajectory/hooks/pre-commit: exit-code 0 pass or SKIP · 1 any step FAILs
- IF-042 scripts/trace -> project-trajectory/hooks/pre-commit: exit-code 0 no integrity finding · 1 integrity finding
