+++
id = "WI-195"
title = "Redacted brief assembler + hat prompt-map keys - allowlist-only planner/critic/arbiter brief assembly on the AGENT_PROMPT_MAP override (DP-001 selected plan P2)"
workstream = "unattended"
needs = ["WI-190"]
buildtier = "medium"
order = 191
+++

## Deliverable

WI-195 (2026-07-16, opus build / fable integrate): scripts/plan_briefs.py - allowlist-only brief assembly, redaction BY CONSTRUCTION: build_surface reads ONLY system-requirements.csv + interfaces.csv (minimal columns, -000 rows dropped) so status.md/log.md/self-assessments are unreachable; assemble() strict {{NAME}} fill (unknown key + unfilled placeholder both raise, computed from the template's own placeholder set so slot VALUES containing braces pass verbatim); HAT_KEYS registers DUALPLAN-PLANNER/CRITIC/ARBITER on --prompt-map with the kit-template fallback located relative to the script; dispatcher-block stripping; surface/hats CLI. 16 tests incl. the sentinel proof (status/log sentinel never reaches any hat's brief). Spine LLR-071/TC-071 under SR-061 (provisional); Proposed IF-059 (source; nearest IF-057), CMP-004; scaffolded.
