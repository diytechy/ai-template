# OI-67 slice 3 — the cell pass, as a four-worker round (2026-08-29)

The per-row authoring of WI-530, run as four parallel Opus workers over
disjoint owner-file batches with a serial fold into the registry. This folder
is the record: what each worker was told, what it was given, what it reported,
and the script that folded the reports. Read it from
[the log fragment](../../log.d/2026-08-29-wi530-cell-pass.md).

- `slice3-brief.md` — the shared worker brief: the row shape, the header
  grammar, what a body must state, what a worker may and may not touch, the
  report schema.
- `slice3-worklist.json` — every row before the pass: owner, far side, seeded
  channel, the legacy contract text, and which files declared the id.
- `slice3-batch-{A,B,C,D}.json` — the four disjoint batches (owner files and
  the marker removals assigned to each).
- `slice3-report-{A,B,C,D}.json` — one object per row: the confirmed
  channel and far side, the proposed `data`, whether a body was written, which
  reason cells were moot, and the worker's note. **The `note` fields are the
  worklist for slices 4 and 6** — split candidates, stale far sides, rows a
  ruling should collapse, the loader gap on the CSV owner.
- `slice3-fold.py` — the fold: applies the reports to `interfaces.toml` block
  by block (channel, far side, `data`, the legacy `contract` and the moot
  reason cells dropped), text-level so the header and every other cell
  survive byte-for-byte. Dry-runs without `--write`.
