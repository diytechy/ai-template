# `restructured/` rows live under the archive

`restructured` is a TERMINAL status (the 2026-09-02 backlog-restructure plan
§1.6) — a row absorbed into a successor by a consolidation — and terminal
history left the active workspace at WI-504 (OI-55 ruled (a)). So every
restructured spec lives at
[`docs/archive/work/restructured/`](../../archive/work/restructured/README.md),
one directory deeper, exactly as `complete/`, `cancelled/` and `partial/` do.

The status word is declared for BOTH roots (`kitlib.registry.SPEC_STATUS_DIRS`
maps a status to a directory NAME, and `read_spec_rows` reads `docs/work/` and
`docs/archive/work/` as one registry), so a spec filed here would be read
correctly rather than skipped — but the archive is where it belongs. This file
is a pointer, not a spec.
