+++
id = "WI-952"
title = "adjudicate: LLR-019, LLR-020, LLR-140, LLR-300, SR-019, SR-020 - approved/routed cell(s) amended on merged trunk 5245ac8..08bbb71 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-019", "SR-020"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-019", "LLR-020", "LLR-140", "LLR-300", "SR-019", "SR-020"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-019 `AcceptanceCriteria`: 'The hook runs the registry-integrity floor and the secrets scan on staged content and blocks a commit that fails either…' -> 'The hook runs the registry-integrity floor and the secrets scan on staged content and blocks a commit that fails either…'
- SR-020 `AcceptanceCriteria`: 'The hook scans the push range and blocks when a secret (always) or an identity/PII class (privacy-check on) appears. Wi…' -> 'The hook scans the push range and blocks when a secret (always) or an identity/PII class (privacy-check on) appears. Wi…'
- LLR-019 `Detail`: 'Runs trace --strict-integrity and the check_privacy secrets scan on staged content and blocks a failing commit. Every b…' -> 'Runs trace --strict-integrity and the check_privacy secrets scan on staged content and blocks a failing commit. Every b…'
- LLR-020 `Detail`: 'Scans the outgoing commit range and blocks a push that would publish a secret or a private identity under privacy-check.' -> 'Scans the outgoing commit range and blocks a push that would publish a secret or a private identity under privacy-check…'
- LLR-140 `Detail`: 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…' -> 'claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock (the live dispatcher…'
- LLR-300 `Detail`: 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…' -> 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…'

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
- LLR-021 [project-trajectory/hooks/kit-python.sh :: kit_python] tests: (see TC-021) — Hook python probe
- TC-019 -> tests/test_pre_commit_hook.py; tests/test_commit_floor_census.py
- TC-020 -> tests/test_pre_push_hook.py
- TC-021 -> tests/test_pre_commit_hook.py::test_hook_refuses_clearly_when_no_working_python3; tests/test_pre_commit_hook.py::test_hook_never_runs_the_checks_on_an_older_python; tests/test_pre_commit_hook.py::test_hook_runs_on_the_project_venv_over_an_older_python; tests/test_pre_commit_hook.py::test_commit_msg_hook_fails_closed_when_no_python; tests/test_pre_commit_hook.py::test_commit_msg_hook_never_runs_on_an_older_python; tests/test_pre_commit_hook.py::test_every_hook_reads_the_one_interpreter_probe; tests/test_pre_push_hook.py::test_pre_push_never_runs_on_an_older_python; tests/test_run_devsetup.py::test_each_run_launcher_searches_what_its_dev_setup_searches[kit-python.sh:hooks]

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-040 scripts/check -> project-trajectory/hooks/pre-commit: exit-code 0 pass or SKIP · 1 any step FAILs
- IF-042 scripts/trace -> project-trajectory/hooks/pre-commit: exit-code 0 no integrity finding · 1 integrity finding
- IF-043 scripts/check_privacy -> project-trajectory/hooks/pre-push: exit-code 0 clean | 1 findings | 2 scan not performed
- IF-134 hooks/pre-commit -> external:git: exit-code exit 0 admits the commit; nonzero refuses it
- IF-135 hooks/pre-push -> external:git: exit-code exit 0 releases the push; nonzero refuses it
