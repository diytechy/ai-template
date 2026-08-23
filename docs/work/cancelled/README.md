# This directory moved — `cancelled/` now lives under the archive

WI-504 (OI-55 ruled (a), 2026-08-22): terminal work-item history left the
active workspace so an agent listing `docs/work/` meets only rows still in
flight, not hundreds of closed ones. Every spec that used to live here is now
at [`docs/archive/work/cancelled/`](../../archive/work/cancelled/README.md) —
same filename, one directory deeper.

Nothing about the registry changed except the path: status is still the
DIRECTORY, `cancelled/` still means a terminal won't-build row whose reason is
its Deliverable, and `kitlib.registry.read_spec_rows` reads `docs/work/` and
`docs/archive/work/` as ONE registry (`spec_roots`), so a cancelled row here is
exactly as live a trace link and dashboard count as it always was. This file
is the only thing that stays — a pointer, not a spec — so a link written
against the old path resolves to an explanation instead of a 404.
