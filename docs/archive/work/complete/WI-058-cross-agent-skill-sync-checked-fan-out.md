+++
id = "WI-058"
title = "Cross-agent skill sync - checked fan-out from one source"
workstream = "scripts"
sr_refs = ["SR-112"]
needs = ["WI-010", "WI-019"]
order = 57
+++

## Deliverable

Cross-agent skill fan-out made a checked, one-command-refreshable copy of the one neutral source: .agents/skills added as a first-class bootstrap target (--agents codex, AGENTS dict entry + optional hooks); bootstrap --sync force-refreshes only each existing per-agent skills subtree; gen_skills_index --check-agents byte-identity drift gate wired into the pre-commit floor + a G3 skills-sync check.py step (kit-only generator, vacuous downstream); SR-025 extended to the checked fan-out with LLR-043/TC-045; PROCESS_OPTIONS/skills-README/ADOPTING tenability + re-sync notes; meta drift resolved (source session-protocol advanced to --stale so .claude/.agents are byte-identical to source). Rides the pending G3 re-attestation.
