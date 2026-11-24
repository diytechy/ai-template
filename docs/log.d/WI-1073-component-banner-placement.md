## 2026-11-24 — WI-1073: the component view's header states placement through `constrains` too

Built on `maint/wi-1073` (cut from `refactor_again` at `d1571e8fc`) with no
plan (`planmode = "none"`). The spec's Deliverable holds the per-item record.

- **What changed.** The generated component view's header, and the
  generator's module and build docstrings, now say a design row sits at the
  owner component of each interface its `constrains` cell names and of each
  interface a test case verifying it names, with `[unplaced] llr_refs`
  listing the rows placed by neither, as LLR-403 states. Before, they named
  the verifying test cases alone. The committed view is regenerated (its
  header lines only); where each row is placed is unchanged. The RESYNC
  entry is anchored `[since d1571e8fc]`.
- **Rows.** None changed; no id minted; no act owed.
- **Deviations from spec:** the build function's docstring, which carried
  the same stale sentence, is corrected beside the module docstring. At the
  coordinator's request, two test-module docstrings with the old wording
  (`tests/test_gen_components.py`, `tests/test_llr_trace_cells.py`) now
  describe placement through `constrains` and through the verifying test
  cases; docstrings only, the two modules `44 passed in 5.54s`.
- **Byte deltas on budgeted files:** none (no budgeted file touched).
- **Tests:** red first `1 failed, 18 deselected in 8.18s`; the 13 importer,
  spine-linked and named modules `309 passed, 2 skipped in 62.41s`;
  `trace.py --strict` exit 0 and `check_trajectory.py --strict` clean;
  `run_menu.py smoke` exit 0, the tier `3956 passed, 3 skipped, 18 warnings
  in 254.02s` (its CPU-seconds over `[smoke-budget]`, a warning for the
  audit).
