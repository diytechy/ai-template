# Execution contracts and implementation slices

**Status:** implementation design for cross-check, 2026-09-05; source
`fa17b85f`. No runtime or approval-policy change is made here. Package order
and enablement conditions live in [IMPLEMENTATION.md](IMPLEMENTATION.md).
This document supplies the next level of detail, not another independent plan.

## 1. Ownership and small interfaces

Use typed values at the existing read boundary. The signatures below describe
responsibilities; they do not mandate a class hierarchy or a separate module
per type. All trunk mutations use the same coordinator serialization boundary.

| Operation | Inputs | Result and permitted effect |
|---|---|---|
| Read project | Git revision, enabled capability set, supported carrier version | Immutable snapshot of WI specs, dependencies, active assignments, pending decisions and current policy; no writes |
| Reconcile proposal | Proposal, snapshot, prior applicable decision | Reviewed mutation plan: affected IDs, scope digest, preconditions, spec/edge edits and lineage; semantic adjudicator may be invoked, but cannot allocate/write directly |
| Apply intake | Mutation plan, expected trunk revision | Recheck preconditions and publish all related edits in one commit; stale input returns for reread, never partially applies |
| Schedule | Validated snapshot, capacity and current authority | Selected single-WI assignments plus wait reasons and snapshot identity; no Git writes or provider calls |
| Claim | Selected WI and expected snapshot | Record assignment and base before launch; reject changed spec, duplicate claim, stale policy or unavailable lane |
| Invoke | Assignment, owed role, route, prompt and budget | One bounded provider process, normalized result and invocation metrics; no implicit approval from exit code |
| Prepare candidate | Assignment output, current trunk B, required validation selection | Candidate C/tree T with final close and checked generated content, or explicit rework/conflict result |
| Accept/promote | Candidate, check evidence, authorized review results, expected B | Validate current authority and identity, then promote once under the selected P5 protocol |
| Record aftermath | Accepted commit, outcome, successor proposals, pending metrics | Idempotent intake/report transactions; no reinterpretation of a failed attempt as accepted work |

The snapshot is in-memory. Assignment and review evidence are durable because
recovery needs them. A dashboard, telemetry index or provider conversation is
never a second source for whether a WI is complete or approved.

Missing/malformed/valid parsing remains distinct. A caller may stop on malformed
authority while another records unavailable optional data; consolidation shares
syntax, not every consumer's failure policy.

### Assignment identity and lifecycle

One assignment names `wi_id`, unique `attempt_id`, immutable spec digest,
recorded claim/base commit, worktree/branch, chosen route, claim-policy revision
and owed phase. A rework invocation belongs to the same attempt while its scope
remains unchanged. Recovery that retries an owed phase also retains the attempt;
a deliberate terminal failure followed by a newly claimed run gets a new one.

| Boundary | Durable fact before proceeding | Restart behavior |
|---|---|---|
| Claim → first build | Tracked claim, base and spec identity | Reconcile local process ownership; launch only if no existing worker owns it |
| Build → review | Candidate/work commit plus owed role | Reuse committed work; do not rerun build merely because the coordinator restarted |
| Review → rework | Retained findings, reviewed identity and next phase | New builder invocation receives exactly the unresolved applicable findings |
| Review → acceptance | Authorized evidence for the selected candidate and policy | Missing result means review is owed; process exit 0 cannot stand in for approval |
| Acceptance → promotion | Accepted candidate/receipt retained and expected trunk B | Check whether already promoted before retrying; changed B requires re-preparation |
| Promotion → intake | Accepted commit and source event identity | Replay aftermath once; deduplicate successor proposals by source event |
| Cleanup | Evidence retention satisfied and no sole-copy work | Retry cleanup separately; never repeat acceptance or delete dirty/unknown content |

Keep WI directory status distinct from attempt phase. A partial/cancelled
terminal WI does not satisfy a predecessor that requires delivered behavior.
The existing selected approval and trace semantics govern until their enabling
amendments land; this table does not reinterpret old lanes during migration.

## 2. Every provider invocation has attributable usage

**Decision proposed for this redesign:** capture metrics per invocation across
build, review, plan, intake adjudication, critique, arbitration, retries and
any enabled retention maintenance. This is part of the launch/result boundary,
not something each role remembers to do after its work finishes.

