# Execution record

Execution authorized by the owner on 2026-09-05, starting from `5645798c`
on `contract_split`. This is a supervised implementation sitting under
the [package boundaries](IMPLEMENTATION.md), with the existing unattended
queue paused. Package labels remain plan scope keys, not allocated WI IDs.

**Resume:** the [September 6 handoff](../handoff-2026-09-06.md) gives the next
session's read order, outstanding work and launch prerequisites. The current
continuation below supersedes pending-state statements in the historical
continuations that follow.

## Current OI-85 continuation (2026-09-06)

The owner accepted OI-85(a) and authorized continued implementation. The
[need-tier ruling](../log.d/2026-09-06-oi85-owner-ruling.md) records SN-007,
SN-026 and SN-024 exactly, using the existing named-registry approval snapshot.
The separate need-drift detector remains deferred; no other snapshot or
artifact Status is absorbed by that act.

| Scope | Current result | Remaining boundary |
|---|---|---|
| Fable repair review | Retain linked-lane base correction, bounded launcher restart, interruption accounting and non-Node resync checks; correct unavailable launch identity and overly broad TOML row inference | Final unfiltered run: 3661 passed, 22 skipped; review dispositions and actual limits in the continuation log |
| P9R | Physical renderer package, shared in-memory stage/count snapshot, direct core fixtures and renderer-absent collection; conservative local selection with Full fallback | Full/freshness checks pass, including 176 HTML and 130 core/shared cases; resync entry is anchored to `cde260dd`; CI/phase-close Full remain unchanged |
| H2/H3/H5 | Deliver Critique provenance, counterpart semantic review and proportionality stopping rules through existing method/prompts | Critique closure approved; TC-209/TC-210 Inspections pass; TC-211 normal sample remains incomplete for the existing unimplemented SR-161 machine record; Drafted-row approval stays separate |
| P0c | Owner selected Short control with absolute limits in the [control ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06) | [Launch preflight](CONTROL-PREFLIGHT.md), cost reservation and reviewed pause deletion; no observations are invented |
| P10 adopter guidance | Canonical vision/hat/need/SR revalidation method and populated adopter examples remain delivered | Source/package migration recipe is anchored to `cde260dd`; replacement cutover remains conditional |

P1/P1A/P3–P8 replacement and integration experiments, capability retirement,
and the replacement portion of P9/P10 remain conditional on the control and
contract decisions. Finishing the independent repairs does not establish a
reason to replace the runner. Existing queued artifact adjudications retain
their own authority; the OI-85 act does not approve the rest of the spine.


The [continuation log](../log.d/2026-09-06-oi85-plan-completion.md) records the
final unfiltered result (`3661 passed, 22 skipped in 744.34s`), failed-first
checks and their fixes, review dispositions and per-commit results.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto --junitxml=out/run-logs/oi85-full-final.xml" rev=1e78ada3+OI85-final; out/run-logs/oi85-full-final.txt -->

Implementation committed locally as `cde260dd0aea68b92469c5b45fdde14c3dd78d59` with hooks enabled. The
source-anchored [resync entry](../../project-trajectory/RESYNC_PACK.md) describes
the package move and coherent runtime/prose refresh. Its follow-on commit is
documentation only. Final smoke tests pass; the enforcing run measured 61.6s
against the unchanged 60s budget and used the owner's standing timing exception.
No push or control launch occurred.
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=cde260dd; out/run-logs/oi85-smoke-budget.txt -->

## Previous continuation (83f2c7aa to 77612fb2)

The owner requested continued execution with Sol, Terra and Luna. Work resumed
from `83f2c7aa`; the first slice below remains a historical record of its own
checks. The following independently justified changes are being verified as
one coherent continuation. None selects replacement by default.

