# Cross-reference — this plan against the independent codex plan

Written 2026-09-05 on branch `redesign-crossref-2026-09-05` (worktree beside the
repo; `contract_split` untouched). Compares `PLAN.md` (this folder, after review
round 1) with the owner's parallel codex plan at
`docs/ai-template-redesign-2026-09-05-codex/` — its `README.md`,
`IMPLEMENTATION.md`, `EVIDENCE-AND-TOOLS.md`, `LLR-AND-RENDERING.md`, and the
Claude Fable adversarial review it received (`FABLE-REVIEW.md`, twelve
findings, all accepted) with dispositions. Neither plan read the other while
being written; the codex evidence document says so explicitly, and this folder's
brief to its own reviewer forbade reading the codex folder.

**Short answer.** The two plans were built independently, from the same repo,
by different model families, and reached the same organizing model, the same
two structural fixes and the same two owner-raised remedies. Where they differ,
the codex plan is more careful about *sequencing and authority* and this plan
is more careful about *measurement and what to cut*. Each caught something the
other's adversarial reviewer missed. Ten elements from the codex plan are worth
incorporating; three of its proposals should stay experiments, not defaults;
two of its positions this plan should adopt over its own. The applied changes
are listed in §5 and were made to `PLAN.md` in the same commit as this file.

## 1. Where the plans agree (independently)

| Point | This plan | Codex plan |
|---|---|---|
| Organizing model | The owner's four-stage loop (§4.4) | "Your four-step loop is the right organizing model" (README §0) |
| One WI per lane, batch admission gone | §2.2, §4.4 | README §2.3: "the assignment schema contains one `wi_id`, never a list" |
| Judge overlap before a row is eligible | Intake at `proposed/` (§4.3) | "authoritative intake reconciliation is the eligibility boundary" (README §2.2, §6 decision 2) |
| A closing worker cannot consolidate the trunk queue | §4 of the sitting report, restated §4.3 | README §2.2 cites and agrees with that argument |
| Persist the claim's integration base (OI-84); coordinator exits on code drift (OI-83) | §4.4 rules; Phase 0 | README §2.4; P6 "pin the running coordinator code revision" |
| No learned worker-tier router; small telemetry instrument instead | §2 of the sitting report; PLAN §3 gap 3 | README §2.7: "support small instrumentation improvements, not a learned router" |
| Keep the stage ladder and the owner's authority dials during the migration | §4.2 after review round 1 | README §1: "Do not collapse stages, change human authority, and replace orchestration in the same experiment" |
| No new frameworks, no event store, no schema engine, no SQLite authority | §4.6 tool verdicts | README §5; EVIDENCE external-tools table |
| LLR as the current design, not a permanent constraint; a replacement route in normal intake | §4.6 (replace-don't-amend, residue detector) | LLR-AND-RENDERING §1 (third intake route: "parent sound, design unsuitable") |
| Rendering as a package with its own test family, selected by affected capability, unconditional at phase close / CI | §4.7 | LLR-AND-RENDERING §2, P9R |
| Migrate by slices behind a rollback, one mutating runner at a time | §5 strangler order, Phase 3 flag | IMPLEMENTATION §5 and P10 |
| Every SN gets an explicit disposition; "optional" never means an approved need disappears | §1 promises table; Phase 1a manifest | README §1: "All 27 existing needs must receive an explicit disposition" |

Two independently-built plans agreeing on all of that is the strongest evidence
either has that the diagnosis is right.

## 2. Where they differ, and which side to take

### 2.1 Evidence identity: keep the governing identity, or serialize the final review?

**This plan** keeps the kit's existing verdict identity (tree minus record
paths, refresh peel kept) and removes one exception, the mechanical-close peel,
by having the worker close before the final round (§4.4, corrected in review
round 1).

**Codex** proposes replacing the whole identity apparatus: serialize final
candidate preparation → checks → final review → promotion in one reserved
"integration turn"; freeze the exact composed tree T; record acceptance in a
same-tree receipt commit; retain candidate branches under
`trajectory/candidates/<attempt>` (README §3 "Simpler integration"; P5). No
record-path exclusion, no refresh peel, no close peel. Its own Fable reviewer
flagged the costs: head-of-line blocking of every lane behind one long final
review (F-05), and the risk that receipt schemas, candidate retention, recovery
export and turn reservation merely relocate the complexity peeling carried
(F-10). Codex accepted both and made P5 a predeclared stop/go experiment.