Current `agent_loop.session_meta` and `agent_common.write_session_log` already
write session-grained metrics under `docs/iteration/`; available fields include
input/output tokens, cache counters, cost, wall time, WI and phase. Route/tier
attribution and provider parity are incomplete. `plan_runner` also invokes
`agent_session` and must use the same accounting boundary. These statements
come from source inspection, not a claim that historical logs are complete.

### Record contract

Extend the existing per-session carrier; do not add a metrics database or a
second transcript store. P0's small instrumentation slice can extend the current
header/writer before a new runner exists. P2 reads old headers with explicit
missing fields. Keep one versioned parser/writer for the extended format.

| Group | Fields and meaning |
|---|---|
| Identity | `invocation_id` allocated locally before launch; `provider_session_id` when reported; `resumed_from` where applicable. One retained conversation can have many invocation IDs. |
| Attribution | `wi_id`, `attempt_id`, role, review/plan round where relevant, subject revision/digest; non-WI calls name their source event instead of inventing a WI. Legacy batches retain an explicit WI set and remain non-attributable to a single WI. |
| Route | Provider family, roster row, requested and reported model, routed tier, effective effort/settings, policy revision. A reported-model mismatch remains visible. |
| Timing/result | Start/end UTC, monotonic elapsed time, API time if reported, exit code, timeout/crash/launch-failure/completed status, domain disposition separately. A completed call can request changes. |
| Usage | Input, output, cache-read, cache-create and reasoning tokens where supplied; reported cost and currency; source and whether counters are invocation deltas or cumulative conversation values. |
| Completeness | Known/partial/unavailable usage, missing fields/reason, parser version and metric scope. Unavailable numbers are omitted/null according to carrier convention, never coerced to zero. |
| Optional context | Current context occupancy, window and compaction signal only if independently reported with defined semantics. Total tokens spent over many turns are not context occupancy. |

Do not assume every provider uses disjoint token categories: cached input can
be included in input totals and reasoning can be included in output totals.
Each adapter declares inclusion semantics. Preserve the reported counters;
derive comparable totals only when those semantics support them. Keep reported
billing separate from optional estimates with a price/source/date basis.

Rules that prevent misleading aggregates:

1. A fresh process allocates a new invocation ID even if it resumes the same
   provider conversation. Retries consume real resources and are separate rows.
2. For cumulative provider counters, calculate a delta only against a known
   prior counter for the same session and scope. Unknown baseline, reset or
   decrease means unavailable delta with a reason; never subtract unrelated runs.
3. Record child-model usage when the provider exposes it, but identify whether
   the parent total includes it. Add either the inclusive parent or disjoint
   children, never both. Unknown inclusion prevents a combined cost claim.
4. Re-reading a result updates/reconciles the same invocation record; it cannot
   append a second billable copy. Only a new external invocation adds usage.
5. Every failed/timed-out call gets a result row with the clock measurement and
   whatever counters arrived. A missing final provider event means unknown
   remaining usage, not “free” or successful work.
6. Report cost by role and attempt before aggregating to a WI. Report abandoned
   work separately, and also include it in total project operating expenditure.
   A per-accepted-WI efficiency figure includes associated rework/review costs;
   a project-wide figure also names unassigned overhead in its numerator.

### Persistence and fault behavior

Before spawning, write a provisional invocation record into the existing local
run-output area with unique identity, intended route and timestamps. Finalize
it atomically on completion. The coordinator transfers the bounded metadata
to tracked `docs/iteration/` records at the next safe serialized transaction,
using the same invocation ID. Indexes are derived, and raw transcripts remain
bounded/redacted under existing policy.

Do not commit telemetry onto a frozen candidate's reviewed tree. During a P5
integration turn it waits in the local spool and is published after the turn,
linked to its candidate/receipt. Required acceptance evidence has its separate
P5 durable receipt and cannot depend on this optional metrics flush.

A same-machine restart reconciles provisional rows with retained results and
marks unresolved ones interrupted. A fresh clone recovers tracked metrics;
unflushed local-only records can be lost with the machine. Report that export's
coverage and uncertainty, never fabricate recovered usage. Capturing external
spend atomically across a provider call and a local disk loss is not promised.
Metrics-write failures are visible operational findings under existing failure
policy; they are not new approval gates or permission to approve without review.

### Acceptance scenarios

