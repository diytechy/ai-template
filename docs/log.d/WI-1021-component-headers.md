## 2026-11-21 — WI-1021: each file declares its one component in a Component header, and membership is read from the headers

Deferred open items: none. The operator ruled the one-component table on
2026-11-21, accepting every pick (the queue-drill HANDOFF §3.5); the ruling
is in the spec's Context, and WI-1045 is filed on trunk for
`acceptance_record.py`'s landing rules. The acts owed go to automated
adjudication.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1021` from `1aa6c439a`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1021-component-headers.md`); the table is
`../plans/WI-1021/component-table.md`.

- **Plan** (`5e13999ca`): the reader beside `gen_arch_map.module_contracts`,
  the census in `arch_inputs`, membership through
  `kitlib.spine.module_components`, and the one-component table with its
  near-even, two-component and against-the-majority flags at the top.
- **Build** (`458724024`): `gen_arch_map.file_component`, the one reader;
  `arch_inputs.component_headers`, the closed scope's census;
  `component_top_view`, the cross-component rule and `gen_components` read
  the headers; an edge touching an undeclared file is unclassified; the
  multi-membership advisory is retired. 167 files carry a header. IF-326 is
  new; IF-194, IF-195 and IF-316 gain the requestor the picks made cross.
  LLR-396, LLR-397 and TC-457 to TC-461 are new and `Drafted`.
- **`derive_stage` is unchanged**: it reads no membership, so the spec's
  "DevStg-Arch derivation" had nothing to switch.
- **Size ratchet**: `gen_arch_map.py` re-stamped 1599 -> 1655 SLOC, a
  reviewed bump: the spec places the one reader beside the `Contracts:`
  reader, and the scope walk went to `arch_inputs` rather than adding to
  it. The module's decomposition stays WI-545's. `check_trajectory.py`
  re-stamped down, 1659 -> 1657.
- **Before the review** (the coordinator): the declaration's carriers
  narrowed to the spec's (`REM` for a batch file, `#` for PowerShell; the
  reader had also read `::` and a `<# #>` help block); LLR-396 and TC-457
  follow. `gen_arch_map.py` re-stamped 1655 -> 1657 SLOC, a reviewed bump
  for the grammar's own two-line carrier table.
- **Acts owed**: LLR-373, LLR-067, LLR-199, TC-435, TC-067, TC-195, TC-436
  and CMP-006's `notes` drift (text only); the new rows' first acceptance.
- **Tests**: red first, `37 failed in 1.46s`, then `14 passed in 0.83s`; the full suite `2 failed, 8268 passed, 31 skipped, 18 warnings in 5206.14s (1:26:46)`, the two (a moved line pin, a stale stage record) fixed and rerun `41 passed in 17.83s`; `run_menu.py smoke` `3713 passed, 3 skipped, 18 warnings in 83.29s (0:01:23)`; `trace.py --strict` `orphans=0 integrity=0`; `check_trajectory.py --strict` clean.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas**: `PROCESS.md` 101,623 -> 101,950 (+327);
  `PROCESS_OPTIONS.md` 202,180 -> 202,304 (+124); the byte-budget skill
  4,742 -> 4,631 (cap 5,000); `RESYNC_PACK.md` 734,651 -> 737,613
  (unbudgeted).
