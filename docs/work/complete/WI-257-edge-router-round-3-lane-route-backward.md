+++
id = "WI-257"
title = "Edge-router round 3: lane-route backward edges instead of keep-direct-cubic - the When 1-unphased / unphased-2/3/4 and How-SW CMP-001-CMP-004 wires hide under their own endpoint boxes and read as sprouting from a box edge, effectively untraceable end-to-end (080-CRITIQUE strongest letter-passing finding; also the in-port-fan crossing left of CMP-001's in-port). Plus the two 111-REVIEW-A MINORs: widen _detour_d's obstacle span to the stub-extended reach (outboard-stub residual fail-open, 13/3000 synthetic, 0 live - or soften the docstring absolute) and short-circuit/cap lane candidates (dense-overlap perf ~30-50x vs pre-hardening, no live impact on tiered geometry). Render surface: bundle a fresh critique"
workstream = "dashboard"
sr_refs = ["SR-052", "SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 254
+++

## Deliverable

Edge-router round 3 (gen_trajectory.py): backward edges lane-routed so they no longer hide under their own endpoint boxes; _detour_d obstacle span widened to the stub-extended reach (outboard-stub fail-open closed; docstring scoped to searched lanes); candidate lanes capped (_MAX_LANES=24) with first-clear short-circuit and second-pass skip. T8=0 through-box on all 5 real panels, byte-stable (0 forward wires changed), 3 biting tests. Adversarial REVIEW-A APPROVE f=2 (both downstream-robustness MINOR, owner notes).
