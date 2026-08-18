## 2026-08-18 — `docs/work/README.md`: the registry states its own location→status contract

**Why.** Two gaps, both of which cost the owner the same question repeatedly.
(1) Nothing *inside* `docs/work/` said what the folders mean, so "should closed
WIs move to an archive?" kept getting re-asked and re-derived — wrongly. They
must not: `spec_files` rglobs the whole of `docs/work/`, so a terminal row is
still a `needs` predecessor, a `sr_refs` trace link and a dashboard count, and
`docs/declared-absences` already rules `docs/work/archive/` must never
materialize. The neighbouring `docs/specs/README.md` teaches the *opposite*
lifecycle (rule R-F archives a spec-of-record at close), which is exactly the
generalization a reader makes with only that README in hand. (2) The shipped
status tables listed six directories; `partial/` — SR-144's third terminal,
live in `SPEC_STATUS_DIRS` and `TERMINAL_STATUSES` — was absent, so an adopter
reading the shipped docs could not learn the state exists.

**What changed.**

- New `project-trajectory/work/README.template.md` and its byte-identical
  dogfooded copy `docs/work/README.md` (39 lines): the seven-row
  location→status table, `SPEC_STATUS_DIRS` cited as the authority rather than
  re-stated, and the terminal-rows-stay rule with the two-artifacts /
  two-lifecycles contrast against `docs/specs/`.
- `partial/` added to the status table in `work/WI-000.template.md` and its copy
  `docs/work/queued/WI-000-example.md`.
- `bootstrap.py`: `work/README.template.md` → `docs/work/README.md` in `MAPPING`,
  plus the header docstring (which also listed the status dirs without
  `partial`).
- Pins: `docs/work/README.md` in `test_dogfood_sync.BOILERPLATE_COPIES` (byte
  identity, the idiom the other five scaffolded READMEs use) and in
  `test_bootstrap`'s scaffold file list, which also gained the
  `docs/work/partial/.gitkeep` it had been missing since the folder joined
  `GITKEEP_DIRS`.
- A reserved `RESYNC_PACK.md` §3 entry, awaiting its landing sha.

**Note left for someone else.** The `BOILERPLATE_COPIES` preamble still says
"these four copies"; it was already stale at five before this change and is now
six. Not touched — a one-word fix in another lane's likely path.
