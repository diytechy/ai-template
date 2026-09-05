# Adversarial review of the 2026-09-05 redesign plan

## Overall verdict

**Adopt-with-corrections.** The plan's evidence base is unusually sound — every code citation I spot-checked was accurate at the current checkout (`_judgement_first` at `dispatch.py:368`, multi-WI spine batching at `dispatch.py:453`, the in-admission consolidation census at `dispatch.py:1100`, `order_key` at `schedule.py:548`, the four-field `queue_digest` at `consolidate.py:170`, the peel machinery in `kitlib/verdict.py`, the README-vs-`process.toml` dial drift at `README.md:418` vs `docs/process.toml:116`, the 8-session plan happy path at `plan_round.py:81`, and the September 5 report's claims). The four-responsibility split, one-WI-per-lane, intake-before-eligibility, and the P5 stop/go gate genuinely serve the user's vision, and policy changes are flagged rather than smuggled. The plan's real weaknesses are **sequencing** (the new kernel would operate against a spine that still mandates the old behavior until P9), and **three underspecified corners of the serialized-integration design** (human-hold re-approval, affected-scope determination, and which policy revision governs at review time). None requires a new platform; all have small fixes.

## Findings

### F-01 — BLOCKER — Spine amendments are sequenced after the kernel that violates them
**Target:** IMPLEMENTATION.md P8 ("Done when… required repository checks pass") and P9; README §6 decision 4.
**Category:** demonstrated internal inconsistency in the plan.
**Failure scenario:** SR-148 (Approved) mandates the exact selection contract the kernel replaces — "ready adjudication rows first, as a stable partition applied at admission," handback precedence, and the current ordering (`docs/requirements/system-requirements.toml:599-601`); SR-144 mandates that a partial close "merges like any other branch" (`:557`); SR-157/LLR-210/TC-208 pin the census-triggered consolidation subsystem (`docs/test/test-cases.toml:2113-2122`); LLR-149/LLR-159 pin batch admission. P8 runs the new kernel on real WIs and requires "required repository checks pass" — but trace/gate/dogfood checks enforce the old approved spine until P9 applies the disposition map. As written, P8's exit criterion is unsatisfiable, or the kernel operates outside the gates, which the vision forbids. P0's "obtain that decision before enabling new assignment creation" gets a *decision*, not the reviewed spine amendment the gates actually read.
**Minimal correction:** carve a small owner-approved amendment package (assignment cardinality, admission-inside-scheduler, consolidation-at-intake, partial-close semantics) out of P9 and gate P6/P8 enablement on it landing. Leave bulk consolidation in P9.

### F-02 — MAJOR — Human-held candidates can churn or livelock under the exact-tree rule
**Target:** README §3 "Simpler integration," final paragraph ("Human-held final approval…").
**Category:** architectural inference.
**Failure scenario:** the plan releases the integration turn on a human hold, lets other work continue, and rules that "a stale human decision cannot authorize a new tree." Every acceptance moves trunk, so any intervening promotion forces re-preparation → new tree T′ → the owner's approval is void → re-approve. With this repo's dial (`human_approval_through = "DevStg-Needs"`, `docs/process.toml:116`) holds are frequent; the owner must win a race against every active lane, repeatedly. Note this also contradicts the current default policy the plan says to preserve: `_admission`'s surface arm stops all new admission once an approval is pending (`dispatch.py:424-427`).
**Minimal correction:** one paragraph defining the approval *subject* — the WI's content delta plus named normative artifacts — so a clean mechanical recompose with identical delta preserves the decision; or state that the existing hold-stops-admission policy governs and drop turn-release for human-held tiers.

### F-03 — MAJOR — "Affected scope" for pending reconciliation is undefined while its only input is declared untrustworthy
**Target:** README §3 creation contract ("Detailed touched-file lists are optional hints; inaccurate declarations must not establish safety") and scheduling contract ("A pending affected-scope reconciliation is resolved before that scope is admitted").
**Category:** architectural inference with counterexample.
**Failure scenario:** if declared file lists cannot establish safety, nothing named in the plan can bound a reconciliation's scope, so the conservative reading makes every pending reconciliation global — "drains the station and runs alone" — on every new proposal. Since most accepted WIs emit follow-up proposals, this reintroduces the idle-station stall the plan deletes (`dispatch.py:1088-1100`), potentially worse than today's once-per-judged-queue census.
**Minimal correction:** name the tracked structured fields that *do* scope affectedness (requirement refs, registry rows, dependency edges, declared exclusive resources), with global as the fallback only when those are absent.

