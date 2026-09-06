# Adopter vision, hats and requirement revalidation

**Status:** implementation-plan addition requested by the owner, reviewed
against `9f938edd` on 2026-09-05. This defines a workflow to ship in the kit;
it does not change an adopter's records or the live kit method in this sitting.

## 1. Outcome and scope

An adopter needs a process suited to **its own product vision**, stakeholders,
domain, operating environment and lifecycle. Copying the kit's seeded hats,
or preserving a previously customized roster during resync, does not establish
that the current roster is adequate. The kit's O1–O6, 27 needs and choice to
extend FIRST-RUN-ADOPTER are examples from this meta-repo, not inherited product
scope or a fixed number of perspectives for every adopter.

Run the review during initial adoption and when an upgrade or project change
materially affects the vision, stakeholders, domain, deployment environment,
authority, data boundaries or assurance method. Start with the affected scope.
A tooling-only upgrade can conclude “no relevant semantic change” with a short
reason; ordinary commits do not owe a fresh whole-spine derivation. Unclear
impact calls for a wider review, not an automatic rewrite.

The workflow needs no objective-reference field, new registry tier, scheduled
review daemon or new approval ladder. Use the existing vision, roster, spine,
work-intake and reviewed change records. Mechanical findings show missing or
invalid references; independent judgment assesses whether the breakdown meets
the actual stakeholder purpose.

## 2. Review sequence and concrete outputs

| Step | Question and work | Reviewable output in existing artifacts |
|---|---|---|
| Establish purpose | Read the adopter's vision, non-goals, stakeholder outcomes, system boundaries and current operating context. Identify what changed since the prior adoption/review. | Scope and impact statement; proposed vision clarification only when needed. Prose objective anchors are optional. |
| Reassess perspectives | For each relevant seeded or customized hat, test its question and failure class against that purpose. Keep, refine, combine, condition or propose retirement where justified. Derive an additional hat when a distinct important failure question has no suitable owner. | Roster proposal with reasons, applicability examples and counterexamples. No target hat count and no inference that zero attributed rows makes a hat useless. |
| Check the input route | Evaluate the proposed predicates on real need/WI contexts and inspect the resulting brief. Ensure declared tags and typed scope actually reach the composer. | A small representative applicability worksheet and actual brief evidence, including not-applicable and missing-context cases. |
| Revisit needs | Ask whether each relevant stakeholder outcome is stated in normative need/acceptance text, whether it still serves the vision and whether an important outcome is absent. | Keep/amend/new-SN/out-of-scope proposals with named stakeholder purpose and observable acceptance intent. A review discovers candidates; it does not approve or silently mint them. |
| Rederive affected SRs | Derive capabilities and failure constraints from the accepted needs, frame and applicable hats. Use a fresh derivation before comparing old implementation-shaped text where an independent check is warranted. | Candidate SR clauses and a comparison with existing SRs: matched, missing, changed, duplicated or unsupported, with reasons. Read legacy rationales before calling a row accretion. |
| Reconcile downstream work | Trace changed obligations into LLRs, TCs, interfaces, approved evidence, active/queued work and retained assets. Preserve IDs where meaning is retained and keep unresolved obligations visible. | One scoped amendment/intake package, impacted evidence/work references and required validation; no global snapshot re-seed or automatic cancellation. |
| Review and adopt | Independently review relevance, coverage and trade-offs under the adopter's existing authority. Apply approved changes through ordinary authoring/approval and migration. | Accepted roster/spine changes and recorded decisions, or a reasoned no-change result. Approval belongs to the configured human/delegated authority. |

“Fresh derivation” describes the information boundary of the validation
exercise, not a mandatory paid multi-agent round for each upgrade. Scale it
to the changed scope and declared review policy. A structural hat-coverage
record can reuse the decomposition artifact contemplated by SR-161; until
that carrier is implemented, a review worksheet must not claim its missing
mechanical coverage check has run.

## 3. Choose the right tier

| Discovered issue | Correct proposal |
|---|---|
| Existing need omits an intended stakeholder outcome in its own text | Amend the need and acceptance intent; rationale alone cannot commission child obligations. |
| A distinct stakeholder outcome has no need, fits the vision and is wanted | Propose a new SN through normal intake with the stakeholder, scope, rationale and acceptance intent. Do not squeeze it under an unrelated parent to preserve the row count. |
| A perspective exposes a necessary constraint on an existing need | Derive or amend an SR under that need; record the hat in Hat-Refs and explain its deriving rationale. Feed it back for the applicable scope review. Do not automatically mint an “edge SN” per hat. |
| Existing SR already carries the complete obligation but implementation/evidence is incomplete | Preserve the SR and repair its design/test/work coverage. Do not remint the same requirement. |
| Existing mechanism no longer earns its cost but the outcome remains wanted | Replace the design and affected evidence while preserving the promise; amend an SR only where it actually constrains the replaced choice. |
| Outcome is outside the current vision or no longer wanted | Make the scope conflict or proposed retirement explicit. A hat finding cannot widen product scope or erase an approved obligation by itself. |

For example, an analytics adopter might find that no existing charter asks
whether incomplete input data can produce a convincing but invalid result.
It may need a DATA-QUALITY perspective. If its existing trustworthiness need
already covers that outcome, derive the missing SR constraint there. If no
need asks that analysts recognize incomplete inputs before acting, propose a
stakeholder need first. Neither result is predetermined by installing this kit.

Removing or merging a hat requires checking inbound Hat-Refs and the obligations
derived through it. The obligation may still be valid under another explicit
basis. Deleting its lens is not a retirement decision about that obligation.
Changed vision meaning similarly prompts impact review, not automatic
invalidation of every child signature or automatic reuse of every old approval.

## 4. Delivery in this redesign

P0/P1 specifies and trials this workflow alongside this repo's own hat sweep.
P1A handles any necessary changed assurance contracts before enablement.
P2/P7 provides the shared context and review-record support; the conceptual
review is useful before those changes land. P10 ships the adoption/upgrade
guidance and validates it against populated adopter examples.

State the method once in the shipped authoring guidance and link it from
ADOPTING and the resync procedure. Preserve the existing single-source skill
fan-out and adopter-owned roster/registry behavior. Kit upgrades propose relevant
new or changed hat questions for comparison; they do not overwrite customized
charters or infer that preserving the file means the review is complete.
No new review form, registry field or hard coverage gate is implied here.

Acceptance for that delivery:

- A new non-Python adopter with a different vision chooses its own relevant
  roster and needs without inheriting the kit's six objective clauses.
- An existing adopter keeps its custom hat and filled registries while an
  upgrade reveals a missing domain question and a genuine missing SN candidate.
- A separate example needs only a hat-derived SR amendment, and one needs only
  implementation repair; neither produces an unnecessary SN.
- A removed/combined hat leaves no unexplained dangling attribution or silently
  retired obligation. A meaningful SR change identifies its affected design,
  tests, interfaces and queued/active work.
- A small upgrade with no semantic impact records that conclusion without a
  whole-spine rewrite. Another with a changed vision reviews the impacted set.
- The selected hats appear in the actual brief. A syntactically valid roster
  with an unreachable relevant predicate is recognized as a review failure.
- Rejected proposals leave existing authoritative content intact; accepted
  amendments retain their ordinary review/evidence and approval semantics.

Fixtures verify structure, reference integrity and preservation. An independent
review evaluates the hat choice, need relevance and adequacy of the rederived
SRs. Passing one does not claim the other.
