# Implementation and migration breakdown

**Proposal only.** This document defines reviewable implementation packages; these labels are not minted WI IDs. Source baseline: `a9bf6cee29fd0492d136457615598e8e96e5dada`. Read [the design recommendation](README.md) first.

The intended deliverable is a smaller reusable kit, not a second permanent coordinator. Keep the current runner as a rollback option until cutover, then delete the replaced runtime. Retain unrelated working tools unless the capability review explicitly replaces or retires them.

## 1. Implementation boundaries

Suggested files describe responsibilities rather than mandatory filenames:

```text
workflow/
  model.py          WI, Assignment, Candidate, Result; validation and transitions
  intake.py         proposal reconciliation and atomic queue mutation plans
  schedule.py       pure decisions, reasons, no effects
  run.py            enact decisions, subprocess lifecycle, recovery
  review.py         plan/review/arbitration protocol
  integrate.py      candidate preparation, checks, acceptance, promotion
  git_adapter.py    narrow Git/worktree commands
  agents.py         roster selection and provider invocation
  cli.py            create / next / run / review / status / doctor
```

Do not split these further preemptively. Reuse existing modules behind adapters where their behavior remains sound. In particular, the check harness, gate derivation, requirement readers, and bootstrap do not need rewrites merely because the runner changes. The CLI can initially wrap existing commands; avoid shipping two independent implementations of the same policy.

The pure layer must import neither process launch nor Git mutation code. The runner calls domain functions and adapters; views only read results. One intake writer allocates IDs and applies queued-scope changes. One integration writer changes trunk.

### Proposed domain records

| Record | Required information | Authority |
|---|---|---|
| WI | ID, intent/acceptance, references, dependencies, priority, tier, execution exclusivity, applicable review strategy | Versioned spec; directory remains WI status during migration |
| Assignment | Single WI ID, attempt, spec digest, base/claim commit, branch/worktree, route and claim-time policy revision (provenance, not continuing approval authority) | Tracked claim created by coordinator |
| Candidate | Assignment, trunk base, candidate commit and complete tree, declared checks and WI close proposal | Frozen versioned candidate |
| Review result | Subject tree/spec/policy, reviewer provenance, criterion-linked findings, severity, disposition | Controlled reviewer result, persisted by coordinator |
| Outcome | WI/attempt, complete/partial/cancelled result, evidence and missing scope, follow-up proposals | One terminal close and its receipt/report |
| Intake decision | Input fingerprint, affected queued IDs, keep/extend/edge/consolidate/return decision and lineage | One reviewed queue mutation |

Canonical fields should be parsed into typed values once. Reuse TOML frontmatter initially. Do not hand-edit a mutable run log and separately replay the same log to decide another authoritative state. Historical attempts are records; current WI directory and recorded current assignment have distinct meanings.

Specify the tracked claim's exact location in package P1. Preserve existing `docs/work/active/<branch>/` structure if it avoids needless migration; replace only its multi-ID assumption. A small assignment file inside the active claim directory is acceptable if no WI status is duplicated in it. Temporary worktree process metadata is not a substitute for the tracked claim.

## 2. Dependency order

```mermaid
flowchart LR
    P0[P0 Baseline and obligation map] --> P1[P1 State and acceptance contracts]
    P0 --> PR[P9R HTML boundary and test isolation]
    PR --> P9
    P1 --> PA[P1A Narrow requirement amendments]
    P1 --> P2[P2 Single-item compatibility reader]
    P2 --> P3[P3 Authoritative intake]
    P3 --> P4[P4 Scheduler]
    P2 --> P5[P5 Exact-tree integration experiment]
    P4 --> P6[P6 Runner and recovery]
    P5 --> PA
    P5 --> P6
    PA --> P6
    P6 --> P7[P7 Review and routing]
    P7 --> P8[P8 End-to-end candidate release]
    P8 --> P9[P9 Requirements and capability migration]
    P9 --> P10[P10 Adopter migration and deletion]
```

P9R is an independent rendering slice after P0 and its own applicable contract amendments; it does not wait for the full runner migration. P1A is the gate for enabling changed behavior under the repository’s own requirements; isolated fixtures and read-only adapters can proceed beforehand. P0 gates replacement work on measured need; the arrows show dependencies if that option is selected, not automatic authorization to build it. P5 is an early stop/go experiment. It must settle whether peeling can be removed before P6 hardens a replacement runtime around the wrong evidence model. P3/P4 can proceed independently of that experiment after P2, but do not run multiple mutating coordinators on the same repo.

