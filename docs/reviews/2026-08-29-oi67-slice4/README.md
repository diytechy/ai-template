# OI-67 slice 4 — the split, as a three-worker round (2026-08-29)

The per-row split of WI-531, run as three parallel Opus workers over disjoint
owner-file batches with a serial fold into the registry — the slice-3 shape
([../2026-08-29-oi67-slice3/](../2026-08-29-oi67-slice3/README.md)), applied
to the split worklist the slice-3 workers' notes produced. This folder is the
record: what each worker was told, what it was given, what it reported, and
the script that folded the reports. Read it from
[the log fragment](../../log.d/2026-08-29-wi531-if-row-split.md).

- `slice4-brief.md` — the shared worker brief: what a `new` / `edit` /
  `delete` action means, the body rules for a split row, what a worker may
  and may not touch, the report schema.
- `slice4-worklist.json` — every registry action of the slice with its id
  (new ids assigned from the watermark, IF-145 onward), owner, far side,
  channel, data, body home, the row it splits from, and the slice-3 finding it
  answers (`why`).
- `slice4-batch-{A,B,C}.json` — the three disjoint batches: A the harness
  family (`trace`, the checkers, `gen_okf`, `gen_arch_map`, `derive_stage`),
  B the coordination family (`subagent_gate`, `plan_coverage`, `integrate`,
  `trunk_step`, `run_menu`, `schedule`, `score_reviews`, `intake`,
  `spine_carrier`, the new `docs/log.d/` README), C the media family (the
  `docs/work/`, `docs/reviews/`, `docs/test/` READMEs, `docs/agents-enabled`,
  `docs/status.md`, `docs/process.toml`, the three generated-document rows).
- `slice4-report-{A,B,C}.json` — one object per row action: the confirmed or
  MEASURED far side, channel, data, tie-backs and component, whether the body
  was written, and the worker's note.
- `slice4-fold.py` — the fold: applies the reports to `interfaces.toml` block
  by block (a new row minted directly after the row it splits from, a
  collapsed row removed, an edited row's far side / channel / data /
  tie-backs rewritten), text-level so the header and every other cell survive
  byte-for-byte. Dry-runs without `--write`.
- `PROMPT-ADVERSARIAL.md` / `RAW-SOL-ADVERSARIAL.md` — the cross-family
  adversarial round over the folded result and what it found.
