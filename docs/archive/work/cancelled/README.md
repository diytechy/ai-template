# `cancelled/` — terminal work-item history (the archive home)

The terminal registry directory relocated here from `docs/work/cancelled/`
(WI-504, OI-55 ruled (a)) so the active workspace lists only rows in
flight. Status is still the DIRECTORY: a spec in this folder reads as
cancelled — the work item will never ship, and its body records why.
`kitlib.registry.read_spec_rows` reads `docs/work/` and
`docs/archive/work/` as one registry, so every row here keeps its full
standing as a predecessor, trace link and dashboard count. The old path
holds a pointer README, not specs.
