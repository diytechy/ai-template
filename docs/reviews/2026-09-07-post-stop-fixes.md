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

## Item 4 — retain the lock hold and document its actual scope

Keep `integrate.lock` held across the provider session. It protects the whole
primary turn against a competing process; releasing and retaking it would add
a gap and another acquisition without a demonstrated throughput need in this
exclusive station. The durable pending selection remains the protection
between processes and after interruption.

Source review traced both callers and the POSIX/Windows non-blocking lock
implementations. The corrected `_slot` docstring states that primary holds may
last minutes, merge refresh can occur under the lock, contenders refuse rather
than wait, and claims/intake/generators do not take this lock. It removes the
false sub-second promise and distinguishes the pending-record refusal from the
OS lock. No runtime behavior changes; no new tests for a docstring correction.

## Item 5 — one owner for the absorption census

Cancel [WI-596](../archive/work/cancelled/WI-596-the-anchoring-copy-s-absorb-le.md)
as superseded by primary approval repair `0f106ce9`. This is the explicit
closure option authorized by resume item 5, not a claim that its original
implementation plan shipped. Preserve its Context and record the disposition
in its terminal Deliverable. No live WI has a dependency on this row.

The current ownership, checked in source:

| Superseded proposal | Current home |
|---|---|
| Whole-file changed-row population | `primary_approval.absorption_census`, shared by briefing and publication verification |
| First-approval brief's absorb ledger | `adjudicate_brief._primary_absorption_text` renders the common primary envelope, including the specialized first-approval brief |
| Durable record of absorbed cells and their judgments | The committed `## Approval` payload's typed `[[absorption]]` tables; publication preserves the carrier in the terminal spec |
| Hold an unjudged absorption before copying | `_absorption_refusal` compares the exact census, requires accepted scoped decisions and checks judgment references; `_absorption_shape` refuses `UNJUDGED` |

The old standalone brief placeholder, `acceptance_record` ingestion and
rollup/intake consumption design are retired by this disposition. They were
not implemented as specified. The current brief supplies cell/blob identities;
the adjudicator supplies judgment references in the typed payload. The human
rollup remains a generated reading of review rounds, not another approval
record. Whole-file snapshot granularity is unchanged. No new census or
approval-consumer route is introduced.

Existing tests exercise shared-census briefing, every registry carrier,
unjudged absorption and the exact ledger requirement. This cancellation changes
queue state and documentation only; it approves none of the historical rows
mentioned in the old WI. Navigable links follow the archived spec; historical
invocation metadata, findings and source-path quotations remain untouched.

## Stop boundary

Resume items 1–5 are addressed in separate commits with their source reviews
and per-commit verification recorded in [the session log](../log.md).
The pending primary writer is clear, the pause remains tracked, and the
coordinator stays stopped. Package PC is next authorized work and has not
started. No further control window, push or merge to main is authorized here.
