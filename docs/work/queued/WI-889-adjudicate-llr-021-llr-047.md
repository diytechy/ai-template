+++
id = "WI-889"
title = "adjudicate: LLR-021, LLR-047, LLR-322, SR-019, SR-020, SR-032, SR-046, TC-021, TC-047, TC-345 - approved/routed cell(s) amended on merged trunk 8d75bc6..945245e (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-019", "SR-020", "SR-032", "SR-046"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-021", "LLR-047", "LLR-322", "SR-019", "SR-020", "SR-032", "SR-046", "TC-021", "TC-047", "TC-345"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-019 `AcceptanceCriteria`: 'The hook runs the registry-integrity floor and the secrets scan on staged content and blocks a commit that fails either…' -> 'The hook runs the registry-integrity floor and the secrets scan on staged content and blocks a commit that fails either…'
- SR-020 `AcceptanceCriteria`: 'The hook scans the push range and blocks when a secret (always) or an identity/PII class (privacy-check on) appears.' -> 'The hook scans the push range and blocks when a secret (always) or an identity/PII class (privacy-check on) appears. Wi…'
- SR-020 `Rationale`: 'Realizes SN-005 and SN-009 — the last gate before content leaves the machine. Parents the interpreter probe, with SR-01…' -> 'Realizes SN-005 and SN-009 — the last gate before content leaves the machine. Parents the interpreter probe, with SR-01…'
- SR-032 `AcceptanceCriteria`: 'The scaffolded onboard/dev-setup scripts run to a green setup.' -> "The scaffolded onboard/dev-setup scripts run to a green setup. When this repository's Windows developer setup has no in…"
- SR-046 `AcceptanceCriteria`: 'A machine listing prints one name-and-description line per declared capability in declaration order; a direct call nami…' -> 'A machine listing prints one name-and-description line per declared capability in declaration order; a direct call nami…'
- LLR-021 `Detail`: 'Probes candidate interpreters by RUNNING one — never by testing for the name on PATH, which a Windows Store alias satis…' -> 'kit_python is the one interpreter probe sourced by pre-commit, commit-msg and pre-push. It runs the two project virtual…'
- LLR-047 `Detail`: 'load_capabilities parses the docs/stack.ini [run] section (configparser, interpolation=None, case-preserving optionxfor…' -> 'load_capabilities parses the docs/stack.ini [run] section (configparser, interpolation=None, case-preserving optionxfor…'
- LLR-322 `Detail`: 'When the shipped coordinator-hook example declares guard hooks and the machine-local settings leave them off, an intera…' -> 'When the shipped coordinator-hook example declares guard hooks and the machine-local settings leave them off, an intera…'
- TC-021 `Expected`: 'Satisfies SR-019 and SR-020 AcceptanceCriteria via the LLR-021 interpreter-probe detail contract' -> 'Each hook refuses without a traceback, names the developer-setup install step and the 3.11 floor, and runs neither its …'
- TC-021 `Method`: "Run the hook suites' python-probe cases; a missing/aliased python3 reports clearly without crashing." -> 'Drive pre-commit, commit-msg and pre-push with non-runnable python3/python stand-ins and, where installed, a real pre-3…'
- TC-047 `Expected`: 'Satisfies SR-046 AcceptanceCriteria' -> 'Satisfies SR-046 AcceptanceCriteria. A declared bare-python capability runs on the menu interpreter rather than the fir…'
- TC-047 `Method`: 'Run the run-menu suite: --list prints name<TAB>desc for each declared capability in declaration order (an empty desc re…' -> 'Run the run-menu suite: --list prints name<TAB>desc for each declared capability in declaration order (an empty desc re…'
- TC-345 `Expected`: "Consent enables the coordinator hooks in the machine-local settings, bound to the opt-in's interpreter, replacing only …" -> "Consent enables the coordinator hooks in the machine-local settings, bound to the opt-in's interpreter, replacing only …"
- TC-345 `Method`: 'Decline and accept the interactive coordinator-hook offer with existing settings, and run the hook command against exam…' -> 'Decline and accept the interactive coordinator-hook offer with existing settings, and run the hook command against exam…'

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
- LLR-032 [project-trajectory/scripts/onboard.template.sh :: onboard/dev-setup] tests: (see TC-032) — Onboard/dev-setup templates
- LLR-047 [project-trajectory/scripts/run_menu.py;project-trajectory/scripts/run.template.sh;project-trajectory/scripts/run.template.cmd;project-trajectory/scripts/run.template.command :: load_capabilities/interactive_menu/direct/launch/_interpreter_dir/write_interpreter_shims] tests: (see TC-047; TC-342) — Run capability menu reader
- LLR-320 [project-trajectory/scripts/dev-setup.template.sh;project-trajectory/scripts/dev-setup.template.ps1;project-trajectory/scripts/dev-setup.template.cmd;project-trajectory/scripts/dev-setup.template.command :: detect_runtime/interactive/maybe_install;FindPython/Interactive/MaybeInstall] tests: TC-343 — Dev-setup readiness operation for a bare run

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-040 scripts/check -> project-trajectory/hooks/pre-commit: exit-code 0 pass or SKIP · 1 any step FAILs
- IF-042 scripts/trace -> project-trajectory/hooks/pre-commit: exit-code 0 no integrity finding · 1 integrity finding
- IF-043 scripts/check_privacy -> project-trajectory/hooks/pre-push: exit-code 0 clean | 1 findings | 2 scan not performed
- IF-134 hooks/pre-commit -> external:git: exit-code exit 0 admits the commit; nonzero refuses it
- IF-135 hooks/pre-push -> external:git: exit-code exit 0 releases the push; nonzero refuses it
