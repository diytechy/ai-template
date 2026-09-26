+++
id = "WI-602"
title = "spot-check the clean close of WI-580 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = "docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md"
buildtier = "medium"
safety_class = "adjudication"
+++

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Done-when

- The row's `## Deliverable` answers its one question, whether what WI-580
  shipped answers what WI-580's row asked for, item by item, each answer citing
  the code, test or document it was checked against.
- Each finding is drafted as a successor in this spec's `## Dispositions`
  section, with an `open_item` cell where the answer is the owner's; none
  reverses the close.
- With no finding, the Deliverable says the close stands and on what evidence.
