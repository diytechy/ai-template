# Post-stop repair source reviews

These reviews cover the bounded fixes in the
[resume prompt](../handoff-2026-09-07.md#resume-prompt-2026-09-07-after-the-stop).
They are the implementing supervisor's source reviews and regression evidence,
not independent provider verdicts or judgments of disputed spine cells.
The [retirement review](2026-09-07-primary-turn-retirement.md) covers item 1.

## Item 2 — exact candidate identity

Root cause: the invocation binding accepted a display-oriented abbreviated SHA
from the session's commit-range reporting. The verifier requires a full commit
identity. `primary_adjudication.session_binding` now reads
`agent_common.head_sha_full` itself; its caller cannot pass an abbreviated
candidate. The single caller in `agent_loop.run_iteration` uses that interface.
Ordinary range reporting retains its existing representation.

The existing real-Git RETURN test now obtains metadata from the production
binding function, commits it as telemetry, and checks that the primary verifier
resolves the actual judgment record and allows completion. Before the fix its
candidate equality assertion failed on the abbreviated SHA. This replaces the
hand-written full-SHA fixture that missed the integration error. No historical
invocation file changes, no relaxed verifier and no new compatibility path.

## Item 3 — resolve the successor's scheduled class before review

Root cause: `parse_dispositions` returned an empty `kind` for an undeclared
dual draft. Review consumers saw that empty value, while `schedule.kind_of`
later derived high-risk. Review consumers now read `intake.draft_kind`, which
adapts the parsed draft to that existing scheduler resolver. The engine,
integration gate and primary approval all use it; no review-policy change or
second risk-class rule is introduced. Minting retains the original authored
cells, including the intentionally empty class beside dual.

Two regressions now omit `safety_class` entirely beside `planmode = "dual"`:
one drives the actual review scheduler and requires REVIEW-A; the other drives
primary approval and requires refusal when the independent review is absent.
Both failed before the fix. Existing tests continue to cover declared classes,
the never/always dials and invalid class/dual combinations. The existing mint
regression caught the initial attempt's redundant explicit high-risk cell;
preserving its assertion keeps the derivation in the scheduler alone.

The module-size check caught the adapter's growth. Accepted and re-stamped
`intake.py` from 1455 to 1459 SLOC: the adapter replaces raw-class reads at
three consumers and delegates all classification policy to the existing
scheduler. A separate module for this mapping would add a new home without
removing behavior. The threshold and every other module baseline stay intact.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_module_size_ratchet.py" rev=9fa88ddc+resume-item-3; out/run-logs/post-stop-repair/3-bar.txt; 3-ratchet.txt -->
