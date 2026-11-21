## 2026-11-21 — WI-1019: LLR-395 states WI-1001's rule that an accepted automated test case no test file declares is a finding

Deferred open items: none. The acts owed go to automated adjudication,
which the operator-acceptance dial releases. The re-point of TC-428 and
TC-429 is WI-1038's, and this session took no operator decision.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1019` from `d849667f1`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1019-tc-untagged-rule-llr.md`).

- **LLR-395** (`43795aa29`), `Drafted` under SR-157, in contract voice and
  naming no code. It states which live test cases owe a test-file
  declaration (`Accepted` or `Founded`, automated reading yes), and that the
  Evidence cell changes nothing. A refused declaration declares nothing. It
  also states the unreadable-file exclusion, vacuity and the parse stop, and
  severity by strict checking and rung. Its cells follow LLR-366
  (CMP-006, phase 6, `test_refs` "TC-428; TC-429"). The watermark moves
  LLR 394 -> 395.
- **Deviation from the spec, by the coordinator's ruling:** the parent-first
  rule refuses an `Accepted` test case verifying a `Drafted` LLR, both in
  `trace.py --strict` (2 integrity findings) and at the hook. So TC-428 and
  TC-429 stay unchanged here, and their re-point is WI-1038's, after
  LLR-395's first acceptance. The spec's Context and Done-when say so.
- **The code tag:** the function applying the rule now carries
  `Implements: SR-157, LLR-395`. The commit checks' RESYNC check owed an
  entry for that shipped file, so one was added with nothing forced.
- **Tests:** the 24 modules reading the rows and the module:
  `886 passed, 2 skipped in 193.93s (0:03:13)`. The pack's 8 readers:
  `102 passed in 58.75s`. `test_bootstrap.py -k "byte_caps or size_budget
  or baselines"`: `3 passed, 71 deselected in 0.37s`. `run_menu.py smoke`:
  `3698 passed, 3 skipped, 18 warnings in 350.93s (0:05:50)`, with a CPU
  budget WARN only. `trace.py --strict`: `orphans=0 integrity=0`;
  `check_trajectory.py --strict`: clean. The unfiltered suite was not run.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** `RESYNC_PACK.md` 733,993 -> 734,651 (unbudgeted).
  No budgeted file was touched.
- **Acts owed:** LLR-395's first acceptance; then WI-1038's re-point and
  its drift on TC-428 and TC-429.
- **Review:** round 1 over `d849667f1..9fe88b282`, Sol (low) on the whole
  diff and Argon (low) by file reference: both APPROVE, no findings.
