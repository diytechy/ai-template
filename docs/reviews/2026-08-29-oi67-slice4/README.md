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
  adversarial round over the folded result (gpt-5.6-sol, medium effort, run
  read-only in a worktree at `816090cd`) and what it found: `VERDICT:
  CHANGES-REQUESTED findings=11`.

## Dispositions (2026-08-29, taken at the slice-6 sitting)

| # | Finding | Disposition |
|---|---|---|
| 1 | `IF-159`'s body claims a failed write is not left on disk; `_self_verify` leaves it | **APPLIED** — the body now says the mismatching file stays where the caller can inspect it and no path is returned. The read-back is the writer's own verification, not a consumer read; the row stays write-side. |
| 2 | `IF-160`: `record_round` reads then rewrites; "the escalation policy reads it" unsupported | **APPLIED** — the claim is gone; the body states the read-back-then-rewrite. The read side is `IF-047`'s (score_reviews is on its consumer list already). |
| 3 | `IF-156`: trunk_step DELETES each compiled fragment — a mutation of the medium | **DEFERRED, agreed** — a requestor row to mint; next worklist. |
| 4 | Three tracked fragments open with `#`/`###`, so `--compile-log` would refuse | **DEFERRED to the trunk lane** — pre-existing on trunk; the row states the grammar the code enforces; the fragments are the trunk lane's to fix before the next compile. |
| 5 | `IF-163` overlaps `IF-164` (both cover the generated block) | **APPLIED** — `IF-163` narrowed to the hand-authored bytes outside the marker pair. |
| 6 | `IF-020` still bundles stdout JSON and the log file | **DEFERRED, agreed** — two rows to mint; next worklist. |
| 7 | `IF-102`'s body still promises `rows_seq_from_text` (IF-119's) | **APPLIED** — clause removed. |
| 8 | Strict enforcement allows invalid ownership/body states | **ADDRESSED by slice 6** — the armed gate (`contract_body_findings`); the undeclared-owner case stays a warn by decision 6.2. |
| 9 | `TC-161`'s approved `method` prose still names `IF-127` | **KEPT, owner-owed** — an approved cell; recorded in the WI-531 fragment. |
| 10 | README exemption is case-sensitive on Windows | **APPLIED** — case-folded (`readme.md` in any case is the declaration home). |
| 11 | "eight far sides" reproduces as nine | **APPLIED** — the fragment says nine, with the counting rule. |
