# Control-window decision

Prepared 2026-09-06 against repaired baseline `83f2c7aa`. This is a proposed
operating envelope for P0c, not observations, a replacement ruling or a change
to the tracked pause. The [measurement contract](EXECUTION-DETAILS.md#6-measurement-and-stopgo)
requires the workload and absolute time/cost caps to be settled before paid
operation. General authorization to implement the plan does not supply those
missing numbers.

## Workload and configuration

Use actual dependency-ready work from the [18-item census](BACKLOG-MIGRATION.md),
under the existing scheduler and approval/review settings. Read each complete
spec before admission. Include ordinary code work, an amendment adjudication,
and the separately identified clean-close sample if each becomes eligible.
Do not manufacture twenty trivial WIs to reach a sample count. Held work stays
held and successor work is counted by purpose. Revalidate the queue at launch;
this document does not claim or reprioritize it.

Keep code fixed within a measured segment. A required repair closes that segment
and is disclosed before any later observations; it does not disappear into an
"unchanged" baseline. Keep sampling, consolidation, authority and provider
consent unchanged. Do not apply the retained adjudicator patch solely to make
the sample look better. Its own queued acceptance remains owed.

## Bounded options

| Option | Observation boundary | Maximum paid operation | Interpretation |
|---|---|---|---|
| Short control | First 8 completed WIs, or 2 active days, whichever arrives first | 12 active coordinator hours and US$100 aggregate provider spend, whichever arrives first | Can expose a repeated concrete fault; small or unrepresentative samples cannot establish throughput superiority or justify broad replacement |
| Planning baseline | First 20 completed WIs, or 2 active weeks, whichever arrives first | Owner-specified hours and aggregate spend required | More credible work mix; still report uncertainty and all incomplete attempts |
| No live control now | No additional unattended operation | Zero pilot spend | Complete independently justified repairs and report the replacement decision as deferred, not as an experiment that passed |

The short control is a suggested bounded first observation, not a statistically
sufficient default. A paid cap is usable only if the chosen routes expose
reliable spend or a defensible reservation bound before launch; unknown usage
must stop admission or require an explicit accounting arrangement, never count
as zero. Each stop condition drains already-authorized in-flight work according
to the current policy; the launch envelope must reserve its possible cost.
The proposed cap includes those reservations. No new quota engine is proposed.

## Decision rule

Record invocation coverage and raw reported cost, attempts and review rounds
per completion, interventions by reason per completion/active day, accepted
obligations, partial/abandoned outcomes, serial integration time and queue wait.
Required human approvals and clean-close sampling are separate from defect
repair. Do not sum ambiguous cumulative token counters. The historical
[four-WI train census](P0-SCENARIOS.md) is context, not a matched control.

Any wrong-tree or unauthorized acceptance, duplicate terminal outcome, or lost
preserved work is a correctness failure. Stop the affected path and repair it;
one failure is not by itself evidence that a rewrite is the smallest remedy.
For operating burden, investigate repeated manual state repair or repeated
avoidable review/integration turns with their actual causes and count.

Select replacement only when a recurring unmet obligation survives the targeted
repair, the proposed replacement removes its cause, and the P1/P1A/P5 gates can
be satisfied. Otherwise retain the runner or select a scoped repair. A weak
sample yields **insufficient evidence**, with targeted repair as the operating
posture. There is no automatic second window. The candidate P5 comparison
thresholds (zero correctness failures; at most 20% matched latency/throughput
regression; reduced protocol surface) remain a separate experiment contract,
including its own absolute budget before execution.

## Original owner-input request (resolved below)

The owner selected the Short control in the ruling below. The implementation
can continue shared-reader, hat-context, adopter and renderer separation work
while the launch preflight is completed. No new runtime,
one-WI assignment policy, test-tier removal or Worktrunk dependency follows
from those independent changes.

## Owner ruling (2026-09-06)

Recorded by the supervising session on the owner's instruction to lock the
recommendation and keep execution moving. The owner stated no strong contrary
opinion; every value below is an owner dial and may be re-ruled in this section.

| Input | Ruling |
|---|---|
| Option | **Short control** |
| Observation boundary | First 8 completed WIs, or 2 active days, whichever arrives first |
| Maximum paid operation | 12 active coordinator hours and US$100 aggregate provider spend, whichever arrives first; in-flight drain cost reserved inside the cap |
| Workload | The dependency-ready queue as it stands at launch, read spec by spec; no manufactured rows; held work stays held |
| Configuration | Code frozen from the launch commit; sampling, consolidation, authority and provider-consent dials unchanged; the retained adjudicator patch is not applied for the window |
| Outcome on a weak sample | **Insufficient evidence** resolves to targeted repair; no second window without a new ruling here |

**Precondition, and why the window has not started.** An independent review
of the repaired baseline (`22b21b06`) found two correctness defects in the
repairs the window was meant to measure: the durable-base rule polluted every
`base..HEAD` evidence reader after a trunk merge into a lane, and the
code-drift scan crashed kit entry points at import on a dangling editor lock
file. Under the segment rule above, those repairs close the pre-repair segment;
the window measures the configuration at the commit that lands them, and the
review record names them before any observation is reported.

**Coordinator restart at merge.** The drift detector ends the dispatcher after
any integration that touches the kit's scripts, which in this repository is
every integration. The one-lane-at-a-time integration invariant is unaffected.
Nothing about the stop needed a human; it only read as attended because the
launchers were a plain `exec` with nothing above them, so exit 11 ended the
process tree. Ruling: keep the fresh-process design (no hot reload, no second
coordinator) and let the **launchers relaunch on exit 11**, bounded, so the
drained boundary becomes a self-restart. The dispatcher keeps owning the
boundary (stop admission, drain, preserve branches, exit); the relaunch lives
one level up because old code cannot load new code into itself. A relaunch is logged
by the fresh process and is not counted as an operator intervention; a run
that exhausts the relaunch cap is.

**Spend visibility.** The historical train shows cost in 3 of 11 sessions.
The cap stands as written: a route that cannot report spend or a defensible
reservation stops admission. If that stalls the window early, the record says
so and the outcome is insufficient evidence, not a quietly widened cap.

**Launch act.** Launching is the owner's reviewed deletion of `docs/work/pause`
at or after the repair commit, with this section unchanged. The need-tier
sitting (SN-007 / SN-026 re-attestation and the SN-024 ruling, carried as an
open item minted 2026-09-06) is independent of the window and does not block it.
