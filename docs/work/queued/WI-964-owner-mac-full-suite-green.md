+++
id = "WI-964"
title = "Owner: the full unfiltered suite is green on the owner's Mac at WI-910's landing"
workstream = "process"
sr_refs = ["SR-046", "SR-032"]
specref = "docs/specs/WI-910.md"
needs = ["WI-910"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Split from WI-910 by the owner on 2026-10-20 (coordinator-2026-10-20 D-019):
WI-910 fixes what CI can verify; this row is the one step only the owner can
take, a run on the owner's own Mac. It is owner-held: no headless leg claims
it, and it is listed under the coordinator handoff's "For the owner". Its
spec of record is WI-910's, `docs/specs/WI-910.md`.

## Done-when

- The owner runs the full unfiltered suite (`python -m pytest -q -n auto`) on
  the Mac at or after WI-910's landing, and the command, the revision and
  the result are recorded in a log fragment.
- A red found there is filed as its own row, never fixed under this one.
