+++
id = "WI-652"
title = "Re-tier the per-commit smoke tier until it runs within 60 s on this 4-core box, keeping it representative"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

The per-commit smoke tier fits its unchanged 60 s budget on this repository's
4-core / 8-thread box. Three quiet runs of `python scripts/check_smoke_budget.py
--mode enforce` gave **26.4 / 26.4 / 25.7 s**, 1555 passed and 3 skipped each.
The tier was 188 s quiet before the change. It holds 1558 of 4267 collected
tests, down from 1953. Nothing was deleted: every test still runs in the full
suite, and 13 new direct pins were added.

- **What moved:** 16 heavy modules, plus six heavy cases split into slow
  siblings (`*_driven`, `test_dogfood_widening`), joined `SLOW_MODULES`, each
  with its reason and loaded cost. Together they were 85% of the tier's
  per-test cost under load.
- **Representativeness (the owner's condition on OI-92 (b)):** every kit
  script family keeps an in-process test in the tier. Scripts whose tests
  were all heavy keep a direct pin of their pure seam: `test_trunk_step_plan`,
  `test_gen_open_items_render`, `test_generated_freshness_census`,
  `test_handback_records`, `test_check_figures_rules`,
  `test_check_need_form_rules`, `test_verdict_rollup_render` and
  `test_gen_trajectory_splice`.
- **Tier cells kept true (arbitration ruling 4(ii)):** TC-135, TC-164,
  TC-170, TC-178, TC-192 and TC-206 have `tier` amended from Smoke to Full in
  place, left Approved, for the joint adjudication WI-669. TC-157 and TC-245
  keep fast evidence and stay Smoke. The thirteen older mismatches, and a
  check that would catch the class, are WI-672.
- **Declared figures:** the membership ceiling `max-tests` drops 2030 → 1620,
  about 4% over 1558. CLAUDE.md and the session-protocol skill carry the new
  figures (CLAUDE.md +2 bytes, now 7,977 of 8,500). The `fig:` markers for
  the count and the seconds are stamped against this item's landing commit in
  the next integration commit, the stack profile's established pattern.
- **Review:** Sol's first round (the measurement, which the integrator had
  reserved for landing; the Smoke evidence; representativeness) was ruled in
  arbitration ruling 4. The fix round was SOUND.

## Context

OI-92 ruled 2026-09-26: option (b), re-tier. The 60 s budget in `docs/stack.ini` `[smoke-budget]` stands and is not moved to fit the box; the tier's membership changes. Today the tier runs 188 s quiet on this 4-core, 8-thread box (spine map D10), so every commit records the seconds FAIL and a real regression is invisible.

The owner's condition: "as long as the 'smoke-test' is representative, it should be okay. Is saving 4 minutes each commit worth it? It may not be, but I'm willing to try it." So: profile the tier (`--durations`), move the heaviest modules into `tests/conftest.py` `SLOW_MODULES` (or mark heavy cases), and keep at least one in-process test of every kit script family in the tier; argue each dropped module in the log. Measure the tier quiet three times on this box with nothing else running and record the three figures (declared-figure convention). Update CLAUDE.md's and the session-protocol skill's measurement lines to the new figures and name the box, re-stamp `tests/test_smoke_budget.py`'s membership ratchet deliberately, and record that this is a trial the owner may revisit.

## Done-when

- Three quiet runs of `python scripts/check_smoke_budget.py --mode enforce` on this box pass under 60 s, their figures recorded with the producing command and revision.
- Every kit script family keeps at least one test in the smoke tier; the log names each module moved out and why.
- CLAUDE.md and the session-protocol skill carry the new measurement; the membership ratchet is re-stamped with the reason; the full suite still collects every moved module.