## 3. Work packages

### P0 — Establish the behavior baseline and the rebuild decision

**Problem:** a rewrite can preserve obsolete mechanisms while accidentally deleting real stakeholder obligations.

**Work:**

- Record source revision, CLI/public carrier surface, active/queued work, relevant owner rulings, and currently supported adopter versions. Exclude owner-only material.
- Inventory all 27 SNs and 76 SRs, then the LLR/TC and test families they govern. Classify core, advanced capability, migration-only, or retirement candidate. Do not approve the classification automatically.
- Capture representative scenarios from ordinary work, spine changes, adjudication, consolidation, human holds, partial close, interrupted review, and adopter upgrade. Census historical train sizes, starting with WI-584/587/588/589 from the prior investigation. For each, distinguish one shared acceptance decision from separate deliverables and compare one coherent consolidated WI against separate exclusive WIs, counting all resulting integration/review turns. Exclusivity provides serialization, not joint approval atomicity: related normative amendments that must be accepted together must fit one coherent WI and acceptance transaction, or retain an explicitly supported joint-approval mechanism until that need is resolved. This is decision material to produce, not a census claimed complete by this plan.
- Measure fresh-core scaffold footprint, warm smoke/full checks, operator interventions, and session costs where logs actually support attribution. Keep historical numbers labeled historical.
- Explicitly disposition existing dev-slice/train batching policy and its approved design/tests: one-WI cardinality is a proposed policy change, not a compatible reinterpretation. Obtain that decision before enabling new assignment creation.
- Establish an early realistic downstream fixture, including user-owned content and a representative non-Python adopter, before pruning the spine. Exercise scaffold, upgrade, and the changed behavior slices on supported platforms; a blank scaffold alone is insufficient.
- Inventory interface obligations once per surface, with a clause map for each consumer’s required behavior. Imports establish dependencies, not error semantics or acceptance guarantees.
- Predeclare a control-period workload, observation window, and decision thresholds with the owner before operating a pilot. Two weeks is a candidate window, not sufficient evidence by elapsed time alone. Observe the recently fixed loop under unchanged authority/review settings; report completions, attempts, review rounds per completed WI, interventions per completion and active day, adjudication by purpose, escaped defects, and work mix. Deduplicate retries and distinguish necessary adjudication from harness overhead. Any intake or policy experiment is a separately labeled treatment, not part of an unchanged baseline. Do not unpause or operate the loop as part of this documentation task.
- Decide whether observed residual failures justify P3–P8 replacement work. Stop those packages if the existing loop meets the agreed needs; P2’s shared-reader/prompt improvements and P9R may still proceed on their own evidence; P2’s new assignment behavior remains conditional on the replacement decision and P1/P1A. If data is inadequate, report the uncertainty and extend the measurement instead of declaring the rewrite necessary.
- Make a deletion ledger: old responsibility, candidate replacement, acceptance evidence, exact retirement condition. Count added schemas, parsers, states, durable carriers/refs, mutation paths, and operating/recovery procedures as well as deleted code. Unused compatibility code must get an expiry rather than a permanent adapter.

**Done when:** the workload, denominators, thresholds, observations, and explicit retain/targeted-repair/rebuild decision are recorded; every stakeholder need has a disposition proposal; public compatibility obligations are named; the selected scenarios can be reproduced without live paid agents by scripted adapters. The owner can distinguish behavior retained from behavior proposed for removal.

**Do not:** clean the backlog, change authority dials, retire tests, or restamp ratchets in this package.

### P1 — Define the small state model and observable acceptance

**Problem:** current lifecycle meaning is distributed across folders, commits, rounds, and inferred bases.

**Work:**

