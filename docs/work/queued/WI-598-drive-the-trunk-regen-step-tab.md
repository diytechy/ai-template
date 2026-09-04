+++
id = "WI-598"
title = "drive the trunk regen step table WHOLE instead of sampling five names — the printed skip and the declared order"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

Drafted by WI-592 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`tests/test_trunk_step.py` asserts the regen table through two arms that each
enumerate a hand-written SAMPLE of five step names — `okf`, `derived-stage`,
`trajectory`, `status`, `open-items`. `test_regen_skips_absent_artifact_families`
asserts the printed skip for those five; `test_regen_runs_in_declared_dependency_order`
asserts the executed order over the same five. Every step added to
`REGEN_STEPS` since those lists were written is outside both, and a step added
next is silent by default rather than by decision.

The immediate instance found by WI-592's spot-check: `LLR-208.detail` claims the
`verdict-rollup` step is "armed by the presence of `docs/reviews/` and skipped
with a printed notice wherever that directory is absent". The claim is true —
`regen()` on a bare tree prints `trunk_step: regen — skipping verdict-rollup
(docs/reviews/ absent).` — and nothing asserts it. That is the same shape WI-588
was sent to close one rung up, so fixing it by appending one name to a list
would leave the mechanism that produced it intact.

IN SCOPE — make both arms read the table rather than a literal list: every
`REGEN_STEPS` row is asserted to print either its `ok` line or its named skip on
a bare scaffold, and the executed order is asserted to be the DECLARED order
across all rows, not a sampled subsequence. Keep the arms cheap; they run on an
empty tmp tree today and should stay there.

NOT IN SCOPE — any change to `trunk_step.py` itself, or to the
`verdict-rollup` step: nothing is wrong with the mechanism, only with what
observes it. Whether `TC-206.method` needs a sentence for the widened arm is the
successor's call after the test lands; `TC-206` and `LLR-208` are `Approved`, so
any cell edit is a re-draft and an approval act belongs to the adjudication that
follows, never to the lane.
