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
