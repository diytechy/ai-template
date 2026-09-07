# Control retry: adjudication review boundary

**Scope:** read-only audit of the second stopped-control seam. This note does
not change policy or prescribe a repair.

## Finding

The `when-minting` predicate skipped the review round for candidate
`fa90a5b73ead04ee8dfbf151a53eeca5cddf1c86`, although its second
`## Dispositions` successor will be minted as `high-risk`.

The log records the resulting decision at
`out/run-logs/control-retry-approval/launcher.log:43`: “adjudication review
not owed … when-minting”. Candidate `fa90a5b7` contains two valid draft
blocks. The first has no declared class and is normalized to `ordinary`; the
second has `planmode = "dual"` and no declared class.

`intake.parse_dispositions` derives its returned `kind` only from
`safety_class`, or `ordinary` when the plan is not dual
(`scripts/intake.py:1252-1255`). It therefore returns
`["ordinary", ""]` for this candidate. Both the coordinator
(`scripts/agent_loop.py:2996-3004`) and the primary approval reader
(`scripts/primary_approval.py:378-384`) pass only that list to
`agent_common.adjudication_review_owed`.

Under the configured `[attestation]` value
`adjudication_review = "when-minting"` (`docs/process.toml:157-166`), that
shared predicate owes a round only for `spine` or `high-risk` returned
classes, or a `consolidate` brief
(`scripts/agent_common.py:1061-1067, 1114-1123`). It consequently returns
false for this candidate.

Later, the primary close passes the same parsed draft through
`intake._disposition_draft` and `intake.stage_mint`
(`scripts/primary_close.py:325-332`,
`scripts/primary_publication.py:46-54`). The minted row preserves
`PlanMode = dual`. The scheduler, whose classification is authoritative for
the minted row, derives `high-risk` whenever `planmode == "dual"` and the
declared class is empty (`scripts/schedule.py:342-348`). Thus this is a
concrete predicate/input-shape mismatch: review scheduling sees the
pre-mint raw normalized field, while the work that is actually minted receives
the derived high-risk class.

## Reproduction

Read-only evaluation of the candidate’s disposition text produced:

```text
parsed kinds: ["ordinary", ""]
adjudication_review_owed(docs, "amendment", parsed kinds): False
minted classifications: ordinary, high-risk
```

No mocked review checker or modified candidate was used.

## Limits

This establishes the missed `when-minting` review for the existing
WI-605 candidate and the same primary publication path. It does not assess the
separate candidate-SHA mismatch that stopped the retry, whether a later
publication reaches `stage_mint`, or whether either drafted successor is
otherwise mintable under all intake checks. The current policy itself is
unchanged: its documented trigger already says a `high-risk` successor owes
a round. The seam is the discrepancy between the review reader’s draft
classification and the mint/scheduler’s derived classification.