| Scenario | Expected evidence |
|---|---|
| One build, one review, one rework, second review | Four distinct invocation records linked to one WI/attempt; each role's actual usage counted once |
| Two parallel WIs | Distinct IDs and correct attribution after merge; no filename collisions or copied lane totals |
| Retained adjudicator called twice | One provider-session ID, two invocation IDs, separately attributable usage deltas |
| Provider timeout before final usage | Known elapsed time and partial/unavailable counters, no invented zero |
| Crash after result before tracked flush | Same-machine recovery exports one row; repeated recovery exports no duplicate |
| Provider includes auxiliary model usage | Scope labels prevent double counting; raw counters retained |
| Provider has no usable usage interface | Run still executes under existing policy; metric coverage reports the gap |
| Plan/arbitration and retention keep-warm | Same writer and attribution rules as builds; overhead is visible rather than omitted |

Use sanitized recorded provider fixtures plus fake adapters first. Pin the
provider-output version tested; verify actual installed CLI formats before
implementing their adapters rather than assuming today's config emits JSON.
Live provider probes are a separately budgeted implementation validation.

## 3. Review feedback starts a fresh builder invocation

**Default:** a material review finding starts a fresh builder process and
conversation on the same WI, attempt and worktree. It is not a new WI and does
not resume the original builder's conversation. The configured routing policy
may keep the model/family, swap it or increase tier; record the effective route.
Do not hardcode a new escalation ladder merely to implement fresh sessions.

This preserves the current `apply_rework_scope`/session-launch behavior. A
coordinator restart is distinct from a provider conversation resume. Builder
continuation, if later desired for measured efficiency, is a separate policy
experiment with fresh independent reviewers retained.

### Rework brief and return contract

The coordinator composes one brief from the recorded assignment and evidence:

- WI scope/acceptance and relevant normative parent constraints, with the
  permission to propose a justified replacement of an unsuitable LLR.
- Base and current work commit, candidate reviewed, and any later recompose
  differences. Old findings do not automatically certify a new tree.
- Stable finding IDs, severity, unmet criteria and evidence; prior dispositions
  and the remaining unresolved set. Include applicable reviewer rationale.
- Current policy, changed routing/authority, remaining budget and the next
  required output. Do not copy every historical transcript into the prompt.

Builder output names the changed commit and, for each applicable finding,
the fix/evidence or a disputed disposition. The coordinator validates identity
and reads repository evidence; it does not trust a prose claim of completion.
A disputed criterion routes to the existing bounded arbitration/owner path.
Changing promised acceptance or active scope returns to intake before dependent
work continues; the builder cannot silently lower the bar to close a finding.

| Review outcome | Next action |
|---|---|
| Approved, with optional minor suggestions | Proceed to applicable acceptance/integration; suggestions do not force another builder |
| Material changes requested | Fresh rework invocation on the existing assignment, with finding-linked brief |
| Reviewer/provider unavailable or malformed result | Retry/reroute the owed review under policy; preserve built work, no gratuitous rebuild |
| Finding disputed | One bounded arbitration attempt against the same subject/criteria, then the policy-defined human decision if unresolved |
| Human authority required | Preserve evidence, stop/drain or continue independent work according to current policy |
| Trunk/spec/policy invalidates candidate | Re-prepare and obtain applicable fresh checks/review; do not reuse an old approval as a new one |

The builder must actually change the deficient implementation or demonstrate
why a finding is wrong. A record-only rewrite is not evidence that a material
defect was fixed. The final reviewer checks the candidate and criteria, not
only the builder's finding-disposition list.

**Adjudicator retention remains separate.** WI-551/WI-541 describe an existing
owner-approved optional continuity capability. The redesign must disposition
that obligation explicitly; fresh ordinary builders do not cancel it, and
adjudicator continuity does not authorize reusing an artifact author's session
as an independent final reviewer. See [the backlog mapping](BACKLOG-MIGRATION.md).

## 4. Verification selection and honest stage reporting

**Correction to the second Fable review:** absence of product tests from a
DevStg-Tests bar does not by itself prove a false claim. `_run_bar` reports
the selected bar and step count. PROCESS distinguishes test definition and
failing-first work from implementation acceptance. Preserve that distinction.

The proposed refinement is a declared validation selection for the *change*
in addition to the derived stage's process checks. Reuse the existing WI bar,
stack configuration and check planner. Avoid another heuristic policy engine.

