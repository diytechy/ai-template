+++
id = "WI-287"
title = "The integrator runs the spec close-ritual at done-flip - integrate_train sets Status/Deliverable but leaves SpecRef set and the spec live in docs/specs/, so every WI the loop closes strands two R-F findings (done row still citing a SpecRef + a live spec cited by no open WI; WI-275/279 hit this live); clear the SpecRef cell + git-mv the docs/specs file to docs/archive/specs/<stem>.<date>.md at done-flip (skip empty/non-spec anchors)"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 284
+++

## Deliverable

integrate_train now captures each closing WI's SpecRef (_wi_specrefs), clears the cell in the done-flip _rewrite_wi_rows update (SpecRef=''), and archives a live docs/specs spec to docs/archive/specs/<stem>.<date>.md (_archive_closed_specs; git-mv, skips empty/non-spec/absent); the integration log records the move. Tests in tests/test_agent_loop_integrate.py (WI-287 pair). Hand-applied 2026-07-23 per owner directive alongside the WI-275/279 cleanup it prevents; full integrate module 59p.
