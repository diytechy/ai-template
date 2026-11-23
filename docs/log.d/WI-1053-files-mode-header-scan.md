## 2026-11-22 — WI-1053: in files mode the one-contract-body check reports itself dormant; LLR-398 says why headers are not scanned alone

Deferred open items: none. The row pins a report that already existed and
amends one row's text; it takes no operator decision and needed no
decisions record.

Built on the maintenance branch `maint/wi-1053` from `3c33b3783`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1053-files-mode-header-scan.md`).

- **The report existed; no code changed.** With no scan surface (files
  mode, or the declared source root absent) and at least one interface
  row, the trajectory check already printed one warning counting the rows
  whose contract bodies went unchecked and naming why, plain and under
  strict checking alike, with no exit-code change. Nothing tagged it and
  no row stated it. With no interface row it stays silent, which is
  SR-159's vacuity where an optional inventory is absent.
- **TC-504** (new, Drafted, minted from the lane's range; the TC mark
  rose to 504): one new test drives the check over a listed header's
  second body in symbols mode with the root present, in files mode and
  with the root absent (plain and strict), with the check off and with no
  interface row. It was red under four mutations of the report's arms,
  each reverted.
- **LLR-398** (Accepted; Detail and Rationale, so it drifts): the Detail
  states the dormant report and its bound; the Rationale says why listed
  headers are not scanned alone in files mode (a partial surface). No code
  name added. `test_refs` gains TC-504.
- **Tests:** the module holding the new test and TC-474's, TC-463's
  module, ten registry readers and the three whole-tree tests:
  `560 passed, 1 skipped, 18 warnings in 756.10s (0:12:36)`.
  `trace.py --strict`: `orphans=0 integrity=0`; `check_trajectory.py
  --strict`: clean. `run_menu.py smoke`:
  `3724 passed, 3 skipped, 18 warnings in 353.32s (0:05:53)`, with a CPU
  budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `low-level-requirements.toml` +861, `test-cases.toml` +1,335.
- **Acts owed:** LLR-398's amendment (Detail, Rationale), its `test_refs`
  traced change, and TC-504's first acceptance.
- **Review:** round 1, Hydrogen APPROVE; Sol one MINOR, dismissed
  (TC-504's generated `evidence` cell names its test by definition; the
  no-code-names rule covers prose cells). The record is in the
  Deliverable.
