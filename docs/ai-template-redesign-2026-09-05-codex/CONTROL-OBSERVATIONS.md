# Short control observations

Operating envelope: [owner ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06).
Preparation and live route probes: [preflight](CONTROL-PREFLIGHT.md).

## Launch

Awaiting the hooks-enabled pause-deletion commit; no coordinator observation
has occurred. The supervisor records the exact commit and UTC start before
reporting any running interval. WI-551 remains deferred through the window.

## Recording and stopping

The supervisor follows the launcher output and existing invocation, review,
integration and Git records. For each completed WI record its accepted
obligations, attempts, review rounds, interventions by reason, reported cost
or unavailable coverage, integration time and queue wait. Preserve incomplete,
partial and abandoned attempts as well. Required approvals and sampled reviews
are separate from defect-repair interventions. Do not sum ambiguous counters.

Count across launcher restarts, never reset the window at exit 11. Stop new
admission at the first ruled WI/day/coordinator-hour bound, recreate the
tracked pause and drain under current policy. The reported spend watch is not
an admission gate. A required runtime repair closes its measured segment;
record the old and new revisions before any later observation. A correctness
failure stops the affected path. Do not widen the window or silently substitute
another one if the sample is insufficient.

## Events

No control events yet. Preparation calls are recorded only in the preflight.
