# WI-538 — REVIEW-A (compiled)

The WI-level verdict the merge slot reads (RULING-7), compiled by the
supervising session from the round files below — ordered by commit time,
the governing verdict last. Every line is quoted from its round file;
nothing is judged here that a reviewer did not judge.

Excluded on purpose: `010-REVIEW-A-e26ab03.md` — written by the lane's own
BUILD session (gpt-5.6-terra, commit 189490e4 "review: record WI-538
re-review approval"), an implementer-authored file under the review path;
it is not a fresh-context verdict and does not count as a round.

## Round 1 — 006-REVIEW-A-7fe441e.md

- [MINOR] tests/test_module_size_ratchet.py:59 -> states that the size ratchet and complexity sensor "cover the same files," but this change keeps the former scripts-only while DEFAULT_INCLUDE adds tests/ to the latter -> correct the contract text to distinguish their coverage as well as their measurement axes -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 2 — 009-REVIEW-A-a9fb50e.md

- [MAJOR] docs/requirements/low-level-requirements.toml:2175 -> LLR-206 still normatively says no `[step:complexity]` is wired in `docs/stack.ini` and that enforcement is exercised only by the module tests, but this diff wires that exact enforced DevStg-Impl step; the requirement surface now contradicts the delivered gate and cannot support a coherent review -> amend LLR-206 to distinguish the report-only downstream template from this repository's opted-in enforced step (and its `tests/` census), then re-review the changed requirement -> @software-engineer
- [MINOR] docs/complexity-baseline:10 -> every newly seeded test-tree row with a blank reason ends in a tab, so `git diff --check` reports trailing whitespace for all 20 additions -> serialize blank reasons as four TSV fields (or remove the terminal tabs from these newly added rows) so the baseline remains parse-equivalent and whitespace-clean -> @software-engineer
VERDICT: CHANGES-REQUESTED findings=2

## Round 3 — 011-REVIEW-A-189490e.md

# WI-538 — REVIEW-A independent (2026-08-30)

**Scope.** `contract_split...HEAD` (base pinned at `ea28176f`) minus telemetry /
verdicts / generated artifacts: the arm (`docs/stack.ini` `[step:complexity]`),
the census widening (`check_complexity.DEFAULT_INCLUDE` + `docs/complexity-baseline`),
the SLOC re-base (`tests/test_module_size_ratchet.py`, `module_sloc`/`_sloc`
factor-out), the TSV serialization change (`write_baseline`), and the edited
`LLR-202` detail. (The base pointer was reset mid-review by a background loop; I
pinned the literal SHA to get stable diffs.)

**Drove the real paths.**
- `check_complexity.py --root . --mode enforce` → `OK - 200 row(s) over 15,
  unchanged from baseline`, exit 0. The armed gate matches the committed baseline.
- `module_sloc` over the live scripts tree returns EXACTLY the 9 baselined values
  (trace 3364 … intake 1081), largest non-member `traj_panels.py` 891 — so
  THRESHOLD 1000 preserves precisely the 9-module watch set, as the derivation
  claims.
- `pytest tests/test_module_size_ratchet.py tests/test_check_complexity.py` → 50
  passed. `check.py --jobs 0` → RESULT: PASS. `trace.py --strict-integrity` →
  integrity=0 (the LLR-197/provenance findings are pre-existing rows this diff
  does not touch). New `"\t\n"` assertion correctly fails on pre-fix behaviour
  (old writer always emitted a terminal tab for a blank reason).
- `SR-183` ("gated only where a repo opts in", both postures in one row) is
  consistent with the edited `LLR-202` detail — no spine contradiction.

**Done-when coverage.** Armed (3a) — verified by the enforce run + stack wiring;
scope reversion is pinned because the baseline's 20 `tests/` rows would report as
vanished under enforce. Scoped (2a) — 200 rows (180 scripts + 20 tests) confirmed.
Re-based (1c) — `test_module_sizes_exactly_match_the_committed_baseline` +
`test_module_sloc_is_the_whole_file_on_the_same_rule`, both green. No item
UNCOVERED.

**Findings.**

- [MINOR] docs/complexity-baseline:8 -> the committed baseline is in a MIXED serialization the tool's own writer would never emit: all 180 script rows still carry the pre-change trailing-tab blank-reason format (5 fields, empty `reason`), while only the 20 new `tests/` rows use the post-change 4-field format. A plain `--restamp` — the exact workflow `docs/stack.ini` documents ("Re-stamp with: … --restamp and review the DIFF, never the run") — rewrites 362 lines of pure trailing-whitespace churn, burying any real complexity delta and undermining the "review the DIFF" instruction on first use. The gate itself is unaffected (`read_baseline` normalizes both shapes; enforce passes). -> Run `check_complexity.py --root . --restamp` now and commit the normalized file so all 200 blank-reason rows are 4-field and the baseline round-trips through its own writer. -> @owner

VERDICT: APPROVE findings=1

## Round 4 — 012-REVIEW-A-f1d0fd6.md

- [MAJOR] docs/complexity-baseline:16 -> The re-stamp raises the already-armed cognitive baselines for `agent_loop.py::route_session` (35 -> 37) and `run_iteration` (17 -> 18), contradicting the baseline's downward-only contract and masking the divergences the new gate must reject -> Restore the prior ceilings and decompose the functions (or place a separately justified change under the applicable policy rather than raising this ratchet) -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 5 — 012-REVIEW-A-3275b37.md

## 2026-08-31 — WI-538 independent review A

- [MINOR] docs/complexity-baseline:10 -> The new blank-reason entry ends in a fifth, empty TSV field (and the same defect is repeated at line 24), contradicting the newly added `test_restamp_writes_lf_only_debt_headed_tsv` assertion that a blank reason serializes as four fields and causing `git diff --check` to report trailing whitespace -> remove the terminal tab from both blank-reason rows (or supply an actual reason) -> @owner
VERDICT: CHANGES-REQUESTED findings=1

## Round 6 — 012-REVIEW-A-4288c3f.md

VERDICT: APPROVE findings=0

## Governing verdict

The final round above governs:

    VERDICT: APPROVE findings=0
