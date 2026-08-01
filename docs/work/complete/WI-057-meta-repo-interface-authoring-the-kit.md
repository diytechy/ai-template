+++
id = "WI-057"
title = "Meta-repo interface authoring - the kit's own seams"
workstream = "self-adoption"
needs = ["WI-056"]
order = 56
+++

## Deliverable

S6 (2026-07-11): authored docs/requirements/interfaces.csv - 43 IF-### seams describing the kit's real architecture (20 Provides-CLI rows, one per arch-map script; 19 file-mediated Consumes rows over the shared-contract hubs docs/stack.ini / docs/architecture.md / docs/requirements/work-items.csv / the spine registries / docs/status.md; 4 subprocess/external seams - pre-commit->check + pre-commit->trace + pre-push->check_privacy + agent_loop->agent CLI). Every one of the 20 modules is now a declared IF endpoint with a Provides and a Consumes seam (scripts/gen_cases marked a deliberate source via its Notes valve). Contracts: IF-### docstring lines added to all 20 scripts and harvested into architecture.md's MODULE MAP. Regenerated arch-map + root PROJECT_STATE.html (the How-SW panel now renders the 43-edge module/file/external graph, check.py the central sink) + docs/okf (now emits IF concepts). check_trajectory connectivity coverage = 0 warns (the connectivity-undeclared driver resolved); trace --strict interfaces=43 interface-findings=0, 0 endpoint advisories. All seams Status=Stable (pinned shipped contracts), so the Active-seam-TC rule is vacuously satisfied - see docs/log.md 2026-07-11 for the reasoning + the surfaced trace/check_trajectory Verifies-column tension. Data + docstrings only, no kit-script behavior change; nothing new rides the re-attestation beyond S5's chain.
