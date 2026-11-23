## 2026-11-22 — WI-1050: WI-1049's verdict answered: LLR-257 re-amended without code names, TC-457, TC-468 and TC-475 made ready

Deferred open items: none. The row changes spine text and one test module
and takes no operator decision; it needed no decisions record.

Built on the maintenance branch `maint/wi-1050` from `5d3a7c52c`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1050-answer-wi-1049-verdict.md`).

- **LLR-257** (Accepted; Detail, drifting): WI-1042's amendment at
  `468c91fd9` re-landed (the acceptance-record reading, the re-pointing
  date, the cut rule, the gap rule) with no code file, function, module or
  symbol named, and the bare `(D3)` replaced by what the cut rule is: no
  reader is kept for an earlier spelling of the record, whose history is
  cut cleanly rather than translated.
- **TC-457** (Drafted): a new test drives a path that cannot be read and a
  file that cannot be decoded, each as a Python module and a shell script,
  through the component reader; each reads as absent and nothing raises.
  Method, Expected and the regenerated Evidence name the case.
- **TC-468** (Drafted): its Method says how each act is taken in contract
  terms, without the snapshot function's name.
- **TC-475** (Drafted) keeps only the failing-test case; the thirteen tests
  of TC-428 and TC-429 carry only their own tag; TC-428 and TC-429
  (Accepted) add LLR-395 to `Verifies`, no other cell changing.
- **Tests:** the three modules holding the five cases' tests, four registry
  readers and the three whole-tree tests:
  `399 passed, 1 skipped, 18 warnings in 118.73s (0:01:58)`.
  `trace.py --strict`: `orphans=0 integrity=0`; `check_trajectory.py
  --strict`: clean. `run_menu.py smoke`:
  `3724 passed, 3 skipped, 18 warnings in 144.86s (0:02:24)`, with a CPU
  budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `low-level-requirements.toml` +1,093, `test-cases.toml` -2,106.
- **Acts owed:** LLR-257's amendment, TC-428's and TC-429's `Verifies`
  change, and the first acceptance of TC-457, TC-468 and TC-475, beside
  F-3's LLR-244 amendment.
