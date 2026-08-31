## 2026-08-30 — WI-538: arm the complexity sensor here, re-base the module-size ratchet to SLOC (OI-68 phase 2, ruled 1c)

**Summary.** Executes phase 2 of the OI-68 complexity-sensor program at the shape
the owner ruled on 2026-08-30 — **1c / 2a / 3a / 4a**, NOT the driver's recommended
1a. The ruling is on record in `docs/requirements/open-items.toml`
`[open_item.OI-68]` (`status = "ruled"`). Because it landed 1c, phase 2 is
**arm + re-base**, never arm + retire: both sensors stay armed, nothing is
deleted, no pointer moves.

Three acts, in one direction:

1. **Arm (3a).** A new `[step:complexity]` in `docs/stack.ini`
   (`layer = product`, `from-stage = DevStg-Impl`) runs
   `check_complexity.py --root . --mode enforce` — the exact-equality compare, in
   both directions, nonzero on either. SR-183 already carries both postures in one
   row ("gated only where a repo opts in"), so arming mints NO new spine row; the
   opt-in is the step's presence in `docs/stack.ini`. Report-only stays the
   shipped default (that ships in phase 3, a separate WI).

2. **Scope (2a).** The sensor's census surface widens to `tests/` as well as
   `project-trajectory/scripts/` — `DEFAULT_INCLUDE` in `check_complexity.py`, the
   single home of this repo's census surface — and `docs/complexity-baseline` is
   re-stamped to seed the ~20 `tests/` functions over the threshold. The line
   ratchet stays scripts-only, per the ruling.

3. **Re-base (1c).** `tests/test_module_size_ratchet.py` is re-based from raw
   physical lines (`len(text.splitlines())`) to **SLOC** — non-blank, non-comment,
   non-docstring — the definition held once beside the sensor
   (`check_complexity.module_sloc`) and imported by the ratchet, so the two sensors
   share one definition of a source line. `THRESHOLD` re-based 1500 → **1000 SLOC**
   and the `BASELINE` dict fully re-stamped to SLOC values (derivation below).
   Nothing deleted: the file, its `[generated]` `linecounts` row, its
   `OTHERWISE_ENFORCED` entry, and WI-521's debt-owner pointer all stay.

**Threshold derivation (1500 raw → 1000 SLOC).** Measured at this branch's base
over `project-trajectory/scripts/`: the 9 modules the raw-1500 ratchet baselined
score 1081–3364 SLOC (`intake.py` the smallest member at 1081); the largest
NON-member is `traj_panels.py` at 891 SLOC. A SLOC threshold anywhere in 900–1000
preserves EXACTLY those 9 modules — a 190-line clean gap — so 1000 is the round
choice that re-stamps the current watch set onto the code axis without deleting an
entry or admitting a new one. This is the "one-time full re-stamp with the
derivation on record" the ruling names.

**Not touched, deliberately.** OI-68 is already flipped `ruled` (done at the
sitting), so no `open-items.toml` edit and no `gen_open_items` regen. The
`linecounts` freshness-wiring kind is left as-is — it is an internal join key and
SLOC is still a source-line count; the axis definition lives in the ratchet's own
docstring. `test_import_layers.py` / `test_agent_loop.py` docstring references to
the ratchet stay valid (the file stays); only `traj_context.py`'s pinned
"1,500-line threshold" is generalised, since that number is now stale.

Deferred open items: none — the ruling (OI-68) is on record and this phase
executes it; it files no new question.

**Rework (REVIEW-A, MINOR, addressed 2026-08-30).** The review found the ratchet's
re-based module docstring still asserted the two sensors "cover the same files …
and differ only in what they measure" — false once 2a widened the complexity
sensor's `DEFAULT_INCLUDE` to `tests/` while this ratchet stayed scripts-only
(`conftest.SCRIPTS`). Corrected the docstring to state that the shared
`check_complexity.module_sloc` source-line definition is the ONLY axis the two
sensors hold in common: they diverge in BOTH what they measure (module SIZE vs
function COMPLEXITY) AND which files they cover (kit scripts only vs scripts +
`tests/`). Docstring-only; no predicate moved, ratchet + complexity tests still
green.

**Rework (REVIEW-A, MAJOR + MINOR, addressed 2026-08-30).** LLR-206 had
retained WI-537's report-only wording as though it described this repository,
contradicting the armed `docs/stack.ini` step delivered here. Its contract now
distinguishes the downstream template's report-only default from this
repository's `DevStg-Impl` enforced step and its scripts-plus-`tests/` census.
The baseline writer now emits a blank reason as four TSV fields, and the 20
newly seeded `tests/` rows were normalized accordingly; a regression assertion
prevents a restamp from recreating trailing whitespace. The reader remains
backward-compatible with historical five-field blank-reason rows.

**Verification.**

- **Arming (3a).** `check_complexity.py --root . --mode enforce` →
  `OK - 200 row(s) over 15, unchanged from baseline.`, exit 0.
- **Re-base units (1c/2a).** `tests/test_module_size_ratchet.py` +
  `tests/test_check_complexity.py` → 50 passed.
- **Commit bar.** `pytest -q -n auto -m smoke` → 1427 passed, 6 skipped (43.9s);
  `check_smoke_budget.py --mode enforce` → 38.1s vs 60s budget, within, exit 0.
- **Full unfiltered suite — GREEN, run in three disjoint file-partition batches**
  (the box was loaded past the 10-min single-shot timeout — the two prior resume
  sessions, iteration logs 003/004, were each reaped mid-single-shot-run with the
  background suite killed on teardown, which is why this row stayed open; the
  batched form is the standing fallback for that): fast in-process modules (74)
  1427 passed / 6 skipped; slow subprocess/scaffold modules split 35 + 36 → 907
  passed / 2 skipped and 857 passed / 8 skipped. **Union: all 145 test files, each
  run exactly once — 3191 passed, 16 skipped, 0 failed.**
