+++
id = "WI-440"
title = "OI-14's two do-not-wait fixes, both partition-neutral: (1) correct the DIRECTION of check_trajectory.cross_component_findings' overlap suppression — today a module tagged into MORE components monotonically SILENCES the check (64 of 97 classifiable edges suppressed by set overlap, 17 via a multi-tagged endpoint), which is authoring-silenceable fail-open; report the multi-membership overlap as its own advisory instead of suppressing on it, warn-first; (2) state in the interfaces declaration (PROCESS.md section 8) that plan_briefs.IF_SURFACE_COLUMNS feeds the IF row VERBATIM into the dual-plan LLM briefs — the one place a mixed Contract cell costs behaviour rather than tidiness — so the consumption is declared rather than rediscovered."
specref = "docs/requirements/open-items.toml#OI-14"
workstream = "lock-program"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++
