+++
id = "WI-284"
title = "Stop the forward-only cascade - integrating a WI flips its row to done but generate_status only rewrites the marker block, leaving the just-done id in status.md's hand-authored prose, so the forward-only smoke test reddens every subsequent train's DONE gate (this inherited-red burned WI-276's budget); scrub the done id at integrate (option a) and/or move the forward-only check off the smoke bar onto the gate tier (option b, the bleeding-stopper)"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 281
+++

## Deliverable

Chose option (a) done cleanly by GENERATION (the kit's own generated-not-hand-maintained rule): gen_trajectory.py --status now emits a scheduler-derived Ready-frontier block inside the forward-only-exempt STATUS markers (never lists a done WI); agent_dispatch._regenerate_disposition_artifacts runs that --status regen at integrate/blocked-disposition so a closed id drops out automatically; status.md forward prose made id-free (points at the generated block). Also fixes WI-283's core (the disposition now regenerates the status-map projection). Regression tests in tests/test_trajectory.py (frontier self-prunes; hand-authored region still policed). Hand-applied 2026-07-23 per owner directive, full suite green.
