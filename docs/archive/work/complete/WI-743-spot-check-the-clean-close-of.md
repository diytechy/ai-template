+++
id = "WI-743"
title = "spot-check the clean close of WI-740 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

**FOLLOW-UP, with no new row.** What shipped answers WI-740: the code, the
verbatim registry edits and the out-of-scope list all hold. The twin test
fails against the pre-fix code, run in a scratch copy. The record is
[001-SPOTCHECK-3ecef627.md](../../../reviews/wi-743-spot-check-the-clean-close-of/001-SPOTCHECK-3ecef627.md),
written by an independent Opus spot-checker.

- **The finding:** `KeepWarmer.__init__` now builds every routing row's
  argv. On Windows, `build_argv` refuses a `{prompt}` row behind a
  `.cmd`/`.bat` shim, such as the template's own gemini row. So with the
  keep-warm dial on, the dispatcher fails at start. This was reproduced.
- **Not filed separately:** batch K's adjudicator found the same defect
  independently and drafted it in WI-741's Dispositions. That draft is the
  one successor.
- **Observations:**
  - a non-bounding route's expired lease now retires at the next
    `keep_for`;
  - a misleading "ping in flight" skip line (read from the code, not run).

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-740-keep-warm-only-a-route-whose-r.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.
