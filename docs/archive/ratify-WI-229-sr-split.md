# WI-229 oversized-SR migration and ratification

**State:** ATTESTED 2026-07-19 — stage 3 may proceed (record below).

This is the stage-1 migration plan required by
[`docs/archive/specs/WI-229.2026-07-20.md`](../archive/specs/WI-229.2026-07-20.md). It freezes the split IDs, the
post-split evidence parents, and the coverage-preservation rules. It does not
ratify itself. The worker that authored it must stop at the attestation boundary.

## Census and decision boundary

The census is against integration base
`808f95da957c1ce90476e8807acb784159255107`. Row size is the sum of the parsed
CSV field lengths (excluding separators and quoting). The live oversized set is:

| SR | Characters | SR | Characters |
|---|---:|---|---:|
| SR-037 | 2,225 | SR-038 | 2,022 |
| SR-044 | 3,143 | SR-045 | 3,278 |
| SR-047 | 2,426 | SR-048 | 2,131 |
| SR-051 | 2,580 | SR-058 | 2,508 |
| SR-063 | 2,477 | SR-064 | 2,438 |
| SR-066 | 3,796 |  |  |

The filed spec names SR-060, SR-061, and SR-065 as notable examples. Those rows
are now 1,282, 1,498, and 1,407 characters respectively and are not split by
this base-sensitive migration. Conversely, SR-037, SR-038, SR-047, SR-048,
SR-051, SR-058, SR-063, and SR-064 now cross the rule and are included. This is
the smallest interpretation consistent with “for each oversized SR”; expanding
the set to rows below the threshold would be unscoped cleanup.

## Supersession model

Stage 3 shall use these rules as one transaction:

1. Add a `SupersededBy` column to this meta-repo's SR registry. Each old SR
   remains at its stable ID, becomes a short `Verification=Inspection`,
   `Status=Verified` supersession-link row, and lists all replacement SR IDs.
   Its Requirement and AcceptanceCriteria describe only the link; none of its
   former implementation obligations remain there.
2. Extend `trace.py`'s optional-column handling so a non-empty `SupersededBy`
   is semicolon-separated, resolves only to other SR rows, contains no self-link
   or cycle, and is an integrity finding when invalid. This is compatibility for
   an adopted registry extension, not a new process rule; WI-229 does not edit
   `PROCESS.md`.
3. Reparent and honestly narrow every existing LLR and TC shown below. Existing
   IDs and Evidence paths survive. A narrowed TC may cite the same test module
   but only the tests relevant to its replacement SR. New LLR/TC IDs fill the
   independent obligations that a composite row used to hide.
4. Mint TC-099 as an `Inspection`, `Tier=Full`, `Automated=Yes` check over the
   eleven old rows: every link resolves, is acyclic, and the old row has no LLR
   parent. TC-099 verifies all eleven supersession-link SRs. This keeps the old
   IDs traceable without preserving them as implementation umbrellas.
5. All replacement rows inherit the old row's SN references, priority, phase,
   and area. They start `Planned`, which honestly regresses the derived gate;
   they move to `Verified` only after the split evidence and complete G3 harness
   pass. No replacement active SR may exceed 2,000 characters by the same
   parsed-field metric.

## Frozen split and evidence map

`keep` means narrow and reparent the existing row. `new` reserves an exact ID
for stage 3. Every currently attached LLR and TC occurs in this table exactly
once; TC-099 is the only evidence retained on an old parent.

