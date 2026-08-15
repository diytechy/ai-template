+++
id = "WI-272"
title = "Dashboard work-item status fidelity — preserve deferred and blocked instead of rewriting both as queued in labels, details, accessible names, and the legend"
workstream = "dashboard"
sr_refs = ["SR-070", "SR-053"]
needs = ["~WI-267"]
buildtier = "medium"
safety_class = "ordinary"
order = 269
+++

## Deliverable

The dashboard no longer rewrites the registry's six statuses into four. A STATUS_BUCKET table makes the six-to-four SWATCH mapping explicit and _wi_status returns the row's own word for every text surface, so a deferred/blocked row's tooltip, accessible name, drill label, node class and detail JSON all report what it actually is (previously the clamp ran BEFORE those were built, so a parked row literally SAID queued). deferred/blocked keep queued's swatch deliberately rather than minting two hues — that would worsen the live U5 near-duplicate residue (LLR-102) — so they are told apart by their own glyph and the legend NAMES the grouping ('not started') instead of letting a shared colour imply queued. Per-status glyphs added (deferred, blocked) and A3's invariant strengthened from one-glyph-per-FILL to one-glyph-per-STATUS with all glyphs distinct, which is what keeps the two swatch-sharing statuses distinguishable without colour at all. Guards: tests/test_gen_trajectory.py::test_wi272_deferred_and_blocked_are_never_rewritten_as_queued + ::test_wi272_status_is_carried_through_the_tiered_drill_too (both emitters), verified to fail against three separate reversions including the original clamp.
