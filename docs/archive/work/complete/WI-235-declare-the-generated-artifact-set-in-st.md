+++
id = "WI-235"
title = "Declare the generated-artifact set in stack.ini instead of hardcoding GENERATED_ARTIFACTS in the integrator (owner question 2026-07-19)"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["~WI-231"]
buildtier = "medium"
safety_class = "high-risk"
order = 232
+++

## Deliverable

The integrator's auto-resolution allowlist is now DECLARED, not hardcoded. agent_dispatch's module-level GENERATED_ARTIFACTS tuple became DEFAULT_GENERATED_ARTIFACTS (the built-in fallback) plus _generated_artifacts(wt), which reads a [generated] section of the INTEGRATE worktree's OWN docs/stack.ini (configparser, optionxform=str so PROJECT_STATE.html keeps its case, interpolation off) at composition time - each row '<path> = <kind> [| <BEGIN> | <END>]' parsed by _parse_generated_row into (matcher, block, kind); kinds trajectory|okf|status|archmap. An ABSENT section falls back to the defaults byte-for-byte; a present section is the WHOLE set (an omitted default drops out); a MALFORMED row (bad kind or a marker count that is neither 0 nor 2, or an unreadable stack.ini) returns a non-blank reason so _compose_train FAILS CLOSED and parks rather than widening resolution. The loader lives in _compose_train and threads artifacts into _resolve_composition_conflict/_regenerate_generated/_generated_entry, keeping _resolve_composition_conflict at its C901 10 (no baseline change). bootstrap scaffolds the section via stack.ini.template (kit defaults, skills index deliberately absent - WI-231 ruling recorded in the section comment); ADOPTING.md 6 notes it is project-owned on re-sync; this repo's own stack.ini dogfoods it. Regressions: declaration-reader unit (absent/extra/removed/malformed), a declared extra artifact composes where an absent section parks, a removed default parks again, a malformed row fails closed, plus the bootstrap-scaffolds-the-section test; the WI-231 end-to-end tests pass unmodified (that IS the byte-for-byte regression).