| Old SR | New SR | Atomic obligation | SN-Refs | Post-split LLR | Post-split TC |
|---|---|---|---|---|---|
| SR-037 | SR-067 | Validate WI IDs, resolvable predecessors, and an acyclic dependency DAG; placeholder/absent registries are vacuous and the declared opt-out silences the step. | SN-002;SN-012 | keep LLR-034 | keep TC-037 |
| SR-037 | SR-068 | Enforce Deliverable/status coherence and strict open-WI SpecRef resolution, with the declared plain/strict severities. | SN-002;SN-012 | new LLR-077 | new TC-077 |
| SR-037 | SR-069 | Reject a done WI token from hand-edited status while standing down for the generated marker and open/unknown IDs. | SN-002;SN-012 | keep LLR-075 | keep TC-075 |
| SR-038 | SR-070 | Generate the offline completeness tiles, SN→SR→LLR→TC hierarchy, and WI roadmap in one self-contained root HTML file. | SN-010;SN-021 | keep LLR-035 | keep TC-038 |
| SR-038 | SR-071 | Conditionally render the software/component and OKF knowledge views, omitting each without its source bundle. | SN-010;SN-021 | new LLR-078 | new TC-078 |
| SR-038 | SR-072 | Make dashboard generation byte-deterministic, responsive, and freshness-gated, with a git-derived as-of stamp excluded from stamp-only comparisons. | SN-010;SN-021 | new LLR-079 | new TC-079 |
| SR-044 | SR-073 | Integrity-check IF IDs, SR back-links, Component references, and the best-effort ThisProject-to-LLR-module advisory. | SN-023;SN-002 | keep LLR-041 | keep TC-044 |
| SR-044 | SR-074 | Emit opt-out, warn-first architecture-connectivity coverage for undeclared endpoints/directions, uncited Active seams, and dangling Contracts citations. | SN-023;SN-002 | keep LLR-042 | new TC-080 |
| SR-044 | SR-075 | Render declared IF seams in the dashboard and architecture map, with the table fallback when seams are absent. | SN-023;SN-002 | new LLR-080 | new TC-081 |
| SR-044 | SR-076 | Report a cross-component import edge with no covering declared interface, with the declared vacuity and strictness rules. | SN-023;SN-002 | keep LLR-067 | keep TC-067 |
| SR-044 | SR-077 | Validate an armed spec's Interfaces section, including resolvable IDs, Proposed rationale, and the intra-module escape. | SN-023;SN-002 | keep LLR-068 | keep TC-068 |
| SR-044 | SR-078 | Compare rival-plan clause/SR/interface coverage and distinguish findings from malformed inputs and absent-registry notes. | SN-023;SN-002 | keep LLR-069 | keep TC-069 |
| SR-045 | SR-079 | Parse and select the agent pair-row registry: enable-list resolution, version ordering, Env merge, cooldown, family preference/fallback, and tier-up-never-down. | SN-006;SN-016 | keep LLR-044 | keep TC-046 |
| SR-045 | SR-080 | Schedule the review-policy sessions with redacted prompt-map briefs, verdict parsing, and selection logging while preserving unmanaged behavior. | SN-006;SN-016 | keep LLR-045 | new TC-082 |
| SR-045 | SR-081 | Score review substance and maintain the advisory decay history while treating anti-gaming tripwires as non-scored gates. | SN-006;SN-016 | keep LLR-046 | new TC-083 |
| SR-045 | SR-082 | Apply fixed win-stay/lose-shift escalation and gate-policy paging for shared failure, contradictions, and tripwires. | SN-006;SN-016 | new LLR-081 | new TC-084 |
| SR-045 | SR-083 | Select two fresh planner hats across families where possible and use the bounded runtime-nonresponse fallback. | SN-006;SN-016 | keep LLR-072 | keep TC-072 |
| SR-047 | SR-084 | Trigger a fresh family-heterogeneous Critique session only for Critique-scoped builds and construct its rubric/intent/artifact brief without self-assessment. | SN-024;SN-006 | keep LLR-048 | keep TC-048 |
| SR-047 | SR-085 | Iterate bounded BUILD↔CRITIQUE rework and page through gate policy at the critique-round cap. | SN-024;SN-006 | new LLR-082 | new TC-085 |
| SR-047 | SR-086 | Accept the Critique verification vocabulary while retaining its LLR requirement, and warn on a lax-TC closure after CHANGES-REQUESTED. | SN-024;SN-006 | new LLR-083 (trace vocabulary); new LLR-084 (closure ratchet) | new TC-086 |
| SR-048 | SR-087 | Derive the top-level module/component view and enforce TOP_VIEW_MAX with nesting, opt-out, and small/absent-inventory vacuity. | SN-023;SN-012 | keep LLR-049 | keep TC-049 |
| SR-048 | SR-088 | Render containerized How-SW membership and boundary-aggregated seams, retaining the flat fallback without containment. | SN-023;SN-012 | new LLR-085 | new TC-087 |
| SR-051 | SR-089 | Tier the When view phase→workstream→WI by count, expose delivery phase, and aggregate parent edges from child edges. | SN-010;SN-021 | keep LLR-052 | keep TC-052 |
| SR-051 | SR-090 | Tier the How-SW view from components to modules whenever containment exists and bound its top level by TOP_VIEW_MAX. | SN-010;SN-021 | new LLR-086 | new TC-088 |
| SR-051 | SR-091 | Attach IF seams to visible block ports and aggregate cross-container seams to container boundaries. | SN-010;SN-021 | new LLR-087 | new TC-089 |
| SR-051 | SR-092 | Descend one hierarchy layer by pointer or keyboard and restore parents through a breadcrumb. | SN-010;SN-021 | new LLR-088 | new TC-090 |
| SR-058 | SR-093 | Purely classify every declared safety/policy input into a scheduling class plus deterministic reason codes. | SN-025;SN-008 | keep LLR-059 | keep TC-059 |
| SR-058 | SR-094 | Cross-check declarations against structural evidence and fail an invalid/missing/contradictory WI closed without stopping disjoint classified work. | SN-025;SN-008 | new LLR-089 | new TC-091 |
| SR-058 | SR-095 | Pack only ordinary work optimistically; serialize protected work, isolate forced single-WI work, and cluster ready spine/gate/attestation work into homogeneous cap-bounded trains. | SN-025;SN-008 | new LLR-090 | new TC-092 |
| SR-063 | SR-096 | Compose and review each train through one integration writer, regenerate authority, run the required bar, and CAS-advance the integration ref. | SN-025;SN-008 | keep LLR-064 | keep TC-064 |
| SR-063 | SR-097 | Record a worker blocker as a smaller serialized disposition with BlockRef/evidence and no review-pass claim. | SN-025;SN-008 | new LLR-091 | new TC-093 |
| SR-063 | SR-098 | Publish through a durable compare-and-swap intent and sync only an exactly clean/expected development worktree, retaining recoverable evidence on failure. | SN-025;SN-008 | new LLR-092 | new TC-094 |
| SR-064 | SR-099 | Enumerate Git evidence before choosing authority and initialize a missing integration ref only when no ownership evidence exists. | SN-025;SN-017 | keep LLR-065 | keep TC-065 |
| SR-064 | SR-100 | Reconstruct one owner/state per WI and train, quarantine ambiguity/duplicate reservations, and fail closed on unprovable ownership. | SN-025;SN-017 | new LLR-093 | new TC-095 |
| SR-064 | SR-101 | Recover every reservation/integration/publication boundary without double assignment, false completion, evidence loss, or dependence on out/dispatch. | SN-025;SN-017 | new LLR-094 | new TC-096 |
| SR-066 | SR-102 | Enforce the typed dual-plan state machine, spend ledger, one-repair/revision caps, position-swap agreement, and PAGE outcomes. | SN-024;SN-006 | keep LLR-070 | keep TC-070 |
| SR-066 | SR-103 | Assemble allowlist-only planner/critic/arbiter briefs from SR/IF registries with strict prompt-template filling. | SN-024;SN-006 | keep LLR-071 | keep TC-071 |
| SR-066 | SR-104 | Adapt mechanical coverage results into clean, implicated-repair, repeated-failure, and malformed round outcomes. | SN-024;SN-006 | keep LLR-073 | keep TC-073 |
| SR-066 | SR-105 | Persist stable round artifacts and file selected queued child WIs with mapped predecessors and registry-valid fields. | SN-024;SN-006 | keep LLR-074 | keep TC-074 |
| SR-066 | SR-106 | Run two planners, cross-critiques, bounded revisions, and position-swapped arbiters as fresh sessions and select only on true-plan agreement. | SN-024;SN-006 | keep LLR-076 | keep TC-076 |
| SR-066 | SR-107 | Refuse a dual row on the direct worker path and derive a contradictory-safe single-WI dispatcher classification from PlanMode. | SN-024;SN-006 | new LLR-095 | new TC-097 |
| SR-066 | SR-108 | Commit SELECT or PAGE as one serialized docs-only disposition and map PAGE through gate policy without pausing disjoint work under autonomous policy. | SN-024;SN-006 | new LLR-096 | new TC-098 |

