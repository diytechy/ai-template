+++
id = "WI-989"
title = "OI-119's ruling: restore WI-963's plan binding"
workstream = "process"
sr_refs = ["SR-178"]
specref = ""
needs = ["OI-119"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

Closed at OI-119's ruling (2026-11-02, option (a); docs/decisions/coordinator-2026-11-02.toml#D-003). The ruling commit moves the OI-115 item, text unchanged, from WI-963's trunk claim copy's Done-when into its Trust section, so the claim copy's Done-when digest is again sha256:371fa4c3f41d21b6, the one WI-963's pass record binds. Option (a) routes no work to this row; WI-963's lane carries the rest.

## Context

Filed by hand in headless leg 29 (2026-11-01) with OI-119, as the queued
placeholder row a pending open item is filed with (OI-102): it carries the
owner's decision to the queue. OI-115's ruling added an item to WI-963's
claimed Done-when after its single plan passed, so on the rebased lane the
plan gate no longer reads the pass record as binding (OI-119 states the
evidence and the options; coordinator-2026-11-01 D-008).

## Done-when

- [x] The owner rules OI-119, and the ruling commit replaces this list with
      the work the ruling routes (OI-102): for option (a), the ruling commit
      moves the item into WI-963's Trust section and this row closes citing
      the ruling; for (b) or (c), this row becomes the routed work.
