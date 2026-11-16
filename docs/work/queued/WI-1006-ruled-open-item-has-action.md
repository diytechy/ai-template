+++
id = "WI-1006"
title = "run.cmd audit reports each ruled open item with no action planned, done or handed on to a later open item"
workstream = "process"
specref = "docs/specs/WI-1006.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request). The spec of
record holds the rule, why it reads text rather than `needs`, and the numbers
a prototype measured on this repo. Its scope critique is owed before a claim.

No SR states this today. The critique decides whether one is owed, or whether
IF-073's registry contract carries it.

## Done-when

- [ ] A check reports, warn-only, each `ruled` open item that has none of: a
      work item in an open or complete directory whose text names it; a later
      open item naming it that is `pending`, or `ruled` and itself covered;
      a `follow_up` cell. The rule is the spec's.
- [ ] The open-items template's header documents the optional `follow_up`
      cell and asks a follow-up item to name the item it continues; the `-000`
      row shows it. This repo's registry follows.
- [ ] `run.cmd audit` runs the check, and a finding does not change its exit
      code.
- [ ] The four ruled items it reports at filing (OI-35, OI-79, OI-89, OI-90)
      each gain a `follow_up` cell or a citing row, so it lands with 0
      findings.
- [ ] Regressions name each arm: covered by a draft, queued, active, deferred
      or complete row; not covered by a cancelled, partial or restructured
      row; handed to a pending item; handed through a ruled item
      that is itself covered; a cycle of ruled items with no row; a
      `follow_up` cell; no registry (vacuous); a registry that does not parse
      (stops, as the readers do).
- [ ] A RESYNC entry if the check ships to adopters: a new optional key, no
      forced migration.