### F-04 — MAJOR — Claim-time policy pinning can bypass a mid-flight authority tightening
**Target:** README §3 assignment contract ("chosen route, policy revision") and integration sequence step 3 ("obtain the final review against T, the WI scope, and policy"); IMPLEMENTATION.md P1 domain records.
**Category:** architectural inference.
**Failure scenario:** the Assignment pins a policy revision at claim and active specs are frozen. If the owner raises `human_approval_through` while a WI is in flight, an integration turn that evaluates authority against the pinned revision machine-approves work the human now holds — exactly the failure SN-029's acceptance directs toward "MORE human involvement" (`docs/requirements/stakeholder-needs.toml:244`). The plan never says which revision governs the final review and promotion.
**Minimal correction:** one sentence: approval authority and holds are evaluated at the integration turn against current trunk policy; the pinned revision is provenance for the build phase only.

### F-05 — MAJOR — The serialized-turn measurement ignores measured review churn
**Target:** README §3 "Simpler integration" ("measure head-of-line blocking"); IMPLEMENTATION.md P5 measurement bullet.
**Category:** architectural inference grounded in repo data.
**Failure scenario:** the plan treats the turn as roughly one per WI, but the repo's own data (`docs/decisions-for-review-2026-09-05.md`, Appendix A) shows builds averaging ~3.2 review rounds, up to 12, with review-heavy WIs at 21,427–38,189 s wall. Each material defect returns to build, and each rework needs a fresh compose + checks + final review turn; intake adjudication (measured 151–1,381 s per disposition) then occupies "the next serialized transaction." The serial section per WI is rounds × (compose + checks + review), not one turn. A P5 measurement scripted around single-pass acceptance would pass a design that stalls in practice.
**Minimal correction:** require P5's measurement to model multi-round rework and intake latency at the configured lane count, and declare the acceptance threshold *before* running the experiment.

### F-06 — MAJOR — No concrete disposition for the dominant spine-train case
**Target:** README §2.3 and §6 decision 1; IMPLEMENTATION.md P0 batching-disposition bullet.
**Category:** explicit proposed policy change (correctly flagged for owner approval — not itself a defect); the gap is the missing decision material.
**Failure scenario:** today all ready same-kind spine rows admit as one exclusive train (`dispatch.py:452-453`); Appendix A shows a real four-row train (WI-584/587/588/589) sharing one lane. Under one-WI-per-lane these become either four serial integration turns (four compose/check/review cycles where one existed) or one consolidated WI of the size §2.3's own qualification warns against. The owner is asked to decide cardinality without seeing this cost.
**Minimal correction:** add to P0 a census of historical train sizes and a stated default rule (consolidate at intake when rows share one acceptance decision, otherwise sequence), so decision 1 is concrete.

