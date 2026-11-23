## 2026-11-22 — WI-1056: WI-1055's verdict answered: F-3's five unblessed rows re-landed under an amended SR-221, and SR-248's chain repaired

Deferred open items: none. The row changes spine text, one report line of
the evidence regeneration command, docstring back-links and three test
modules; every choice it made is stated by a spine row, so it needed no
decisions record.

Built on the maintenance branch `maint/wi-1056` from `3c33b3783`, with the
commit hooks on, under the plan `docs/plans/WI-1056/plan.md` (`9548c30c1`)
and the coordinator's go-ahead. The record is in the row's Deliverable
(`../archive/work/complete/WI-1056-answer-wi-1055-verdict.md`).

- **SR-248's split:** SR-248 keeps discharge (one `shall`). SR-249
  (placement), SR-250 (the files realizing a design row, read from the
  code's back-links) and SR-251 (the evidence generation, LLR-406's new
  parent in place of SR-157) are new. LLR-403 keeps placement, its consumer
  list cut to what TC-480 verifies; its discharge clause moved to the new
  LLR-408 (TC-485), which names LLR-201 as the pass that runs it. LLR-405
  cites LLR-204's grammar and states the absent root, the unreadable file
  and the missing header.
- **Re-landed under an amended parent:** SR-212's acceptance states
  LLR-244's reach; SR-221 says the listing is for a file, read through the
  back-links. LLR-244, LLR-263, TC-239 and TC-258 carry `8e08b3029`'s text
  with every code name replaced by contract terms. Text only on the six
  `Accepted` rows. WI-1018's Context no longer lists SR-221.
- **Code:** the evidence regeneration command names a missing test-case
  registry or tests root instead of calling every cell current (red first);
  its report line sits beside the writer, re-stamping `trace.py`'s size
  baseline down by 4. RESYNC entry added.
- **Tests:** fifteen new or extended tests across `test_llr_trace_cells`,
  `test_assumption_gate` and `test_trace`, and one re-tagged from TC-480 to
  TC-485. Each that drives behaviour the
  code already had was shown failing under a mutation of that code, never
  committed, and green once restored. The 85 affected modules:
  `46 failed, 3003 passed, 2 skipped, 18 warnings in 839.92s (0:13:59)`,
  one failure this branch's (fixed in `08639915b`) and 45 failing
  identically on the base. `run_menu.py smoke`:
  `3735 passed, 3 skipped, 18 warnings in 145.71s (0:02:25)`, with a CPU
  budget WARN only.
  `trace.py --strict`: `orphans=0 integrity=0`; `check_trajectory.py
  --strict`: clean; the three assumption-gate steps: 0 findings each.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Pre-existing reds:** 45 tests in `test_intake_held_act`,
  `test_intake_settled`, `test_snapshot_readers`, `test_assumption_gate`'s
  release half and `test_done_when_blessing` fail on the base `9548c30c1`
  with the same node ids; 42 stop at "the held-act mint was refused: ...
  cannot be read at <sha>". Not this row's to fix.
- **Byte deltas:** no budgeted or watched file was touched.
  `system-requirements.toml` +4,815, `low-level-requirements.toml` +1,707,
  `test-cases.toml` +4,844, `RESYNC_PACK.md` +1,597.
- **Acts owed:** the amendments of SR-212, SR-221, LLR-244, LLR-263, TC-239
  and TC-258; no routed traced change; the first acceptance of SR-248 to
  SR-251, LLR-403, LLR-405, LLR-406, LLR-408 and TC-480 to TC-485.
