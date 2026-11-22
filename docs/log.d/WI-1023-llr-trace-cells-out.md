## 2026-11-22 — WI-1023: design rows lose their module, code_symbol and component cells; readers use the Implements index and placement is derived

Deferred open items: none — the one call the row owes the operator is the
batch act's ruling ("trace cells removed, requirement text unchanged"),
asked for in the Deliverable; every other act goes to automated adjudication.

Built on the maintenance branch `maint/wi-1023` from `3002931c7`, with the
commit hooks on, and merged with trunk at `73aa095ce` before the close. The
record is in the row's Deliverable
(`../archive/work/complete/WI-1023-llr-trace-cells-out.md`).

- **Plan** (`16e5dce34`): every reader of the three cells enumerated from the
  code with what it reads instead; derived placement; SR-180's chain; the
  generated evidence column; the migration arm.
- **Build** (`19749ec70`): `module`, `code_symbol` and `component` leave the
  design tier's schema and the template, and the loader refuses a key a
  requirement tier does not declare (the approval snapshot and history read
  without that rule; LLR-404). One index read up from the code's
  `Implements:` tags (LLR-405) feeds `--tests-for`, the interface-form reach,
  the consolidation signal and the build brief. A design row is placed at the
  owner component of each interface its verifying cases name; unplaced rows
  are counted on `trace.py`'s `placement:` line and listed in the component
  view (LLR-403; 119 placed, 236 unplaced at the tip). SR-180, LLR-180 and
  TC-175 retire to SR-248, LLR-403 and TC-480; the symbol anchor, IF-117 and
  the CodeSymbol crosscheck retire with the cells. `trace.py
  --regen-evidence` generates the TC evidence column's test-file parts
  (LLR-406), changing none of the base's 412 cells.
  `migrate_carrier.py --llr-trace-cells` (LLR-407) removed the cells from
  this repository's 351 rows; the RESYNC entry gives adopters the steps.
  <!-- fig: cmd="kitlib.spine.llr_placement over the registries; arch_tags.evidence_regen over git archive 3002931c7; migrate_carrier.py --llr-trace-cells" rev="19749ec70 (the evidence count at 3002931c7)" -->
- **Merge** (`8e7d43c6f`): `refactor_again` at `73aa095ce` (WI-1042,
  WI-1048), trunk's text and status kept in every design row with the three
  cells stripped, both lanes' test cases and RESYNC entries kept, trunk's
  first; this row's entry re-anchored at `73aa095ce`.
- **Held**: the operator's batch act over the 344 accepted design rows; no
  status moved, no snapshot taken.
- **Deviations**: the column map keeps the retired names (D-003); the
  evidence command is not a regen step (D-001); the OKF line and the brief's
  meta retire (D-002); the stage's before-side and the id sweep read history
  without the key rule; the old-kit re-sync test models the vocabulary
  migration, the `Area` deletion and the new arm.
- **Ratchets**: `trace.py` 3780 -> 3788, `intake.py` 1939 -> 1946,
  `check_trajectory.py` 1656 -> 1663 (reviewed bumps), `gen_arch_map.py`
  1671 -> 1654; the smoke tier's `max-tests` 3720 -> 3740.
- **Byte deltas**: `PROCESS.md` +101 (102,060), `PROCESS_OPTIONS.md` +147
  (202,593), the byte-budget skill -20 (4,603).
- **Tests**: red first `5 failed in 0.68s`, green `5 passed in 8.08s`; the
  full suite `66 failed, 8199 passed, 31 skipped, 18 warnings in 7363.62s
  (2:02:43)` (scripts edited under a running dispatch suite, fixtures of the
  old shape, two readers of history), then the affected modules `1 failed,
  1579 passed, 1 skipped, 18 warnings in 1038.10s (0:17:18)` (a stale stage
  pin, `31 passed` after the regeneration); after the merge `797 passed, 1
  skipped, 18 warnings in 260.45s (0:04:20)` and smoke `3721 passed, 3
  skipped, 18 warnings in 100.13s (0:01:40)`.
  <!-- fig: cmd="python -m pytest -q -n auto (and the module reruns the Deliverable lists); python project-trajectory/scripts/run_menu.py smoke" rev="the worktree ahead of 19749ec70; 8e7d43c6f" -->
- **Review**: round 1, Sol in two halves (four MINORs, one raised MAJOR and
  regraded) and Hydrogen APPROVE, plus two coordinator findings from the
  second adjudication sitting's rule against amendments that add code
  names; all six answered in `4c105adf0`; round 2 narrow, both APPROVE. The
  record is in the Deliverable.
