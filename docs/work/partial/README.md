# This directory moved — `partial/` now lives under the archive

WI-504 (OI-55 ruled (a), 2026-08-22): terminal work-item history left the
active workspace so an agent listing `docs/work/` meets only rows still in
flight, not hundreds of closed ones. Every spec that used to live here is now
at [`docs/archive/work/partial/`](../../archive/work/partial/README.md) —
same filename, one directory deeper.

Nothing about the registry changed except the path: status is still the
DIRECTORY, `partial/` still means a lane that stopped early, its per-close
report under `docs/handbacks/` is still the close event's identity, and
`kitlib.registry.read_spec_rows` reads `docs/work/` and `docs/archive/work/`
as ONE registry (`spec_roots`), so a partial row here is exactly as live a
predecessor, trace link and dashboard count as it always was — and continuing
the work still mints a successor, never a revival of the row itself. This
file is the only thing that stays — a pointer, not a spec — so a link written
against the old path resolves to an explanation instead of a 404.
