+++
id = "WI-666"
title = "Name each registry's own anchor copy on the owner's surfaces, and hold an amendment act to its scope at merge"
workstream = "scripts"
specref = "project-trajectory/scripts/baseline_snapshot.py"
sr_refs = ["SR-146", "SR-148"]
needs = ["WI-646"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

WI-646 made the amendment brief name, for each registry it shows, the commit
that last wrote that registry's recorded copy (`baseline_snapshot.stamp` given
the registry), and bound the brief to the row's `Adjudicates` scope. Two
places still carry the defects it fixed:

- `adjudicate_brief.first_approval_values`' baseline line, and
  `trace.reattest_model`'s per-entry `baseline` (which feeds the owner's
  approval brief `docs/ratify/CURRENT.md` and the open-items view), still call
  the directory-wide `stamp(root)`. The owner is told the newest write
  anywhere in the snapshot directory, not the copy the rows were measured
  against: at the WI-641/601/603 sitting that named a needs-only copy for
  requirement and design rows.
- At merge, `acceptance_record.merge_approval_refusal` checks only a
  first-approval row's act against its `Adjudicates` scope. An amendment
  adjudication now records a scope too, but its `--reattests` act is not held
  to it, so an act could re-anchor rows its verdict never ruled.

IN SCOPE: pass the registry to `stamp` at both owner-surface sites; extend the
merge check to an amendment row's `--reattests` act against its recorded
scope; test each seen failing first.

## Done-when

- The owner's brief and the open-items view name, per registry, the commit
  that last wrote its copy.
- An amendment act re-attesting a row outside its row's `Adjudicates` scope is
  refused at merge, by name.
- The commit bar passes.
