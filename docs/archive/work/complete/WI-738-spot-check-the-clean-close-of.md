+++
id = "WI-738"
title = "spot-check the clean close of WI-736 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

**CONFIRMED.** What shipped answers WI-736: the three replacements landed
verbatim, nothing else in either registry moved, and no code changed. The
record is
[001-SPOTCHECK-5b75c39a.md](../../../reviews/wi-738-spot-check-the-clean-close-of/001-SPOTCHECK-5b75c39a.md),
written by an independent Opus spot-checker.

- **Runs:**
  - the session modules ran `105 passed`;
  - a probe of the plain adapter over gemini results, in three shapes and
    under three argv forms, found everything unread left empty.
- **Observations**, passed to batch J's sitting adjudicator (WI-737) as
  chain evidence:
  - SR-227's "one bounded turn" holds only on the claude adapter;
  - its "by one writer" is stricter than the lock-free tombstone, and a
    0.5 s lock wait sits in the tick;
  - an unread runner's conversation id fills from `session_id`;
  - `adapter_for` matches by prefix.
- **Not filed:** no new row.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-736-batch-i-returns-bound-sr-222.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.