**Assessment.** Codex's ordering is the cleaner *end state*: reviewing the
composed tree that will actually be promoted removes the refresh peel as well
as the close peel, and it answers "what exactly was reviewed" without any
reconstruction. But it trades every lane's independence for it, and the repo's
own data (about 3.2 review rounds per build, up to 12) means the serial section
per WI is rounds × (compose + check + review), not one turn. This plan's design
removes half the machinery at no concurrency cost. **Take: this plan's design
as the default, codex's as a bounded experiment** with codex's own P5
conditions attached — a predeclared latency budget at the configured lane
count using the historical round distribution, and a ledger that counts the
protocol surface added against the peeling deleted. If the experiment passes,
adopt it in Phase 3; if not, the default stands. (Applied: §4.4, §7.)

### 2.2 Amend the approved contracts BEFORE enabling the new runner

Codex's Fable review found this as its one BLOCKER (F-01): SR-148 approves the
current admission partition, LLR-149 the multi-WI batch, SR-144 the partial
close, SR-157/LLR-210/TC-208 the census consolidation. A new runner enabled
before those rows are amended either fails the gates or runs outside them.
Codex added P1A — a narrow, reviewed amendment set landed before P6/P8.

**This plan has the same defect and its reviewer did not catch it.** Phase 3
rebuilds the loop while Phase 1b prunes the spine, and nothing says the rows
that *mandate the old behaviour* are amended before the new behaviour runs.
**Take: codex's P1A, as a prerequisite inside Phase 2.** (Applied.)

### 2.3 The scheduler as the sole admission authority

Codex names a defect this plan glossed: `schedule.order_key` and
`dispatch._judgement_first` give two different answers to "what runs next", and
the dashboard shows the first while the dispatcher executes the second (README
§2.1). Its remedy is one pure scheduling result — selected assignments plus the
reason every other WI waits — consumed identically by CLI, dashboard and
dispatcher, with `next --explain`. This plan kept `schedule.py` "as is" and
only deleted batch admission. **Take codex's remedy.** (Applied: §4.3, §4.4.)

### 2.4 Intake precision

Codex's intake contract carries four things this plan's did not: the affected
queued IDs derived from structured references (requirement rows, dependency
closure, declared shared/exclusive resources), with a global hold when scope
is missing or ambiguous (Fable F-03); the split between transaction staleness
(snapshot revision) and semantic reuse (a fingerprint over the adjudicated
scope, not over Deliverable/telemetry/tier — preserving the deliberate
four-field `queue_digest` rationale, F-08); deduplication of repeated event
proposals so a dismissed finding cannot mint work forever; and a one-time
exclusive reconciliation WI for the legacy queue instead of reconciling every
idle tick. **Take all four.** (Applied: §4.3.)

### 2.5 Authority at review time and human holds

Codex, after F-02 and F-04: claim-time policy is execution provenance only;
approval authority, holds and evidence are evaluated against *current trunk
policy* at each phase boundary and at promotion, so a mid-flight tightening of
`human_approval_through` applies to in-flight work. Under a stopping hold with
`keep_nondependent = false`, drain, then prepare the held candidate on the
settled trunk so the owner is not asked to race a moving trunk; artifact
attestation (names normative content) is distinct from candidate approval
(names tree T, never carried to T′). This plan said nothing about holds or
policy versions. **Take both.** (Applied: §4.4.)

### 2.6 The LLR id question

Both plans add the third intake route. They differ on the id: this plan's
§4.6 said a mechanism change *replaces* the row (new id, `supersedes`); codex
says keep the id when it still names the same design responsibility and only
the content is amended, and mint a successor only when obligations split,
combine or disappear. Codex is right on the mechanism, and adopting it also
removes the re-pointing cost this plan was inventing tooling to pay. What
matters against the owner's concern is that the *text* is rewritten to
describe the new design rather than patched around, which this plan's residue
detector still enforces. **Take codex's id policy; keep this plan's detector
and its single-adjudication price.** (Applied: §4.6.)

### 2.7 Rendering selection

Both isolate rendering. Codex's selection table is more complete than this
plan's path trigger: it names the shared snapshot as the input contract, adds
"unknown impact or unavailable comparison base → run the broad suite and say
why", requires the selection to compare the whole change against its recorded
base (renames and deletions included), forbids a required check from going
pending through a workflow-level path skip, and — the point this plan missed —
notes that SN-007's full-suite acceptance must be amended *before* any
narrowing is enabled. **Take the table and the SN-007 note.** (Applied: §4.7.)

### 2.8 Capability sets, review envelope, telemetry record

