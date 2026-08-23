# This directory moved — `complete/` now lives under the archive

WI-504 (OI-55 ruled (a), 2026-08-22): terminal work-item history left the
active workspace so an agent listing `docs/work/` meets only rows still in
flight, not hundreds of closed ones. Every spec that used to live here is now
at [`docs/archive/work/complete/`](../../archive/work/complete/README.md) —
same filename, one directory deeper.

Nothing about the registry changed except the path: status is still the
DIRECTORY, `complete/` still means `done`, and `kitlib.registry.read_spec_rows`
reads `docs/work/` and `docs/archive/work/` as ONE registry (`spec_roots`), so
a closed row here is exactly as live a predecessor, trace link and dashboard
count as it always was. This file is the only thing that stays — a pointer,
not a spec — so a link written against the old path resolves to an
explanation instead of a 404.
