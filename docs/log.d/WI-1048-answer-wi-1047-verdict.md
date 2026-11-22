## 2026-11-22 — WI-1048: WI-1047's verdict answered: LLR-373 and TC-081 say what the code does, the returned rows are ready for a second sitting

Deferred open items: none. The row changes spine text and tests and takes no
operator decision; it needed no decisions record.

Built on the maintenance branch `maint/wi-1048` from `2474d7b4f`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1048-answer-wi-1047-verdict.md`).

- **LLR-373** (Accepted; Detail in `732d08500`, title and rationale after
  it at the coordinator's request): the component view's generator reads no
  join; it lists each component's modules from the declarations themselves
  and places each seam from its endpoint cells alone (LLR-199, TC-435). The
  join's readers are the top view, the cross-component scan and the
  connectivity warns. The title no longer says the component view reads
  it, and the rationale drops the pre-WI-1021 row inputs.
- **LLR-398** (Drafted): its scan surface exists only outside files mode
  and with the source root present, a listed header included, as the code
  reads it; TC-474 and its test follow. Whether a files-mode adopter's
  listed headers should be scanned is left as a question.
- **TC-081** (Accepted, Method and Expected; Evidence traced): LLR-080's
  rendering, with three new tests and the table-fallback test as evidence.
- **LLR-393, LLR-394, TC-455, TC-456** (Drafted): no implementation carrier
  in their text; TC-455's Expected states its own pass condition, and its
  test gains the literal mapping.
- **TC-474** (new, Drafted): LLR-398's five unverified clauses, over
  existing tests (one gains two arms).
- **TC-475** (new, Drafted): LLR-395, over TC-428's and TC-429's tests and
  a new test of a declared test that fails. WI-1038 is superseded by
  WI-1048; the coordinator cancels it on trunk at the merge.
- **Tests:** the 52 modules the rows' modules, registry readers and
  whole-tree tests name:
  `1898 passed, 1 skipped, 18 warnings in 4515.10s (1:15:15)`.
  `run_menu.py smoke`: `3717 passed, 3 skipped, 18 warnings in 593.77s (0:09:53)`,
  with a CPU budget WARN only. `trace.py --strict`:
  `orphans=0 integrity=0`; `check_trajectory.py --strict`: clean. After the
  follow-up: the 15 registry-reading and whole-tree modules,
  `540 passed, 1 skipped, 18 warnings in 187.15s (0:03:07)`; smoke,
  `3717 passed, 3 skipped, 18 warnings in 128.86s (0:02:08)`.
  Review round 1 (Sol's MINOR: `module_components`' docstring drops its
  caller-policy claims, with a RESYNC entry): the 16 modules a docstring
  there can reach, `417 passed, 1 skipped, 18 warnings in 130.27s (0:02:10)`;
  `trace.py --strict` `orphans=0 integrity=0`.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `low-level-requirements.toml` +866, `test-cases.toml` +7,786.
- **Acts owed:** LLR-373's and TC-081's drift, LLR-080's amendment again,
  and the first acceptance of LLR-393, LLR-394, LLR-395 and LLR-398 with
  TC-455, TC-456, TC-463, TC-474 and TC-475, beside what WI-1047's sitting
  already judged.
- **Review:** round 1, Sol (low) and Hydrogen (low): Hydrogen APPROVE; Sol
  one MINOR (a docstring), fixed in `9ae7df40c`. Round 2 narrow: both APPROVE.