- Specify the domain records above, legal transitions, authority per transition, and one-WI assignment cardinality.
- Define dependency satisfaction for complete, partial, cancelled, and restructured predecessors. Absorption rewrites live inbound edges; it never declares missing work complete.
- Define pause as stop admission and drain according to current policy. Distinguish held approval, malformed authority, provider fault, crash, and deliberate partial result.
- Define transaction staleness separately from semantic reuse. Record the snapshot revision for apply-time preconditions; fingerprint the scope/acceptance/dependency/artifact/resource inputs actually adjudicated for judgment reuse. The current four-field digest intentionally avoids nonsemantic churn; preserve that goal while adding omitted normative input. Do not invoke the LLM merely because Deliverable, telemetry, a routing-only tier, or unrelated trunk bytes changed. Classify uncertain inputs conservatively until reviewed; measure over-invalidation in P5/P8.
- Preserve the settled clauses: SN-006 records limit-enforcement faults and continues; SN-029 sends approval-authority faults toward more human involvement. Ask an owner only about a remaining concrete gray zone, such as failure to determine independence from a pending hold. Do not reopen the whole failure policy.
- Specify current-trunk policy as the authority at review/promotion, with claim-time policy retained only as execution provenance. Include a mid-flight authority tightening in the acceptance scenarios.
- Add the normal intake route for a sound parent obligation with an unsuitable LLR design; specify how one scoped WI replaces the design and evidence under existing approval authority. Use the [replacement workflow](LLR-AND-RENDERING.md#1-llrs-should-constrain-the-selected-implementation-without-freezing-the-design), not a new mandatory registry.
- Write the small behavioral scenarios and failure tables before kernel code.

**Done when:** a reviewer can walk create → claim → execute → review → integrate and each failure return without reading existing runtime modules; every state has one owning writer and recovery rule. Any unresolved independence-under-hold failure transition has a scoped ruling before P6 implements it; settled SN-006/SN-029 behavior is not blocked on a new general ruling.

**Deletion enabled:** no implementation yet, but multi-ID assignment and inferred base are explicitly absent from the target contract.

### P1A — Amend incompatible contracts before enablement

**Problem:** an owner decision in a plan does not amend the approved rows and tests that still require the old runtime. Deferring all spine edits to P9 would leave P8 operating against conflicting contracts.

**Work:**

- Prepare the smallest reviewed, version-scoped amendment set for one-WI assignment, scheduler-owned admission, intake-owned reconciliation, and whichever partial-close/evidence changes P5/P6 will enable.
- Inspect SR-148, SR-144, SR-156, SR-170/SR-173, LLR-149/159/182/210 and their actual TC/test links. This is a candidate impact list, not a claim every row needs rewriting. Preserve externally required behavior and distinguish a changed mechanism from a retired obligation.
- Approve amended artifacts through the current stage/authority mechanism, update acceptance tests in the same scope, and record old→new obligation/evidence mappings. The user’s approval of the redesign is not a substitute for those artifact changes.
- Scope old-format and old-runner compatibility tests to their supported version; specify the new contract for the new runtime without weakening the common assurance bar. Isolated failing-first prototypes may precede enablement. Do not flip a new runtime on in the live repo while its governing contract is still the old one.
- Include the change-intake diagram and worker/reviewer brief contract where they incorrectly equate every violated LLR with a coverage gap. Preserve approval authority while permitting justified design replacement.
- Finish any evidence-specific amendment after P5 selects the actual protocol. Bulk retirement and optional packaging remain P9 work.

**Done when:** every behavior changed by enabling P6/P8 has the necessary reviewed requirement/design/test amendment and honest stage state; the old runner’s remaining supported behavior is explicitly version-scoped. No red gate is waived to fit the pilot.

**Deletion enabled:** the specific incompatible old contract/test path may retire at its declared version boundary; no unrelated spine cleanup is required here.

### P2 — Read the existing kit through one compatibility boundary

**Problem:** changing both storage and orchestration at once makes failures hard to locate.

**Work:**

- Read current specs and policy using existing parsers where possible; convert once into the domain records. Use typed absent/malformed/valid parsing outcomes, preserving each consumer’s failure policy. Preserve raw text and source spans where editing, masking, BOM, or CRLF behavior requires them; shared syntax does not imply identical failure handling. Characterize existing callers before replacing their parsers.
- Consolidate prompt filling through a strict catalog that rejects missing slots and preserves the supported stdin delivery boundary. Return typed domain failures from library code and map them to CLI exit codes at the command boundary. Consolidate responsibilities where contracts match; do not introduce one universal result envelope or pursue a fixed module count.
- Add one-item assignment creation with a durable base, spec digest, and route record.
- Reject multi-WI assignment creation in the new kernel. Existing active multi-WI lanes must drain through the old runner before switching; do not fabricate new acceptance or split their history.
- Keep schema and CLI migration translations in this adapter only, with the supported version range declared.
- Expose a read-only `next --explain`/`status` interface for the new model.

**Done when:** all current queued WIs and active assignments, including legacy multi-WI shapes, have a supported or explicitly unsupported/old-runner disposition; snapshots are reproducible; no repository state changes during inspection.

**Deletion enabled:** multiple ad-hoc consumers of WI status and base inference in the new execution path. Old imports remain until cutover.

### P3 — Put reconciliation before eligibility

**Problem:** scopes are minted independently and reconciled again at dispatch or close.

**Work:**

- Implement a single proposal path for human drafts, gap findings, partial reports, review findings, and worker successor proposals.
- Produce a reviewable intake mutation plan. Semantic decisions may call the adjudicator; allocation/writes remain deterministic and trunk-owned. Record affected queued WI IDs derived from requirement/artifact row refs, dependency closure, shared/exclusive resources, and normative scope, plus the adjudicated input snapshot. Missing or ambiguous scope requires a global hold; a filename match or a nonempty ref list cannot by itself prove independence.
- Support keep, extend an unclaimed WI, add edge, consolidate several unclaimed WIs into one successor, and return for decision.
- Recheck input fingerprint and queued status immediately before applying. Stage the complete change in an isolated candidate/index; publish one commit or nothing. No partially rewritten dependency graph becomes authoritative.
- Preserve each absorbed acceptance criterion and source link. Many-to-many legacy supersession must import without dropped obligations or cycles.
- Freeze active specs. A proposal overlapping active work waits for it or requests a separately authorized stop/change; it never edits the assignment silently.
- Reconcile the legacy queue once under an exclusive reconciliation WI. Thereafter reconcile new or changed proposals, not every idle tick.
- Deduplicate repeated event proposals by source event and accepted decision, with a bounded adjudication outcome. An unchanged dismissed finding cannot mint work forever.

**Done when:** duplicate replay mints no duplicate WI; stale judgments do not apply; dependent edges remain valid; unrelated proposals stay independent; contradictions surface before affected build admission.

**Deletion enabled:** `dispatch._admit` consolidation census in the replacement path; repeated successor-specific consolidation logic. Keep lineage validation as intake behavior.

### P4 — Make scheduling the sole admission policy

**Problem:** scheduler order and dispatcher admission are separate answers.

**Work:**

- Use a pure immutable snapshot and return selected one-item assignments plus blocked/held reasons.
- Handle dependency readiness, authority, global/affected reconciliation barriers, exclusive work, pause, and capacity in one function. A scoped barrier consumes the current intake decision’s explicit affected IDs; if its scoping evidence is absent, ambiguous, or invalidated, hold conservatively rather than guessing independence.
- Test whether stdlib `graphlib` removes enough cycle/traversal code to justify use. Always impose deterministic priority/ID ordering on its ready set; library iteration order is not product policy.
- Replay legacy queue snapshots and list every intentional ordering change. No blanket “matches legacy” claim: the proposed priority simplification deliberately changes some ties.
- Render the same decision result in CLI and dashboard. An executor finding a changed snapshot must recompute, not reorder locally.

**Done when:** independent readers select identical WIs/reasons; exclusive work drains and admits exactly one; human-held work is never authorized by capacity or priority; rejected/missing/cyclic dependencies are clear.

**Deletion enabled:** `_judgement_first`, spine batch assembly, duplicated kind/action ranking in the new dispatcher, and optionally custom critical-path/downstream algorithms if their policy is retired.

### P5 — Compare and prove the integration design

**Problem:** evidence is hard to trust when close and refresh mutate the reviewed branch.

**Work:**

- Build a real-Git prototype that reserves the final integration turn, composes candidate C on trunk B, performs closure/generation, freezes tree T, checks/reviews T, and publishes a same-tree acceptance receipt.
- Persist candidate/attempt identity before invoking the reviewer. Use retained ordinary branches under `trajectory/candidates/<attempt>`; preserve worker and trunk ancestry, and append each phase receipt as a same-tree child commit. Rejected and human-held candidates remain reachable until the required evidence is archived. A lost uncommitted result is re-requested; it is never guessed as approval. Specify a full-clone/export recovery procedure that includes candidate branches, and test retention before allowing their deletion.
- Put the complete minimum acceptance evidence in Git-reachable committed material. For the proposed design, structured receipt plus necessary rationale lives in commit metadata; generated Markdown is a projection. Prototype rejected-review persistence too.
- Verify message/secret hooks, identity policy, commit signing where configured, and CI check binding. A new commit with the same tree may still need commit-specific checks; do not equate tree equality with every check passing.
- Verify human artifact attestations still name the approved normative content and acting authority. Keep artifact-content approval distinct from final-tree approval: unrelated trunk motion alone need not invalidate unchanged artifact content, but T approval never transfers to T′. Test both `keep_nondependent` policies, an owner ready to review after a long wait, and current-trunk policy tightening during a running assignment. Content authority is not conferred merely by matching a hash.
- Recheck trunk B and governing policy before/after compose, checks, review, and at promotion. A coordinator reservation does not exclude human commits; stop stale work at the first observed phase boundary and explain the invalidation to the operator.
- Publish using a normal checked Git workflow that refuses dirty trunk and unexpected B. Do not update a checked-out branch behind its index, bypass hooks through plumbing, or overwrite unrelated work.
- Crash-inject before/after candidate creation, review result recording, acceptance commit creation, trunk promotion, outcome/intake bookkeeping, and worktree cleanup.
- Before measurements, agree a numeric experiment budget relative to the old runner: completion latency/throughput at each tested lane count, maximum human-decision re-prompt count, operator interventions, and serial waiting time. Record the workload and hardware first; never choose the threshold after seeing results.
- Measure at the configured lane count with single-pass acceptance, repeated material-defect rework, arbitration, long human holds, and follow-up intake adjudication. Use the historical review-round distribution (including its long tail) to select cases; do not equate historical whole-WI wall time to exclusive-turn time. Count every compose/check/review turn and intake judgment, and measure semantic re-adjudication frequency. Add a representative live controlled run only when implementation is approved.
- Compare a smaller alternative first: move mechanical close before review while retaining the existing governing-identity and refresh-evidence protocol. This may remove close peeling; it does not by itself remove refresh peeling or prove exact composed-tree acceptance. Test changed-base behavior and reviewer provenance explicitly against the same stakeholder obligations, recording any semantic difference before selecting either protocol.
- Compare the complete replacement protocol surface against the deleted one: receipt schema/parser, retained candidate branches, recovery/export, authority checks, and turn reservation versus peeling, excluded-path rules, and governing-history reconstruction. P5 must show a reviewer-explainable reduction, not merely move the complexity to new files.

**Done when:** wrong-tree acceptance, stale-trunk promotion, missing review provenance, and duplicate terminal outcomes are impossible in the tested transition model; restart from a clean clone reconstructs all committed obligations; the predeclared performance/intervention budgets pass and the protocol comparison demonstrates simplification. An unset budget or unreviewed complexity comparison leaves P5 incomplete.

**Stop/go:** if required evidence cannot be carried simply or review serialization is unacceptable, keep the existing verdict adapter temporarily and revise this design before P6. P6 may proceed only after P5 passes or an explicit retained-adapter contract is reviewed; its evidence assumptions cannot remain unresolved. Do not build a second metadata service or general event store as an unnoticed workaround.

**Deletion enabled if successful:** refresh and mechanical-close peeling, governing-revision reconstruction, and record-path exclusions in the replacement acceptance protocol. Historical evidence readers can remain in a migration/export tool.

### P6 — Implement runner, claims, and recovery

**Problem:** lane execution currently understands trains, historical evidence, and multiple closing shapes.

**Work:**

- Implement one dispatch loop: reconcile pending inputs, obtain schedule decision, record claim, create worktree, execute assigned phase, collect result, send candidate to review/integration, record outcome.
- Use Git worktree operations behind a narrow adapter. Preserve branches and patches until outcome/recovery evidence permits cleanup.
- Route every invocation with exactly one WI ID and one attempt. Unknown worker output is an error/uncertain attempt, never `complete`.
- Resume from the recorded base and next owed phase. Ensure the single-checkout/resumed shape cannot turn the evidence range into HEAD..HEAD.
- Pin the running coordinator code revision. When its implementation changes, stop admission, reach a defined safe boundary, exit, and let the launcher restart. Do not hot-reload an imported module graph.
- Distinguish durable state from local PID/log conveniences. In a same-machine restart, reconcile running processes; from a fresh clone, no local process is assumed active.
- Implement deliberate partial close by preserving unfinished code and making a reviewed report-only terminal transaction unless a usable subset independently meets the declared acceptance. Do not merge broken work solely to terminate a lane. Reconcile this change explicitly with SR-144 (partial outcome), SR-156 (serial lane lifecycle), and LLR-182 (terminal vocabulary) through P1A before enabling it. Check SR-170/SR-173 separately where the candidate-generation design changes shared regeneration; those are distinct obligations.

**Done when:** one and two lanes use the same path; no double assignment, no lost partial artifact, no rerun of completed work, and no busy retry loop on human-held work. Pause and resume work through every state.

**Deletion enabled:** multi-WI focus selection, train evidence aggregation, assignment-wide round inference, duplicate clean/partial path writers, and stale in-process coordinator behavior.

### P7 — Unify controlled review and planning

**Problem:** plan, adjudication, critique, and implementation review use overlapping session machinery and different outcome grammars.

**Work:**

- Use one provenance/findings/disposition envelope and shared transition engine, with typed subject-specific criteria payloads. Do not create a universal optional-field schema that recreates parser sprawl. Keep prompts and applicable criteria with their subject.
- Preserve provider-neutral routing, consent, cross-family preference/fallback, and configured review count initially.
- Support one ordinary review; opt-in plan review; rubric-based subjective critique; consolidation review; bounded dispute arbitration. Keep advanced dual-plan strategy behind its capability boundary.
- Store stable finding IDs, criterion, evidence, severity, disposition, and resolution. Preserve minor suggestions without requiring another build round for stylistic churn.
- Treat proposed acceptance changes as amendments requiring appropriate authority, never reviewer edits hidden in rework. Explicitly ask whether a workaround exists only to preserve an unsuitable LLR; permit a scoped replacement with preserved parent acceptance and updated tests, rather than treating design approval as immutability.
- Give the owner a renderer-independent resume view: current activity, blocked decision, next safe action, and evidence/check freshness. Keep human-authored operational Notes for outages, quotas, or stale loaded processes that Git cannot infer. Every generated field needs a source and timestamp or an explicit unknown. Refresh live status on state transitions, pause, and failure without requiring an HTML commit on every tick. Retire a separate handoff only after the owner can resume both a paused and a failed run from this view plus Notes.
- Record actual check selection, results, and skips separately from the derived development stage. A configured bar passing must not imply the complete suite passed. Preserve legitimate failing-first test-definition stages; any new stage-wide all-green requirement needs an explicit doctrine amendment.
- Record model/tier/roster ID and session role before launch. Preserve budget use across retries and resumed sessions.
- Stop recurring arbitration at the declared cap and produce a concise owner brief: contested obligation, evidence, options, recommendation, and affected work.

**Done when:** each review type uses the same provenance/freshness rules; disagreements route consistently; exhausted budgets surface a concrete decision; a model or worker cannot silently lower approval requirements.

**Deletion enabled:** duplicated phase-specific result parsing and escalation accounting; mandatory advanced-plan steps for ordinary WIs where owner policy permits retirement.

### P8 — Demonstrate one complete replacement loop

**Problem:** clean unit tests do not demonstrate the user's intended loop.

**Work:**

- Run fresh scaffold scenarios with scripted providers over real Git: two independent WIs, overlap requiring consolidation, ordered separate changes, human-held amendment, conflicting review, partial close, and crash/restart.
- Verify final status and records from a fresh clone. Compare scheduler display with actual claims.
- Verify P1A’s governing artifact amendments and the selected P5 protocol have landed before live enablement; a plan approval alone does not clear this prerequisite.
- Run a controlled sequence of real ordinary WIs and one scope-changing WI only after the owner approves implementation/operation. Keep the current pause until deliberately changed in that implementation session.
- Report operator interventions, root causes, session counts, token attribution where available, time in build/review/integration, and emitted follow-up work. Distinguish harness failures from product failures.

**Done when:** all acceptance families below pass; the agreed pilot completes without manual state repair; required repository checks pass with results and elapsed seconds recorded. Proposed pilot minimum: three ordinary completions and one reconciliation/approval case, plus automated recovery scenarios. This is a smoke demonstration, not a reliability estimate.

**Deletion enabled:** replacement becomes the only candidate runtime for the migration release; old runner remains a rollback tool, not a second active service.

### P9R — Isolate HTML rendering and its test family

**Problem:** module splitting has not separated HTML dependencies from text status, shared fixtures, or broad test invocation.

**Scope and ordering:** follow [the rendering package and selection contract](LLR-AND-RENDERING.md#2-isolate-rendering-as-a-package-in-this-repository). This slice may run after P0's boundary/cost inventory and its own required test-cadence/assurance amendments; it need not wait for P8. Amend any conflicting full-suite promise, including SN-007 as applicable, before enabling narrower validation. Existing checks remain in force until then.

**Work:** retain unfiltered CI during the initial extraction; narrower ordinary-change selection starts locally after applicable amendments, and CI narrowing requires demonstrated selection coverage and a separate cadence decision. Establish a shared in-memory project snapshot; extract renderer/layout/assets into a package; separate text-status CLI and fixtures; classify core/shared/rendering tests by behavior; implement one small affected-capability selection table with a broad fallback; keep current-output freshness and approved full-run cadence. Use the existing configuration/profile mechanism, not a separate rendering repository or generic test-impact framework.

**Done when:** core imports and test collection work without the renderer; core-only changes omit the expensive HTML family; rendering/schema/shared-input changes select it; actual data still generates a current, honest surface; selection handles renames/deletions and missing bases; full enabled-capability tests remain green; measured cost and coverage reports distinguish selected runs from full runs.

**Deletion enabled:** renderer imports from core/status, fixture coupling, and obsolete facade re-exports after their compatibility window. Test-case retirement still requires the ordinary obligation/evidence mapping.

### P9 — Consolidate requirements, tests, docs, and capability packaging

**Problem:** a smaller kernel can still inherit the same process burden.

**Work:**

- Complete the remaining P0 disposition map after the narrow enabling amendments already landed in P1A; do not defer any contract needed by the pilot until this package. Apply it without silently dropping criteria, historic approvals, or live dependencies. Every retired SR/LLR/TC must map to affected SN acceptance clauses and replacement evidence, or the explicit owner decision retiring that obligation; no approved clause may become unsupported through indirect cleanup.
- Re-map executable tests to enduring behavioral obligations. Keep a known-defect regression even if its old helper disappears, translated to the new boundary.
- Move obsolete implementation notes and old compatibility controls to migration/history; remove live normative rows only through the approved spine change.
- Assemble three capability sets using existing scaffold machinery: manual core; managed loop; advanced planning/architecture/reporting. Express the capability sets in the existing bootstrap mapping/profile mechanism. Generate their inventory and requirement/check view from that mapping and existing spine links; do not introduce a second authored manifest, registry, or schema. The exact set boundaries must honor the SN dispositions; accessibility stays with every shipped UI. Adoption tests must prove that each moved promise is available and verified when its capability is enabled, as well as absent from core dependencies when disabled.
- Keep current gate derivation and trace schema in this release. Consider direct SR evidence or stage simplification only in a separately reviewed proposal.
- Replace master-process runtime prose with the four-step loop and the canonical policy tables. Put detailed operational reference beside the relevant adapter.
- Run byte-budget checks before and after editing watched docs and report deltas. These plan documents are not among those capped files.

**Done when:** every removed row/check has an explicit disposition; a minimum scaffold runs without importing/installing advanced capabilities; required capability tests and all mandated repo checks pass.

**Deletion enabled:** retired template surfaces, redundant doctrine copies, old helper-specific tests, and advanced-core imports. No test quota determines success.

### P10 — Ship a bounded migration and remove old paths

**Problem:** indefinite compatibility doubles the architecture.

**Work:**

- Publish a versioned RESYNC recipe and converter that reads supported old formats, preserves adopter content and history, and reports unsupported/ambiguous input without modifying it.
- Require an idle old station before conversion. Drain active multi-WI lanes with the old runner; never import them as fake one-WI accepted assignments.
- Run old and new schedulers read-only on saved snapshots, comparing intentional policy differences and unexplained differences separately.
- Select exactly one mutating runner through an explicit version/config boundary. Refuse mixed claims or simultaneous runners.
- Pilot on this repo and at least one representative adopter copy, including a non-Python profile and supported OS CI.
- Remove old runtime files, aliases, migration fallbacks outside the supported window, prompts, and tests whose behaviors were retired. Update bootstrap mapping, kit inventory, dependency ledger, resync pack, and docs together.

**Done when:** fresh adoption and supported upgrade are green; a reviewer can locate one writer for each lifecycle fact; the old runner is unreachable in the shipped current profile; the rollback recipe has been exercised on a copy.

## 4. Acceptance and test families

These are behavior families, not a request for one new registry row per bullet or one test per implementation branch.

| Family | Required checks |
|---|---|
| Intake | Duplicate proposals; stale semantic inputs; overlap with active work; contradictory approved requirement; atomic edge rewrite; no accepted obligation lost in consolidation |
| Scheduling | Deterministic selection; correct predecessor satisfaction; stable priorities; unknown/cyclic references; pending reconciliation; exclusive drain; one WI per lane; capacity and human holds |
| Assignment | Durable base; immutable assigned scope; claim before launch; repeated claim refused; clear attempt identity; provider failure and reroute provenance |
| Review | Correct subject tree/spec/policy; independent role provenance; changed content invalidates verdict; missing evidence cannot approve; minor vs material defects; bounded dispute handling |
| Integration | Real composed-tree checks; trunk changed after preparation; dirty checkout; conflicts; complete close before final review; no unauthorized artifact approval; publication policy honored |
| Recovery | Crash at each durable boundary; existing process ownership uncertain; candidate/receipt written but not promoted; promoted but intake not run; cleanup interrupted; no duplicate work or close |
| Partial/cancelled | Preserved code/report; terminal does not mean accepted implementation; dependencies stay unsatisfied or are explicitly rewritten; successor deduplication |
| Adoption | Fresh green scaffold; preserved adopter files; supported old upgrade; non-Python tooling; Windows/POSIX; absent advanced layers have no required imports |
| Assurance | Gate/check failure honesty; secrets and optional privacy behavior; trace integrity; unchanged human approval authority; normative amendment invalidates attestation |
| User-facing | One explainable next-action view; operator sees a concrete blocked decision; no historical record is presented as a living requirement; status after fresh-clone recovery |

Test selection strategy:

1. Small deterministic unit examples for policy boundaries and meaningful failure messages.
2. Property/state-sequence tests for graph ordering, unique claims, bounded transitions, and idempotent recovery. Hypothesis is optional development tooling, not a shipped dependency.
3. A limited real-Git suite for the filesystem, hooks, refs, worktrees, and candidate publication boundaries. Mocks cannot establish those guarantees.
4. Fresh-scaffold and upgrade tests per supported capability/OS contract, not every combinatorial toggle permutation. For HTML, use P9R’s affected-capability selection and the [selection table](LLR-AND-RENDERING.md#run-expensive-rendering-tests-when-the-rendering-capability-can-be-affected); do not omit shared registry/status/approval tests merely because their filename includes trajectory.
5. Human acceptance of first-use and owner-decision clarity. Almost entirely automated TC coverage cannot establish that the process feels proportionate.

Record before/after suite duration on the same environment. Do not transfer the old smoke membership ratchet mechanically to a changed implementation: review the behavioral bar first, then change any membership baseline with its reason. Existing checks remain mandatory until that change is approved.

## 5. Rollback and migration integrity

Before enabling the new writer, retain the old kit revision, a clean paused state, and an export of open specs and claims. Back up by normal Git references and copies; no rewriting or deletion of owner history.

- Before the first new accepted mutation, rollback can select the old runner with the untouched old state.
- After new mutations, rolling code back alone is insufficient. Pause/drain, translate new open state through a tested reverse converter if supported, or use an explicit forward repair. Never reset trunk to erase accepted work or owner rulings.
- Historical old verdicts remain historical; the new integrator requires its own evidence for new candidates. Do not globally grandfather legacy review files.
- An unsupported adopter format stops that migration with a report. It does not become a permanent silent runtime fallback.
- A package that adds a new path must name the old path it removes and the release that removes it. P10 is part of the deliverable, not an optional cleanup wish.

## 6. Effort and agent use

Do not price this from the current registry size or claim a credible calendar estimate before P0/P5. The high-risk work is evidence/publication/recovery, not writing the scheduler. Re-estimate after the integration experiment and the first end-to-end fixture.

Use Luna for bounded tasks with explicit evidence:

- Census and old→new obligation/test mappings, with spot-check review.
- Read-only scheduler replays and documented differences.
- Deterministic fixture creation and mechanical adapter cleanup after contracts settle.
- Documentation/link updates and deletion-ledger verification.

Use a stronger architectural reviewer for the state/authority contract, intake transaction, exact-tree integration and crash model, policy changes, and final consolidation decisions. Use an independent reviewer of the configured family for acceptance. This is a work-allocation recommendation, not a new model-routing policy. Record actual tier and roster identity so savings can be assessed rather than assumed.

The useful completion criterion is not “fewer files” or “fewer tests.” It is: one WI per assignment; one intake decision boundary; one scheduler answer; one review subject; one terminal outcome; preserved stakeholder evidence; and a demonstrated reduction in the work required to understand and operate the kit.