| Scope | Deliverable and evidence | Current boundary |
|---|---|---|
| P0a obligations/scenarios | [Complete declared-link census](P0-OBLIGATION-MAP.md) and [scenario/train census](P0-SCENARIOS.md) | All baseline SN/SR rows and linked LLR/TC/test families accounted for; newly authored amendments are mapped separately below; clause adequacy still needs judgment before any retirement |
| P0a populated adopter | [Old-kit Node upgrade oracle](P0-ADOPTER-EVIDENCE.md) | Fresh and populated current-harness evidence; supported-platform and version limits are explicit |
| P0c | [Concrete control-window options](CONTROL-DECISION.md) supplied to owner | Workload/time/spend inputs pending; tracked loop pause retained |
| P1b prose purpose | Root README O1–O6; [purpose-to-need worksheet](VISION-OBJECTIVES.md#3-proposed-mapping-of-every-current-need) links the anchors | No objective field, parser, registry tier or approval state |
| P2a/H1 | [Explicit parent-need context in the real hat brief](H1-EXECUTION.md) | Existing carrier readers and prompt slot; two reviewed SN-026 subject tags authored, no approval act |
| P2a dependency mutation | [Parsed multiline dependency rewrite](P2A-EXECUTION.md) | Existing intake writer; source surgery validated by the TOML parser before mint effects, no queue close |
| P9R first extraction | [Text status independent of renderer imports](P9R-EXECUTION.md) | Existing public CLI/facade preserved; no CI or test-tier removal |
| P10 guidance | One adopter revalidation method in the canonical spine-authoring skill, linked by ADOPTING/RESYNC | Project-specific hats, needs and approval history retained; no generic migration engine |
| LLR replacement workflow | PROCESS §5 change-intake route plus worker/reviewer pointers to the canonical spine-authoring method | Unsuitable designs can be amended within scope; parent constraints, enduring regressions and applicable child approval remain required |
| H2–H5 promise gaps | [Scoped amendments and Inspection procedures](DECOMPOSITION-AMENDMENTS.md) | Reviewed proposals enter the live Drafted chain; authoring, approval and actual verification remain distinct |

P1/P1A/P3–P8 replacement, one-WI assignment enablement, P5's integration
experiment, capability removal and runtime cutover remain conditional. The
control window cannot be replaced by historical incomplete telemetry or fake
provider timings. The plan's independent repairs can finish without claiming
those conditional packages were implemented.

### Responsibility and deletion ledger

| Existing responsibility | Smallest change | Added operational burden / retirement condition |
|---|---|---|
| Resumed worker base inference | Existing verified claim becomes the shared base source (P0b) | No new durable claim carrier; legacy unclaimed fallback remains only for explicitly supported manual use |
| Loaded stale runner code | Stop admission at a safe boundary and restart the process (P0b) | Exit 11 and one documented restart procedure; no hot reload or second coordinator |
| Invocation accounting scattered across roles | Shared invocation metadata and existing log writer (P0b) | Additive fields in existing carrier; no metrics database or cost inference |
| WI-only perspective selection | Shared explicit SR/SN scope resolution (H1) | Existing parsers, no new carrier; replaces the caller's incomplete context composition |
| Single-line dependency rewrite after parsed selection | TOML-verified source-span replacement before mint effects (P2a) | Removes `_SPEC_NEEDS_RE`; existing parser and writer remain, no new lexer or destructive recovery branch |
| Mandatory prompt catalog missing from scaffolds | Ship its existing generator and generate the catalog | Existing catalog contract; no new catalog writer or source of truth |
| Text status loading the HTML implementation | Route the public status command before renderer imports | No new command, snapshot file or schema; full facade remains required for supported imports |
| Upgrade relevance explained in several places | Canonical spine-authoring method plus adoption/resync pointers | Existing scoped review record; no mandatory new worksheet carrier |
| Every violated LLR treated as missing coverage | Ordinary change intake distinguishes unsuitable design from changed parent obligation | Existing scoped amendment and approval route; no new replacement registry or shim requirement |
| Whole runtime / snapshot adapter / legacy converters | No deletion authorized by these changes | Each requires its clause/evidence map, supported-version decision and applicable replacement gate |

The obligation-map review corrected two proposed classifications: safe resync
(SR-036) and provenance stamping (SR-111) are continuing core promises, not
temporary conversion code. The map's reproduction now executes with all 27 SN
and 76 SR identities present. No classification changes a live Status.

### Continuation validation and remaining decisions

Implementation committed as `77612fb217b1b0d18b420d7460b394e7398d7d0f` with hooks
enabled. The follow-on resync entry and committed-adopter measurements use this
exact source. No push, artifact approval or unattended unpause occurred.

The product Python changes passed the unfiltered suite: `3586 passed, 20
skipped in 734.63s`. Its first attempt found the composer-size and stale-stage
failures described in the session log; neither was waived. The final authoring
review then changed wording and manual Inspection records, with focused
verification (`155 passed, 1 skipped, 56 deselected in 2.96s`) and a regenerated
stage check (`1 passed in 0.02s`). The full run predates those final wording
corrections; no second full run is claimed for them.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=83f2c7aa+continuation-final-Python; out/run-logs/redesign-continuation-full-final.txt; focused commands in docs/log.d/2026-09-06-redesign-continuation.md -->

Smoke tests initially took `84.35s` (`1670 passed, 4 skipped`). The enforcing
command reran the tier: `1670 passed, 4 skipped in 56.14s`, measured wall
`56.4s vs 60s budget -> within`, exit 0. Both observations are retained; no
budget or membership was changed to obtain a pass.
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=83f2c7aa+continuation; out/run-logs/redesign-continuation-smoke-budget.txt; initial run in redesign-continuation-smoke.txt -->

Traceability reports `orphans=0`, `integrity=0` and `schema-findings=0` for the
authored chain. SR-184's advisory about Critique wording with Inspection is
retained deliberately: it inspects a Critique acceptance record's provenance,
not the artifact's subjective quality. The new TCs' result sections explicitly
say they have not run. Strict trajectory, Ruff and documentation checks pass;
the pre-existing report orphan warning remains.

Watched/capped bytes: PROCESS `88365→88990` (+625 for ordinary design-change
intake); canonical byte-budget skill `4781→4632` (−149 from restamping/tightening
its explanation). Materialized skill copies match. AGENTS.template remains
9980, CLAUDE 7975 and PROCESS_OPTIONS 187932; none of their caps changed.
<!-- fig: cmd="wc -c project-trajectory/PROCESS.md project-trajectory/skills/byte-budget-guard/SKILL.md project-trajectory/AGENTS.template.md CLAUDE.md project-trajectory/PROCESS_OPTIONS.md" rev=83f2c7aa+continuation-final-wording -->

The remaining plan is not represented as complete. P0c still needs the owner's
workload/window and absolute time/spend limits in [the control decision](CONTROL-DECISION.md).
The amended need cells SN-007/SN-026 require need-tier re-attestation;
SR-162 and the new Drafted SR/TC rows follow their ordinary artifact authority.
The [amendment record](DECOMPOSITION-AMENDMENTS.md) names their exact state and
unexecuted Inspection work. P9R's package/snapshot/fixture/selector work and its
cadence approval remain beyond the first import extraction. Replacement,
one-WI enablement, the P5 experiment, capability retirement and cutover remain
conditional on their evidence and authority gates. No unattended run, broad
baseline reset, queue cleanup or Worktrunk dependency is implied.

## Initial scope (2026-09-05)

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

## Boundaries at the first slice

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

## Independent review and repair segment (2026-09-06, Fable 5.1)

The owner asked for an independent review of the two implementation commits
before locking the control decision. Three reviewers (runtime, continuation
code, spine/docs) worked from `875a64b7`; findings and dispositions are in
[the review](../reviews/2026-09-06-redesign-fable-review.md) and
[its dispositions](../reviews/2026-09-06-redesign-fable-dispositions.md).
The owner then instructed the fixes and locked the recommendation; the ruling
is the [control decision's owner section](CONTROL-DECISION.md#owner-ruling-2026-09-06).

Two P0b repairs were themselves defective and are repaired here, which closes
the pre-repair segment under the measurement contract's own rule:

- **Durable base.** The claim-first rule polluted every `base..HEAD` evidence
  reader after a trunk merge into a lane (readers walk without
  `--first-parent`). A linked lane now keeps the merge-base with trunk; the
  claim commit is the boundary only in the single checkout the repair had
  targeted. The regression test merges a trailer-bearing trunk commit.
- **Code-drift scan.** A dangling editor lock file matched `*.py` and raised
  at import of every kit entry point. Non-regular entries are skipped; a
  failed launch capture disables detection with one warning instead of
  restarting on every poll.

**Restart at merge, ruled and implemented.** The drain design stands. The
launchers (live and shipped templates) relaunch the coordinator on exit 11,
bounded at 50, so a walk-away run survives its own integrations. Relaunches
are not operator interventions; exhausting the cap is.

Also landed: Ctrl-C in an attached sitting persists a complete `call_` record
with `outcome: INTERRUPTED`; R-E judges a `#fragment` on a TOML registry as a
row id (the line the dual-plan composer already held), with the reader homed
in `kitlib.spine`; the old-kit resync test runs its kit assertions without
Node; SR-184 no longer disclaims its parent's family clause; the Inspection
carriers are named by subject; and **OI-85** carries the need-tier sitting
(SN-007 / SN-026 re-attestation, the SN-024 ruling, the parked SN drift
detector). No need cell, approval, policy dial or queue state changed. The
restart drain's "preserved" treatment of non-boundary exits is retained by
design (dispositions, item 5).

### Validation

Focused modules touched by the repairs, run at the repaired tree: coordinator
drift, session accounting and stdin, hats, dogfood sync, launcher interpreter
(including the new relaunch cases), old-kit resync, dispatch, module-size and
complexity ratchets: `214 passed, 15 skipped`, then the ratchets alone
`4 passed` after the reviewed `check_trajectory.py` +5 SLOC restamp. The base
rule's two tests, R-E's fifteen SpecRef/anchor tests, intake's 35
needs/supersede/mint tests, the bootstrap launcher/byte-cap tests, and the
spine-carrier/rule/stage modules (`59 passed`) pass. Strict trajectory check on
the live repo: clean (the three standing WI-title warnings). Trace at the tip:
`orphans=0 integrity=0 schema-findings=0`, `docs/stage` current at
DevStg-Tests with 17 drafts. Full unfiltered suite: `1 failed, 3593 passed,
22 skipped in 694.32s`, the one red being this segment's own base-rule
fallback, corrected by one line and re-verified on its module set (`84
passed`); no second full run is claimed. Commit bar: `1674 passed, 4 skipped`,
`59.0s vs 60s budget -> within`. Exact tails in
[the session log](../log.d/2026-09-06-redesign-fable-review.md).