Three smaller codex elements worth taking: express the three capability sets
(manual core / managed loop / advanced planning-architecture-reporting) in the
existing bootstrap mapping with adoption tests that a disabled capability is
absent from core imports (README §2.6, P9, Fable F-09 — no second manifest);
one review-result envelope whose common part is only provenance, findings and
disposition, with typed subject-specific criteria payloads, and arbitration
capped at one attempt before a human (README §3 "Controlled plans"); and the
full per-session telemetry record — WI, attempt, role, provider/model, roster
row, tier, policy revision, timestamps, review outcome, terminal result —
written once (README §2.7). (Applied: §4.1, §4.4, §3.)

### 2.9 Effort

Codex refuses to estimate: "Do not price this from the current registry size
or claim a credible calendar estimate before P0/P5" (IMPLEMENTATION §6). This
plan gives about 36 days. Codex is right that the number is not credible until
the Phase 1a manifest and the integration experiment exist; the owner still
needs an order of magnitude to decide whether to start. **Keep the figure,
label it indicative, re-estimate after Phase 1a and the exact-tree experiment.**
(Applied: §5 totals.)

## 3. What this plan has that codex does not

- **Measured evidence.** Appendix A (every LLR/TC/IF classified; per-need
  mass), appendix B (module map, stage mass, import closure, batch-lane sizing,
  seven parsers / eight result conventions / seven prompt mechanisms), appendix
  C (about fifty tools against five objectives). Codex's evidence document is
  a census of counts plus a source map; it explicitly did not measure the
  render cost or the classifications ("remain P0 work"). Codex's P0 is largely
  what appendices A and B already are.
- **The control period and its decision gate** (Phase 0, from review round
  1). Codex's P5 stop/go tests the *new* design; nothing in codex measures
  whether the churn fixes already landed on 09-04/05 make a rebuild
  unnecessary. That is the cheaper experiment and it comes first.
- **The honesty-device diagnosis and the ratchet cuts** (§2.4, §4.5). Codex
  says "do not add new ratchets before the core is smaller" and stops there.
- **The amend-versus-uproot measurement** (218 detail rewrites, 1 row removed
  since August) and the render test timing (68 s / 38 s / 23 s on every
  commit). Codex raises both concerns qualitatively.
- **The stage-clamp mistake, caught and withdrawn.** Codex never made it.

## 4. What codex proposes that this plan should NOT adopt as written

- **The exact-tree receipt protocol as the default** (§2.1 above): experiment,
  not default.
- **Deferring all effort estimates**: the owner asked how big this is.
- **"Do not add new ratchets"** read as a veto on the escapes ratchet: that
  one closes an evasion path the existing ratchets leave open; it stays an
  optional WI, after the core is smaller.

## 5. Changes applied to PLAN.md in this commit

1. §4.1 — capability sets expressed in the bootstrap mapping; adoption tests
   for absence-when-disabled.
2. §4.3 — scheduler as the sole admission authority with an explainable
   decision object; intake records affected queued IDs with a global-hold
   fallback; transaction staleness split from semantic reuse; proposal
   deduplication; one legacy reconciliation WI.
3. §4.4 — authority evaluated against current trunk policy at each boundary;
   human-hold drain under `keep_nondependent = false`; artifact attestation vs
   candidate approval; review envelope and arbitration cap; the exact-tree
   integration turn as a bounded Phase 3 experiment with codex's P5 conditions.
4. §4.6 — id kept when the design responsibility is unchanged; successor only
   on split/merge/retire; detector and single-adjudication price retained.
5. §4.7 — codex's selection table adopted (unknown impact → broad run; whole
   change vs recorded base; no pending-by-path-skip); SN-007 amendment named
   as a precondition.
6. §3 gap 3 — the full telemetry record.
7. Phase 2 — a P1A-style contract-amendment prerequisite (SR-148, SR-144,
   SR-156, LLR-149/159/182/210 and their TCs) before Phase 3 enables any
   changed runtime behaviour.
8. Phase 1a — the six-way disposition vocabulary (keep / consolidate / move
   to design decision / move to optional capability / migration-only /
   retire).
9. §5 totals — effort labelled indicative, re-estimate point named.
10. §7 — decision 11: run the exact-tree experiment or not.
11. §8 — this cross-reference indexed as round 2.

## 6. A note on the two reviews

Each plan was reviewed adversarially by the other's model family — this one by
codex `gpt-6-astra`, codex's by Claude Fable 5 — and each reviewer found what
its own family's plan had missed: astra caught this plan's stage clamp and
automatic re-baseline; Fable caught codex's amend-before-enable sequencing and
its hold/policy-version gaps. Neither reviewer caught the defect the *other*
plan shared (astra did not flag amend-before-enable here). That is the
cross-family review doctrine working exactly as SN-026 describes it, and a
reason to keep both plans in the record rather than merge them into one.