The old-row link sets are therefore frozen as:

| Old row | SupersededBy |
|---|---|
| SR-037 | SR-067;SR-068;SR-069 |
| SR-038 | SR-070;SR-071;SR-072 |
| SR-044 | SR-073;SR-074;SR-075;SR-076;SR-077;SR-078 |
| SR-045 | SR-079;SR-080;SR-081;SR-082;SR-083 |
| SR-047 | SR-084;SR-085;SR-086 |
| SR-048 | SR-087;SR-088 |
| SR-051 | SR-089;SR-090;SR-091;SR-092 |
| SR-058 | SR-093;SR-094;SR-095 |
| SR-063 | SR-096;SR-097;SR-098 |
| SR-064 | SR-099;SR-100;SR-101 |
| SR-066 | SR-102;SR-103;SR-104;SR-105;SR-106;SR-107;SR-108 |

## SN coverage and non-spine reference migration

Every child inherits its parent's complete SN set, so the migration removes no
SN→SR edge. After the split the affected need coverage is:

| SN | Replacement SRs |
|---|---|
| SN-002 | SR-067..SR-069; SR-073..SR-078 |
| SN-006 | SR-079..SR-086; SR-102..SR-108 |
| SN-008 | SR-093..SR-101 |
| SN-010 | SR-070..SR-072; SR-089..SR-092 |
| SN-012 | SR-067..SR-069; SR-087..SR-088 |
| SN-016 | SR-079..SR-083 |
| SN-017 | SR-099..SR-101 |
| SN-021 | SR-070..SR-072; SR-089..SR-092 |
| SN-023 | SR-073..SR-078; SR-087..SR-088 |
| SN-024 | SR-084..SR-086; SR-102..SR-108 |
| SN-025 | SR-093..SR-101 |