### F-07 — MINOR — Wrong SR cited for partial-close reconciliation
**Target:** IMPLEMENTATION.md P6, "Reconcile this change explicitly with SR-144/SR-169."
**Category:** demonstrated citation defect.
**Failure scenario:** SR-169 is "The state view shows how the parts connect" — the SN-023 architecture-graph row (`docs/requirements/system-requirements.toml:860-872`), unrelated to lane close. A P6 implementer reconciling against it would miss the real conflicting rows. SR-144 is correct; the plausible second citations are SR-173 (ordered, no-partial-result regeneration, `:914-919`) and LLR-182 (terminal-outcome vocabulary under SR-144, `low-level-requirements.toml:1881`).
**Minimal correction:** fix the citation (verify against the plan's own baseline `a9bf6cee`; at the current checkout, one docs-only commit later, SR-169 is the state-view row).

### F-08 — MINOR — The `queue_digest` gap is a documented tradeoff, not an oversight, and the proposed fix has a stated cost
**Target:** README §3 creation contract (fingerprint paragraph); IMPLEMENTATION.md P1 staleness bullet.
**Category:** demonstrated context (docstring) + inference; the proposal itself is properly labeled "investigate."
**Failure scenario:** `consolidate.py:170-180` argues *deliberately* for four fields — hashing Deliverable/BuildTier "would re-arm the census on an edit that changes no answer." The plan's conservative whole-snapshot fingerprint inverts that: nearly every acceptance-text edit invalidates prior decisions, decision reuse (intake step 3) almost never fires, and semantic adjudication cost rises — against the plan's own "do not invoke an LLM on every tick" goal. The gap is real (an edit that makes two rows' Done-when overlap does not re-arm today's census), but the plan should argue against the recorded rationale, not past it.
**Minimal correction:** cite the docstring's rationale in §2.2/P1 and state the expected re-adjudication frequency as a P5/P8 measurement, alongside the invalidation-optimization note already present.

### F-09 — MINOR — P9's capability manifest contradicts the plan's own anti-framework rule
**Target:** IMPLEMENTATION.md P9 ("small declarative capability manifest") vs README §2.6 ("Avoid inventing a general plugin framework: the existing bootstrap mapping can express a few explicit capability sets").
**Category:** demonstrated internal inconsistency; simplicity risk.
**Failure scenario:** a new manifest format with artifact lists, requirement IDs, and verification entry points is precisely the custom machinery the user fears, and a second home for information the bootstrap mapping and spine already carry.
**Minimal correction:** either express the three capability sets in the existing bootstrap mapping as the README states, or explicitly define the manifest *as* that mapping with no new schema.

### F-10 — MINOR — The deletion ledger must count receipt-protocol machinery against the peeling it deletes
**Target:** IMPLEMENTATION.md P0 deletion ledger; P5 "Deletion enabled if successful."
**Category:** architectural inference.
**Failure scenario:** the deleted interpretation machinery (refresh/close peeling, governing-revision walks in `kitlib/verdict.py`) is replaced by protocol machinery: a versioned receipt schema, the `trajectory/candidates/<attempt>` namespace and retention policy, a full-clone recovery/export procedure, turn reservation, and re-preparation rules. P5's stop/go as written is judged on correctness and latency only; a design that is correct but net-neutral in complexity could pass.
**Minimal correction:** require the P0/P5 ledger to tally added protocol surface against deleted interpretation surface, so "simpler" is part of the stop/go bar, not assumed.

### F-11 — MINOR — SN-006/SN-029 "tension" is narrower than the plan implies
**Target:** README §3 assignment contract ("Clarify the tension… in SN-006/SN-029") and P1's blocking owner ruling.
**Category:** demonstrated by row texts.
**Failure scenario:** the approved acceptance texts already partition most cases — approval-authority faults resolve toward more human involvement (SN-029 acceptance, `stakeholder-needs.toml:244`), while limit-*enforcement* faults record and continue (SN-006 acceptance, `:135`). A broad "clarify the tension" ruling request invites re-litigating approved text and gives P6 an unnecessarily wide blocker.
**Minimal correction:** narrow P1's policy question to the actual gray zone — a fault in the machinery that decides whether work is independent of a pending hold — and cite the two acceptance clauses as already settling the rest.

### F-12 — MINOR — The turn cannot bind the human's trunk, and detection is deferred to promotion
**Target:** README §3 integration sequence steps 1 and 4.
**Category:** architectural inference.
**Failure scenario:** "trunk mutations and new claims wait during this turn" is enforceable on the coordinator, not on the owner, who commits rulings/approvals directly under `push = "human"`. An owner commit landing mid-turn is discovered only at "promote only if trunk still equals B," after a full compose + check + review has been spent.
**Minimal correction:** state that the coordinator re-checks trunk-equals-B at each phase boundary within the turn and aborts early, and note the owner interaction in operator docs. Cost only, not correctness.

## What survived adversarial challenge

Atomicity of the intake transaction (single-writer, stage-then-one-commit) is Git-native and sound; the crash-recovery model (claim-before-launch, crash-as-interrupted-attempt, P5 crash injection at every durable boundary) is well specified; stale-decision refusal and content-change-invalidates-verdict rules are coherent; and the currently idle, tracked-paused station (`docs/work/pause` exists, no `docs/work/active/`) makes the P2 drain-before-switch migration condition realistic. I found no fabricated evidence; the evidence document's self-declared limits match what I could verify.

## Hard design decisions still unresolved

1. Assignment cardinality for spine work (owner decision; F-06 supplies the missing cost data).
2. The approval subject for human-held candidates under trunk motion (F-02).
3. Evidence that scopes a reconciliation below global (F-03).
4. Claim-time vs. current policy at the integration turn (F-04).
5. Whether commit-metadata receipts can carry required evidence at all — correctly gated at P5, including hook/signing/CI binding and candidate-branch retention.
6. Ordering-policy simplification (dropping downstream/hard-path ranking) — explicit policy change awaiting owner replay review, not a defect.

## Suggested changes that would worsen simplicity if taken as written

- The whole-snapshot intake fingerprint without an invalidation policy (F-08) — trades one staleness bug for systemic adjudication churn.
- The P9 capability manifest as a new format (F-09).
- The one-size review-result schema for plans, implementation, consolidation, *and* subjective critique: watch for lowest-common-denominator fields plus per-subject extensions recreating today's parser sprawl — keep the shared part to provenance/finding/disposition and let subjects own their criteria payloads.
- The receipt protocol itself if P5's ledger shows it merely relocates complexity (F-10).

**Not run:** no tests, no commands, no implementation — this was a read-only inspection of the checkout at `0d6f3398` (one docs commit past the plan's stated baseline `a9bf6cee`), which is why line numbers could differ marginally from the plan's citations; none I checked did.