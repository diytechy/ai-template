## 2026-11-23 — WI-1062: WI-1061's verdict answered: SR-251's chain states its live scope, the keyless condition and an all-or-nothing write

Deferred open items: none. The row changes spine text, one writer call, one
test module, the RESYNC pack and the regenerated evidence and views; every
choice it made is stated by a spine row, so it needed no decisions record.

Built on the maintenance branch `maint/wi-1062` from `3db0c6823`, with the
commit hooks on and planning `none`. The record is in the row's Deliverable
([WI-1062](../archive/work/complete/WI-1062-answer-wi-1061-verdict.md)).

- **Scope:** SR-251 and LLR-406 both say "each test case the test-case
  registry holds", and both say a declaration naming a case the registry
  does not hold adds nothing and is not reported as changed. "live" is gone
  from LLR-406. SR-251's acceptance criteria also state the report of
  changed cases that LLR-406 already described.
- **Keyless:** LLR-406 gives a case with no evidence key a key only when its
  declarations supply a part, so a keyless case no declaration names stays
  keyless and unchanged.
- **All-or-nothing write:** SR-251's acceptance criteria say an interrupted
  rewrite leaves the registry's bytes as before or fully rewritten, never
  partly written. LLR-406 says the registry is replaced whole: written in
  full beside it, moved in by one step, and a failed move leaves the bytes
  and no copy. The registry writer in `arch_tags.py` now calls
  `kitlib.observation.write_atomic` (IF-315, both modules CMP-006) instead
  of writing in place. The text keeps the line ends it was read with, and
  the file is still UTF-8. RESYNC entry added.
- **Tests:** three tests tagged TC-483. The failed-replacement test was red
  first against the in-place write (`DID NOT RAISE OSError`). The
  unheld-case and keyless-case tests passed on the code as it stood, so
  five temporary mutations of `arch_tags.py`, none committed, showed both
  of their clauses bite. TC-483's method and expected name the three
  cases; evidence regenerated from the tags.
- **Checks:** the trace-cells, trajectory-arch, arch-map, import-layer,
  size-ratchet and dogfood-sync modules:
  `361 passed, 1 skipped in 132.90s (0:02:12)`. `trace.py --strict`:
  `orphans=0 integrity=0`, its absolute-term count unchanged at 419.
  `check_trajectory.py --strict`: clean. `run_menu.py smoke`:
  `3754 passed, 3 skipped, 18 warnings in 127.52s (0:02:07)`, with a CPU
  budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `system-requirements.toml` +653, `low-level-requirements.toml` +913,
  `test-cases.toml` +1,110, `arch_tags.py` +574, `test_llr_trace_cells.py`
  +3,381, `RESYNC_PACK.md` +1,440.
- **Byte-order mark (the coordinator's addition before review):** the
  writer dropped a leading byte-order mark, at the base as after the swap,
  so LLR-406's "keeps every other byte" was false for such a registry. It
  now sets the mark aside and writes it back; `write_atomic` is unchanged.
  A fourth TC-483 test, red first (`At index 0 diff: b'#' != b'\xef'`),
  and TC-483's method and expected name the case. LLR-406 and SR-251 need
  no new clause: "every other byte" and "only those cells change" cover
  it. The trace-cells, import-layer, size-ratchet and dogfood-sync
  modules: `79 passed, 1 skipped in 15.30s`; `run_menu.py smoke`:
  `3755 passed, 3 skipped, 18 warnings in 93.81s (0:01:33)`, a CPU budget
  WARN only.
  <!-- fig: derived="the totals are those the Deliverable's item 6 declares, each with its command and revision" -->
- **Owed to the next sitting:** the first acceptances of SR-251, LLR-406
  and TC-483.