Stage 3 must also update active semantic back-links. Historical review, plan,
and archived evidence may retain the old ID because the old row resolves to its
children; generated OKF/report/dashboard artifacts are regenerated, not edited.
The current interface rows map as follows:

| Interface | Replacement SR-Refs for the affected part |
|---|---|
| IF-009 | SR-067;SR-068;SR-074 |
| IF-011 | SR-072 |
| IF-023 | SR-067;SR-068;SR-074;SR-077 |
| IF-024 | SR-070;SR-071 |
| IF-025 | SR-075 |
| IF-040 | SR-072 |
| IF-044 | SR-079;SR-082;SR-083 |
| IF-045 | SR-079 |
| IF-046;IF-047 | SR-081 |
| IF-053;IF-054 | SR-093;SR-094;SR-095 |
| IF-056 | SR-071;SR-074;SR-075;SR-076 |
| IF-057 | SR-078 |
| IF-058 | SR-102 |
| IF-059 | SR-103 |
| IF-060 | SR-104 |
| IF-061 | SR-105 |
| IF-066 | SR-106 |

`docs/architecture.md`, live specs, source `Implements:`/`Contracts:` comments,
and README references must be changed to the narrow replacement IDs they
actually describe. The only currently open WI with an affected `SR-Refs` cell
is deferred WI-065; stage 3 must explicitly re-affirm it against SR-074 and
update its SpecRef prose in the same change. Done/historical WI rows are not
rewritten; their old IDs remain resolvable through the supersession rows.

## Stage-3 transaction and dry-run proof

Baseline commands on the stated base both exit zero:

```text
trace.py --strict-integrity
SN=25 SR=66 LLR=76 TC=76 orphans=0 integrity=0

trace.py --strict --no-placeholders --strict-schema --require-verified
SN=25 SR=66 LLR=76 TC=76 orphans=0 integrity=0 status-findings=0
placeholders=0 schema-findings=0
```

The ratified execution order is:

1. Add and test optional `SupersededBy` integrity validation.
2. Add 42 replacement SRs (`SR-067..SR-108`) as `Planned`; convert the eleven
   parents to short Inspection supersession rows; reparent/narrow the 23
   existing LLRs and 20 existing TCs; add LLR-077..LLR-096, TC-077..TC-099,
   and all live back-link changes. Regenerate the derived gate and report the
   expected G3→G2 regression rather than masking it.
3. Run strict trace at G2. The expected registry totals are SR=108, LLR=96,
   TC=99, with zero orphan/integrity/schema findings. The eleven old SRs are
   traceable through TC-099; every replacement SR has at least one LLR and TC.
4. Run the existing evidence by its narrowed TC rows, then the full unfiltered
   suite and complete G3 harness. Only after those pass, set all replacement
   SR/LLR/TC rows to `Verified`, regenerate `docs/gate`, OKF, architecture map,
   trajectory/dashboard, iteration index, and trace report, and verify strict
   trace again with the same zero-finding totals.
5. Record the before sizes above and the computed after size for every old and
   replacement SR in the integration log. Clear WI-065's staleness warning by
   the explicit SR-074 re-affirmation. Do not hand-edit generated artifacts.

This ordering is join-safe: old IDs never disappear; every moved LLR/TC points
to a replacement created in the same registry transaction; every replacement
inherits an existing SN; Inspection exempts only the old link rows from LLRs,
not from TC evidence; and no Verified claim is made while the derived gate is
temporarily G2.

## Owner attestation hard stop

The owner must review the exact ID/evidence map above and record one of these
outcomes in an owner-controlled integration action:

- **ATTEST:** approve this exact plan for stage 3; or
- **REVISE:** name the old SR, replacement ID, or evidence mapping to change.

Required attestation record: named owner, date, decision, and the commit hash of
this page. Until that record exists, WI-229 is blocked at stage 2. Autonomous
gate policy does not waive this stop, and no build session may write the new SR,
LLR, or TC rows.

## Attestation record

- **Owner:** Peter Johnson
- **Date:** 2026-07-19
- **Decision:** **ATTEST** — this exact plan (census, supersession model,
  frozen split and evidence map, SN/interface migration, stage-3 transaction
  order) is approved for stage 3 with no revisions. Ruled by the owner in a
  live session after reviewing the full page ("Sufficient, ATTEST"); the
  transcription is recorded in the development branch's `docs/log.md`
  Decisions (2026-07-19 entry).
- **Page commit:** `9fed833f35139b69a519b75e978e6232209e2e8d`
  (`WI-229: freeze the oversized-SR migration plan`); the page content is
  unchanged between that commit and this record.
