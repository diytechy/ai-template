+++
id = "WI-1007"
title = "trajectory_arch.py is split by the checks it holds, each module under the size line, with no change of behaviour"
workstream = "process"
sr_refs = ["SR-159", "SR-165"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#122-rulings-taken-on-2026-11-15-and-2026-11-16"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-11-16 at the operator's ruling (HANDOFF §12.2:
"`trajectory_arch.py` (1,132 code lines): file a work item to decompose it;
not on this branch"). The module passed the line-count ratchet's 1,000-line
threshold while the first-day and conversion fixes landed (989 to 1,012), and
WI-999's component derivation record took it to 1,132. Its own section
comments name seven checks: the armed definition gate, seam-TC coverage and
its migration allowlist, the Implements-tag and CodeSymbol crosscheck, the
How-SW top-view rule, the declared arch-map scan profile, the component
derivation record, and specs acting on declared interface boundaries.

Where the cuts fall is the plan's to find. Its scope critique is owed before
a claim.

## Done-when

- [ ] `trajectory_arch.py` is split along the checks it holds, and every
      module that results is under the ratchet's threshold. The public names
      callers import still resolve, or every caller moves in the same change.
- [ ] Behaviour is unchanged. `check_trajectory.py --strict` prints the same
      findings on this repository before and after. The existing tests pass,
      with only their imports changed.
- [ ] Each LLR binding a moved symbol names its new module. `trace.py
      --strict` and `check_trajectory.py --strict` are clean, and the
      module-size baseline holds the new modules.