| Change/claim | Validation owed |
|---|---|
| Needs/design/test-definition work | Applicable process/trace checks and honest evidence of the stage deliverable; newly specified expected-red tests are not reported as passing implementation |
| Changes existing runnable code while global spine is at an earlier stage | Relevant existing behavior/regression checks plus new change acceptance before claiming delivery; a low global stage cannot silently remove implementation verification |
| Claims implementation complete | Applicable implementation/gate suite, coverage and acceptance evidence; expected-red new behavior is no longer a successful terminal delivery |
| Pure records/docs | Existing declared floor and relevant doc/record validation; no claim that product tests ran when they did not |
| Rendering or shared-input changes | The existing [affected-capability table](LLR-AND-RENDERING.md#run-expensive-rendering-tests-when-the-rendering-capability-can-be-affected), with broad fallback |
| Unknown impact, missing base or changing the selector | Broad applicable validation and a recorded reason; no default narrowing |

Test-first evidence names the new test and the expected missing behavior.
Existing regressions or unrelated failures cannot be relabeled expected-red.
No existing required check, including SN-007's full-suite promise, is waived by
this table. Resolve any doctrine/cadence inconsistency through a narrow reviewed
amendment before enabling changed selection; retain current bars meanwhile.

Each check result names candidate tree, selection/version, command, status,
duration and evidence location. Status distinguishes pass, fail, unavailable,
not applicable, and not run; expected-red is scoped test-definition evidence,
not a pass override for a required implementation check. Aggregate statements
say “selected checks passed” or “full suite passed” only when supported.

## 5. Integration experiment and boundary failures

P5 compares close-before-review with the existing refresh adapter against
final compose/check/review under one reserved turn. The exact-tree receipt
format and commit publication are prototype outputs, not settled tooling.

| Injected event | Required result, for either acceptable implementation |
|---|---|
| Trunk moves before or during costly validation | Detect at phase boundary; final expected-base check prevents stale promotion |
| Human tightens approval policy while builder runs | Old claim supplies provenance only; current authority holds promotion |
| Candidate proposes relaxing its own policy | Existing trunk policy governs whether that change may be accepted |
| Conflict on source or normative data | Return a concrete rework/conflict result; no automatic semantic resolution |
| Conflict only in generated output | Regenerate from the composed authoritative sources using the declared order; checks see the resulting candidate |
| Review approved but result not durably recorded | No acceptance inferred from a CLI exit; repeat owed review if evidence cannot be recovered |
| Receipt recorded but promotion not completed | Retained candidate reconstructs the owed action; recheck base and authority |
| Promotion completed but intake/metrics not flushed | Accepted work stays accepted; replay only missing aftermath by source event |
| Cleanup interrupted or dirty worktree found | Preserve branch/files and report remaining cleanup; never erase sole-copy evidence |

No tool, including Worktrunk, replaces the domain checks in this table merely
by offering a merge command. Worktrunk is optional operator tooling; no station
prototype is on the critical path. This is a scope/economics decision, not a
claim that its history-preserving flags cannot work.

## 6. Measurement and stop/go

Measure a known repaired configuration before deciding on replacement.
Separately identify changes made to establish that configuration: durable base,
code-drift handling and telemetry attribution. Compare against older history
only with these differences disclosed. Check-selection semantics require the
decision in §4, not an assumed fourth unconditional fix.

Proposed planning baseline: two active weeks and at least 20 completed WIs,
with ordinary builds, scope/approval work and adjudications represented. If the
available backlog cannot supply a meaningful mix, keep the operational sample
small and report uncertainty; scripted cases provide correctness evidence but
cannot be counted as observed real-agent efficiency. Agree the actual workload
and budget before starting paid operation. Elapsed time alone is insufficient.

| Decision input | Required presentation |
|---|---|
| Review burden | Median/p90 rounds per completed WI, separated by kind, with raw sample count |
| Operator effort | Interventions per completion and active day, reason classified; distinguish ordinary required approvals from manual state repair |
| Useful progress | Accepted obligations/WIs, partial and abandoned work, unresolved findings, successor proposals by purpose |
| Spend | Reported cost/token categories by invocation/role and completion; metric coverage and unknown usage alongside totals |
| Integration cost | Sum of all compose/check/review/intake turns per completion; queue wait and active serial time separately |
| Correctness | Escaped defects, lost/stale evidence, unauthorized approvals, duplicate assignment/outcome and recovery failures |
| Simplicity | Removed versus added readers, writers, states, durable carriers and recovery procedures, including adapter/migration cost |

Candidate experiment budgets for owner review: zero observed wrong-tree or
unauthorized acceptance, duplicate terminal outcomes or lost preserved work;
no manual state repair in the scripted crash suite; no more than 20% regression
in median/p90 completion latency and accepted completions per active hour on
matched work at one and two lanes; and a documented reduction in protocol
surface. These are proposed thresholds, not measurements or accepted promises.
Small samples may leave p90/throughput comparisons inconclusive. P0's ruling
must set final thresholds and an absolute time/cost cap before P5 is run.

Outcomes are **retain**, **targeted repair**, **replace**, or **insufficient
evidence**. Failed/inconclusive experiments do not justify continuing the
rewrite by momentum. Keep reviewer settings unchanged during the control
window. Any self-minting freeze during replacement is a separately authorized
treatment with duration and restoration conditions; selecting replacement
alone does not silently turn existing review dials off.

## 7. One layer below the implementation packages

These labels are planning slices, not new WI IDs. Mint only the next authorized
coherent slice after reconciling its overlap with existing work. Each ends in a
reviewable change plus its applicable checks; no package-wide “done” by prose.

| Slice | Concrete deliverable | Entry/exit and deletion boundary |
|---|---|---|
| P0a inventory | Revisioned need/contract/test and queued-work maps; representative adopter fixture | Read-only first; map every queued item and approved promise before retirement |
| P0b footing | Durable base, defined script-drift stop and session attribution in current runner | Reproduce OI-83/OI-84, apply existing authority, replace inferred base and missing route metadata; run current bars |
| P0c decision | Control results and retain/repair/replace ruling with budgets | Requires known configuration and credible observations; no automatic unpause |
| P1a contracts | Domain records, transition/failure table and ownership | Walk all §1/§5 cases with fake providers before implementation |
| P1b purpose | Reviewed objective wording and SN mapping | Independent of replacement; no new stage or inherited downstream objectives |
| P1A enablement | Narrow approved amendments and old/new behavior/test map | Must precede live changed behavior; P5 supplies final evidence-specific amendments |
| P2a readers | Shared parser/prompt and compatibility boundaries | Preserve absent/malformed policy, raw text/CRLF/source spans; remove duplicate consumers only after equivalence cases pass |
| P3a intake | Proposal decision preview and atomic application | Duplicate/stale/overlapping/active-scope cases; replace idle-tick semantic census only at cutover |
| P4a scheduling | One decision object consumed by CLI and dispatch | Saved-snapshot replay explains intentional ordering changes; remove dispatcher override |
| P5a comparison | Real-Git prototype and recorded protocol/performance decision | Include rework, holds, metadata checks and fresh-clone recovery; no receipts platform if experiment fails |
| P6a runner | One-WI claim, invocation and owed-phase recovery | Same one/two-lane path; no fresh claim on coordinator restart; drain old batch lanes before switching |
| P7a sessions | Shared result envelope, finding-linked rework briefs and usage writer across roles | Fresh builder behavior and §2 accounting scenarios pass; remove role-specific duplicate accounting/parsing |
| P7b owner view | Text resume/decision surface with operational Notes | Resume paused and failed runs without manual handoff; retire handoff only after that demonstration |
| P8 pilot | End-to-end fake-provider suite and approved real-WI sample | P1A and P5 contract settled; report unknown metrics and all interventions |
| P9R extraction | Renderer package, snapshot boundary and shared test selection | May proceed independently after inventory/own amendments; prove core works with renderer absent |
| P9a consolidation | Clause/evidence-backed removal and capability mapping | No count quotas; optional promises verified when enabled; independently argued cuts stay separate |
| P9b objectives | Optional reference carrier and adopter migration, if selected | Follow VISION-OBJECTIVES.md; maintain legacy adopter validity and ordinary approval semantics |
| P10 cutover | Forward/reverse migration limits, single-writer switch and old-path deletion | Rehearse rollback after new accepted work without resetting away that work; publish supported-version boundary |

Do not require parser cleanup or rendering extraction to wait for the runner
decision where their own evidence is sufficient. Conversely, a successful
parser refactor does not authorize assignment, approval or scheduling-policy
changes. Requirements and executable acceptance tests stay together at each
behavior-changing slice.
