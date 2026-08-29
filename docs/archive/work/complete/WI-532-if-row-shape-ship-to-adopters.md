+++
id = "WI-532"
title = "Ship the interface row shape: PROCESS.md section 8, templates, reference docs, RESYNC entry, converter (OI-67 slice 5)"
specref = "docs/plans/2026-08-29-if-row-shape-plan.md"
workstream = "architecture"
sr_refs = ["SR-159"]
needs = ["WI-528"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The shipped kit describes the row the code reads. Record:
[../../../log.d/2026-08-29-wi532-if-row-shape-shipped.md](../../../log.d/2026-08-29-wi532-if-row-shape-shipped.md).

`PROCESS.md` §8 rewritten for the one-owner row inside its watched budget
(−367 bytes): owner as the providing thing, the far side naming the direction,
`Channel`/`Data`, the definition beside the code, mint header-first, reason
cells argument-never-citation. `PROCESS_OPTIONS.md`'s intra-repo section,
`INTERFACES.template.md`'s rules and worked snippet, the registry-machinery
reference row and the two enforcement-audit rows follow. A `RESYNC_PACK.md`
entry `[since 088a6cca]` with the converter commands, the search recipe and
what replaces the `req_refs` grep. `migrate_carrier.py --if-shape`: in-place,
comment-preserving, reports every judgement it did not make (dropped
`req_refs`, seeded `channel`, an owner it could not derive), `--check` writes
nothing, idempotent, four tests.
