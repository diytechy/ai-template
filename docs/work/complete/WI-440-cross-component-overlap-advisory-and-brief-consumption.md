+++
id = "WI-440"
title = "OI-14's two do-not-wait fixes, both partition-neutral: (1) correct the DIRECTION of check_trajectory.cross_component_findings' overlap suppression — today a module tagged into MORE components monotonically SILENCES the check (64 of 97 classifiable edges suppressed by set overlap, 17 via a multi-tagged endpoint), which is authoring-silenceable fail-open; report the multi-membership overlap as its own advisory instead of suppressing on it, warn-first; (2) state in the interfaces declaration (PROCESS.md section 8) that plan_briefs.IF_SURFACE_COLUMNS feeds the IF row VERBATIM into the dual-plan LLM briefs — the one place a mixed Contract cell costs behaviour rather than tidiness — so the consumption is declared rather than rediscovered."
workstream = "lock-program"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

Completed 2026-08-13. The overlap-suppression direction is fixed: an import
edge silenced ONLY by a multi-tagged endpoint's set overlap now surfaces as a
warn-only advisory naming the module(s) and edge — 15 on this repo, exactly
OI-14's measured 17 minus the 2 pairs already covered by a declared IF row.
The hard finding, the untagged-endpoint vacuousness (containment's job) and
the components_check opt-out are unchanged; the advisory never joins the exit
code, even under --strict. PROCESS.md §8 declares the planning-brief
consumption (+311 B); PROCESS_OPTIONS documents the new WARN in the layer
emitting it (+355 B); complexity ratchet entry DELETED by decomposition
rather than bumped. The codex round found two edge defects, both fixed in
the follow-up commit: the scan read interfaces.csv before the vacuity guard
(an unreadable CSV crashed a vacuous scan that used to return clean — the
covered-pairs read is now lazy), and the two public wrappers each triggered
their own scan from main (two reads of the same registries that a mid-run
change could make disagree — the per-root cache makes the one-pass contract
literally true). Builder totals: full 2317 passed / 6 skipped; module 75
passed post-fix; 7 new cases cover advisory-vs-finding-vs-vacuous.
