+++
id = "WI-592"
title = "spot-check the clean close of WI-588 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

THE SHIPPED WORK MATCHES THE ROW. All three items WI-588 was asked for shipped,
and the one that carried the weight is genuinely driven. The close stands; one
residual is drafted as a successor below.

RE-DRIVEN, NOT READ. WI-588's whole subject was a cell that read true while
nothing drove it, so reading its deliverables off the cells would have repeated
the error it was sent to correct. The mutation was re-derived at this tip and
reverted (`git diff` over `trunk_step.py` empty). Baseline
`tests/test_trunk_step.py` `18 passed`. With the entire `verdict-rollup` tuple
deleted from `trunk_step.REGEN_STEPS` — module valid, zero occurrences left —
the file runs `1 failed, 17 passed`: the single red is
`test_regen_really_writes_the_verdict_rollup`, failing on the arm that names the
step that stopped running. `TC-206`'s four PRE-EXISTING evidence nodes run
`4 passed` under the same mutation, so WI-588's account of what stays green is
accurate and the file is no longer blind end to end.

The two cells carry what the row demanded: `TC-206.method` states the driven arm
and why no existing arm can see it, `TC-206.evidence` cites the node, and
`LLR-208.detail` names the `verdict-rollup` id, its `docs/reviews/` guard, its
LEAF position, and membership-as-contract. Both rows now read `Approved` where
WI-588's deliverable said `Drafted` — the adjudication minted at its merge, not
drift.

THE ONE RESIDUAL. `LLR-208.detail`'s WI-588-added clause "skipped with a printed
notice wherever that directory is absent" is TRUE but undriven: both arms that
could assert it enumerate a five-name SAMPLE of the regen steps and neither
includes `verdict-rollup`. Same class of gap, one scale smaller, introduced by
the amendment that closed the larger one — and the sampling means every regen
step added since those arms were written inherits the same silence. Drafted as a
successor rather than fixed here, because the remedy is a generalization over
the whole table and this lane is a spot-check.

Harness: full unfiltered suite driven at the close tip, result in `docs/log.d/`.
No source file changed by this WI.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-588-llr-208-tc-206-return-verify.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Dispositions

```toml
title = "drive the trunk regen step table WHOLE instead of sampling five names — the printed skip and the declared order"
workstream = "process"
buildtier = "medium"
specref = "docs/requirements/low-level-requirements.toml"
```

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
