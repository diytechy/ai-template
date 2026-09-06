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

## Pending owner inputs

Choose the observation boundary and absolute time/spend limits, or defer live
control. The implementation can continue shared-reader, hat-context, adopter
and renderer separation work while these inputs are pending. No new runtime,
one-WI assignment policy, test-tier removal or Worktrunk dependency follows
from those independent changes.
