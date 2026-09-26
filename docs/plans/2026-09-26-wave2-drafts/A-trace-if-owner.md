+++
id = "WI-@A@"
title = "Stop trace's interface-owner reachability advisory flagging owners a design row does name"
workstream = "scripts"
specref = "project-trajectory/scripts/coherence.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

`trace.py` warns when an interface row's owner is named by no design row's
`Module` and declares no `Implements:` line. Two defects make that advisory
fire on owners that are traced:

- `coherence.llr_module_ids` takes each `Module` cell whole, so a cell listing
  several modules joined by `;` contributes one unusable key instead of one per
  module.
- `trace._implementing_modules` joins the profile's source root to paths that
  already start from it, producing `scripts/scripts/<mod>` keys that match no
  owner.

At b14d1808, IF-186 (`scripts/bookkeeping`) and IF-187
(`scripts/check_readability`) both get the advisory although design rows name
their modules inside `;`-joined `Module` cells.

IN SCOPE: split `;`-joined `Module` cells wherever the owner join reads them,
fix the doubled source prefix, and test both with an owner reached each way.
NOT IN SCOPE: changing what counts as reaching the spine.

## Done-when

- A test with an owner named only inside a `;`-joined `Module` cell, and one
  reached only through an `Implements:` header, gets no advisory; an owner
  reached neither way still does.
- `trace.py` at the landing commit prints no reachability advisory for
  IF-186 or IF-187.
- The commit bar passes.
