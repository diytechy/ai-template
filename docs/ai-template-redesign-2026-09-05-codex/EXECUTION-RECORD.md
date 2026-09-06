# Execution record

Execution authorized by the owner on 2026-09-05, starting from `5645798c`
on `contract_split`. This is a supervised implementation sitting under
the [package boundaries](IMPLEMENTATION.md), with the existing unattended
queue paused. Package labels remain plan scope keys, not allocated WI IDs.

## Current scope

Start P0a's revisioned inventory and P0b's current-runner repairs:

- Resolve the resumed worker's evidence base from the existing Git claim.
  Exercise completion, assignment and review consumers after restarting on
  the lane checkout; retain explicitly unclaimed/manual compatibility.
- Detect loaded coordinator code moving and stop at a safe boundary before
  another provider session. Preserve the finished session's evidence and
  require a fresh process to load the changed code.
- Extend the existing session accounting boundary with invocation identity,
  route attribution and honest raw usage, including planning sessions.
  Absent or incomparable counters must not become zero or a summed total.
- Evaluate the additive smoke station step against the existing harness.
  It is a smoke regression check, not a claim that the full suite passed.

Each repair uses focused regression tests, the existing commit checks and
an intermediate adversarial review requested as `claude-opus-5`, high effort.
Any unavailable route or failed check is recorded explicitly. The owner's
standing permission to commit despite this computer's flaky smoke timing
does not change the declared budget or make a breached check pass.

## Remaining boundaries

The control workload, paid-run budget and observation window have not been
established. These repairs do not open the replacement packages P3–P8 or
unpause the loop. P0a remains incomplete until its obligation/scenario maps
and representative adopter evidence are recorded. Hat-context repair and
adopter revalidation remain independently justified follow-on slices; no
SN approvals, capability retirements or wholesale SR rederivations are
implied by starting these runtime fixes.

The [refreshed inventory](P0-INVENTORY.md) records the committed baseline,
queue identities and preserved work. Results, review dispositions and remaining
work are appended below as each slice is verified.

## First implementation slice

The durable base comes from the existing claim commit and its verified
queued-to-active move. Claim subject and Git-status parsing have one shared
home; no new assignment file is introduced. A missing legacy claim retains
the old fallback, while unreadable claim history refuses to proceed.

Runtime Python changes now produce process exit 11. The worker stops before
another provider session; the dispatcher preserves branches and drains
already-running children before it exits. An operator invokes the launcher
again to load the changed code. This is a process restart, not a partial WI
close or a new launcher retry policy. OI-83 and OI-84 record these dispositions
under the owner's execution authorization.

Workers, dual-plan roles, recovery probes and interactive launches share
invocation accounting and the existing bounded/redacted log writer. Each call
has an independent ID and monotonic duration; provider session IDs may repeat.
Non-worker records use non-numeric
`call_` names, preserve the established display-date format and commit through
the existing scoped telemetry helper. Interactive stdio remains attached;
those records contain launch metadata with unavailable usage, not a captured
terminal transcript. Probe telemetry is outside the following builder's
progress range. Raw counters remain separate, absent
values stay blank, and unknown scope prevents treating cumulative counters as
additive spend. The reader now consumes the complete metadata header, so the
regenerated index can display previously ignored recorded fields.

The smoke station step selects the existing per-commit tier and enforces its
unchanged wall-time budget at `DevStg-Tests`. It is this repository's own stack
configuration; the step is not added to an adopter template.

### Review and scope decisions

Intermediate reviews used the requested Opus 5 / high route. The
[first review](../reviews/2026-09-05-redesign-p0b-opus.md) requested corrections;
the [follow-up](../reviews/2026-09-06-redesign-p0b-opus-followup.md) approved with
compatibility conditions. The [dispositions](../reviews/2026-09-06-redesign-p0b-dispositions.md)
separate fixed findings from unsupported claims and record the condition tests.
The subsequent [accounting review](../reviews/2026-09-06-redesign-p0b-accounting-opus.md)
covers the final probe/interactive sweep. Its shared-boundary fixes explicitly
exclude standalone calls from worker draw rotation and encode physical line
breaks in log metadata. The dispositions also retain an unusable closure
response and distinguish it from the structured retry.
No requirement approval or snapshot changed: SR-028/LLR-028's existing
session mechanisms remain intact, and IF-015 was already Drafted.

The module-size ratchet is deliberately re-stamped for these repaired
responsibilities: `agent_common.py` 1338→1473, `agent_loop.py` 2613→2678,
`integrate.py` 1426→1421 SLOC. The shared parser moved downward; existing
function-complexity ceilings remain unchanged. No file was split merely to
evade the size sensor. <!-- fig: cmd="check_complexity.module_sloc on the three named scripts" rev=5645798c+P0b -->

### Limits and next work

This is P0b footing plus the refreshed P0a census. Full P0a obligation/scenario
mapping and populated adopter-upgrade evidence remain owed. H1's next slice
must union hats applicable to each explicit parent need; dropping conflicting
context fields would silently omit perspectives. First SN→SR decomposition
also needs its exact need-scope bridge settled before assuming SR references
already exist. The existing predecessor-DAG work is a separate obligation.

Provider parity remains incomplete: plain-text calls can leave counters and
reported model unavailable; ambiguous multi-model reports remain ambiguous.
The original availability probe predates the wrapper and is retained without
an invented local invocation ID or clock. Existing `context-*` fields retain
their legacy inferred meaning; they are not used as current occupancy or
billing totals in this slice. The complete-header fix restores those recorded
values to the generated index without endorsing their interpretation.

A telemetry hook veto leaves visible residue under the existing reconciliation
protocol. Abrupt coordinator death can still leave usage unknown; no spool was
added. The control workload, paid-run budget and observation period remain
unestablished, so no replacement decision or unattended run is implied.

### Validation of this slice

The broad repair passed the unfiltered suite: `3556 passed, 20 skipped in
713.82s`. This run preceded the final probe/interactive accounting completion;
it is not represented as a full-suite run of the later incremental patch.
That completion passed the routing, stdio, accounting, dual-plan and ratchet
modules (`93 passed in 9.72s`), and selected worker/interactive regressions
(`4 passed, 67 deselected in 4.16s`). The final shared-reader/writer review
fixes passed their accounting, mixed-log and complexity checks (`29 passed in
1.80s`). <!-- fig: derived="out/run-logs/redesign-full-final.txt, redesign-accounting-final.txt, redesign-accounting-worker.txt and redesign-accounting-review-fixes.txt; exact commands recorded in the session tool output and log fragment, base 5645798c plus scoped P0b changes" -->

Final smoke tests passed: `1654 passed, 4 skipped in 60.81s`. The enforcing
command reported `61.0s vs 60s budget -> OVER` and exited 1. An earlier smoke
run also exceeded the budget; no timing pass is claimed. The owner authorized
committing despite this computer's flaky smoke timing, so this measured breach
is retained without changing the budget or tier membership.
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=5645798c+P0b-final; out/run-logs/redesign-smoke-commit.txt -->

Strict trajectory and trace integrity checks, documentation links, Ruff and
the unchanged function-complexity ceilings pass. Documentation retains the
existing report orphan warning and advisory staleness hints. No new dependency
or approval carrier was introduced. The commit is local; no push is implied.

Implementation commit: `22b21b06`. The follow-on
[resync entry](../../project-trajectory/RESYNC_PACK.md) anchors its upgrade
instructions to that exact source commit. Project-specific vision/hat/need
revalidation remains in the planned adopter workflow; this runtime slice does
not complete that broader acceptance work.
