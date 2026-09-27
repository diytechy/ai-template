+++
id = "WI-652"
title = "Re-tier the per-commit smoke tier until it runs within 60 s on this 4-core box, keeping it representative"
workstream = "process"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

OI-92 ruled 2026-09-26: option (b), re-tier. The 60 s budget in `docs/stack.ini` `[smoke-budget]` stands and is not moved to fit the box; the tier's membership changes. Today the tier runs 188 s quiet on this 4-core, 8-thread box (spine map D10), so every commit records the seconds FAIL and a real regression is invisible.

The owner's condition: "as long as the 'smoke-test' is representative, it should be okay. Is saving 4 minutes each commit worth it? It may not be, but I'm willing to try it." So: profile the tier (`--durations`), move the heaviest modules into `tests/conftest.py` `SLOW_MODULES` (or mark heavy cases), and keep at least one in-process test of every kit script family in the tier; argue each dropped module in the log. Measure the tier quiet three times on this box with nothing else running and record the three figures (declared-figure convention). Update CLAUDE.md's and the session-protocol skill's measurement lines to the new figures and name the box, re-stamp `tests/test_smoke_budget.py`'s membership ratchet deliberately, and record that this is a trial the owner may revisit.

## Done-when

- Three quiet runs of `python scripts/check_smoke_budget.py --mode enforce` on this box pass under 60 s, their figures recorded with the producing command and revision.
- Every kit script family keeps at least one test in the smoke tier; the log names each module moved out and why.
- CLAUDE.md and the session-protocol skill carry the new measurement; the membership ratchet is re-stamped with the reason; the full suite still collects every moved module.
