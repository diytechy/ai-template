# Vision objectives: stable anchors above stakeholder needs

**Status:** proposed design for the next cross-check, 2026-09-05. Source:
`fa17b85f`. This document does not amend the live vision, needs, approval
baseline, or registry schema. Its sample text becomes canonical only if moved
into the root README through the normal reviewed change.

**Disposition after the [third Fable review](FABLE-REVIEW-3-CROSSCHECK.md#3-findings) (2026-09-05, finding O1):** adopt the smaller alternative this document names in §4 — the six clauses as headed prose in the root README's vision section with plain anchors, no `objective_refs` field, no carrier, parser, approval-classification or migration work, and no P1b/P9b slices. The mapping in §3 is kept here as a review worksheet. A carrier field is reconsidered only if, after P9's consolidation, a reviewer still cannot navigate from purpose to need. The redesign's thesis is fewer tiers describing the kit to itself; a sixth tier is not added while P9 removes rows.

## 1. Recommendation and boundary

Add short, stable objective keys `(O1)`, `(O2)`, etc. to the existing vision.
They make the question “which part of the vision does this need serve?”
answerable without inventing another normative registry. A need must still
state a recognizable stakeholder outcome and its own acceptance intent.

```text
Vision, containing named objectives
             │ objective references explain purpose
             ▼
       SN → SR → LLR → TC
          existing verified spine
```

An objective is a direction and scope anchor. An SN is a stakeholder's
observable need. An SR states a testable delivered capability; an LLR selects
a design; a TC names verification. An O-to-SN link establishes relevance,
not proof that the objective is satisfied or that the breakdown is complete.

Do not add objective Status, priority, tests, approval ledgers, a new gate,
or an objective-completion percentage. Reuse the existing vision consistency
review. Scope and priority remain properties of the needs and owner decisions;
an objective does not make its linked optional capabilities mandatory.

## 2. Proposed text inside the existing vision

Keep the current opening purpose paragraph and its single vision tag. Add
the following clauses immediately after it, before the rest of the README.
Each key has an explicit HTML anchor, such as `<a id="objective-o1"></a>`;
do not depend on a heading renderer's punctuation rules for stable links.

| Key | Proposed objective clause | Evidence of progress, read from needs and operating results |
|---|---|---|
| O1 | **Maintainable over time.** Keep code, analytics and their development process understandable and economical to change while preserving required behavior. | A reader can explain the changed responsibility; ordinary changes require less repair, duplicated description and operator intervention. |
| O2 | **Traceable and explainable.** Connect stakeholder purpose to requirements, design choices, implementation and verification so a reviewer can understand both what exists and why. | Trace integrity holds; important design and boundary decisions have an accessible rationale and supporting evidence. |
| O3 | **Trustworthy evidence.** Build test-first and report verification honestly, including failures, limitations and protection against publishing secrets or private information. | Required checks exercise the promised behavior; reports distinguish planned, run, passed, failed and unavailable evidence. |
| O4 | **Explicit authority.** Advance through clear approval boundaries, keeping human decisions and delegated decisions visible and preventing automation from granting itself additional authority. | Changed normative content receives its applicable approval; holds and policy changes are honored during execution and recovery. |
| O5 | **A shared, usable way of working.** Let humans and different AI agents understand, coordinate and resume work from the same project record, with bounded self-direction where enabled. | People can find the next action and owed decisions; enabled automation makes useful progress and resumes without manual state repair. |
| O6 | **Reusable and proportionate.** Make adoption and upgrade practical across stacks and supported platforms, preserve project-owned content, and keep optional capabilities cheap to omit. | A representative adopter can install and upgrade; the manual core runs independently of the managed loop and advanced surfaces. |

The right column is review guidance, not a second acceptance specification.
Thresholds and mandatory behaviors belong in existing SN/SR acceptance and
the [measurement contract](EXECUTION-DETAILS.md#6-measurement-and-stopgo).

O1/O2/O3/O4 directly unpack the opening vision. O5/O6 also make explicit
commitments already present in the surrounding README and approved needs:
self-direction, portability, bounded operation and proportionality. This is
a proposed scope clarification, not a claim that all six clauses are a
verbatim reformat of the opening paragraph. Review their meaning before use.

Claude's five promises remain a useful comparison: Traced maps chiefly to O2;
Gated to O3/O4; Adoptable to O6; Self-directing to O5/O4; Legible to O1/O2/O5.
They are comparison labels, not a second set of live objective identifiers.

## 3. Proposed mapping of every current need

This is a purpose mapping, not a retirement or approval decision. Need text
and acceptance remain in [the live registry](../requirements/stakeholder-needs.toml).
The mapping was drafted by reading all 27 current needs and acceptance cells
at `fa17b85f`; adequacy still needs the independent cross-check.

| Need | Proposed objective refs | Distinct contribution retained |
|---|---|---|
| SN-001 | O6 | Working adoption and upgrades that preserve adopter content |
| SN-002 | O2, O3 | Mechanically verified traceability |
| SN-003 | O6 | Stack-independent configuration and adoption |
| SN-004 | O4, O3 | Explicit gates with enforced required checks |
| SN-005 | O5, O3 | One agent-neutral working and enforcement contract |
| SN-006 | O5, O4 | Bounded unattended operation and clear recovery/failure behavior |
| SN-007 | O1, O3 | The kit verifies itself through changes |
| SN-008 | O3 | Honest pass verdicts and explicit missing evidence |
| SN-009 | O3 | Secrets and enabled identity/privacy protection |
| SN-010 | O2, O5 | Navigable documentation and current generated views |
| SN-011 | O6 | Argued dependencies and supported-platform operation |
| SN-012 | O1, O6 | Proportionate granularity and optional capabilities |
| SN-023 | O2, O5 | Visible progress and system connections |
| SN-024 | O3 | Independent, rubric-grounded subjective verification |
| SN-025 | O5 | Next work derived from tracked state |
| SN-026 | O5, O3 | Configurable models and independent perspectives |
| SN-027 | O5, O4 | Bounded parallel work and controlled serial integration |
| SN-028 | O4, O5 | One discoverable and unambiguous policy home |
| SN-029 | O4, O5 | Honest autonomous advancement under current authority |
| SN-033 | O2, O5 | Needs recognizable to stakeholders |
| SN-034 | O6, O5 | Accessible setup and resume entry points across platforms |
| SN-035 | O5 | A discoverable actions menu within its declared scope |
| SN-036 | O2, O3 | Relevant perspectives and failure cases considered in decomposition |
| SN-037 | O2 | Requirements and architecture grounded in system boundaries |
| SN-038 | O2, O6 | Every supplied file's purpose is explainable |
| SN-039 | O6 | Applicability of each need is explicit |
| SN-040 | O2 | Reproducible, reviewable component-partition rationale |

Do not force a questionable need under O1 or O5 because those are broad.
For each link, a reviewer should finish “without this need, this objective
would be frustrated because …” with a specific consequence. If no link fits,
record either a missing objective or disputed product scope. Neither finding
automatically authorizes a new objective or deletion of the need.

## 4. References and one source of truth

**Recommended carrier:** one optional `objective_refs` array on an SN, using
unqualified keys within that project's vision, for example:

```toml
# Proposed additional field on an existing need, not a live schema today.
objective_refs = ["O1", "O6"]
```

The displayed links are derived as `README.md#objective-o1`, etc. The keys
are not additional SN tags, citation prose in `why`, or copied objective text.
The root vision owns objective wording; the SN owns its forward references;
reverse lists are generated. No objective-to-SN table is hand-maintained
after migration: this document's table becomes historical review evidence.

Rules for the optional feature:

- A project without anchored objectives remains valid. An existing adopter
  does not acquire a missing-field failure after a kit upgrade.
- If a row supplies the field, parse a nonempty list of distinct known keys.
  Report wrong types, duplicates and unresolved references through the
  existing registry/doc validation boundary. Do not write another parser.
- For a project adopting the convention, omitted mappings are a review
  worklist initially. Requiring coverage is a later explicit scope decision,
  not a new global gate hidden inside bootstrap.
- Preserve the singleton vision tag; numbered clauses live inside that
  one home. SR/LLR/TC inherit purpose through SN links and receive no new
  objective fields.
- Stable keys survive wording clarification. Splits/merges use new keys and
  update inbound references in the same reviewed change; retired keys are
  never reassigned. Git history records old meanings, without a new watermark
  or lifecycle registry.
- A reference-only edit does not amend need wording. Review it for semantic
  correctness, classify it explicitly with existing traced fields, and verify
  that an inaccurate relink cannot silently rewrite normative acceptance.
- An objective meaning change receives the existing owner vision/scope review
  with the linked needs shown as an impact set. Reassess those needs; amend
  their normative text where needed through ordinary approval. Do not silently
  invalidate every child signature or infer that none is affected.

The first implementation must add the optional field to the kit template,
carrier/schema, approval-field classification, trace output, documentation and
dogfood fixture together. Inspect `spine_carrier.py`, `kitlib/spine.py`,
`acceptance_record.py`, `check_docs.py` and the existing trace tests before
choosing exact helper placement. This is a small extension of existing readers,
not a new Objective service. If that extension costs more than it clarifies,
the supported smaller alternative is vision anchors plus manual links in the
existing review brief, with no schema change.

## 5. Implementation slice and acceptance

P0 prepares the wording/mapping for review; this is independently useful even
if no runner is replaced. P1A includes any necessary assurance-contract
amendment. P9 can ship the optional reference carrier without waiting for a
runner rewrite, after the objective decision and its own prerequisites.

1. Review six clauses against the existing vision, all needs and non-goals.
2. Agree the carrier choice: recommended optional SN field, or prose-only
   links. Do not build both as independent authorities.
3. Add the vision anchors and the selected linking support in one bounded
   slice, including the downstream migration recipe and existing-reader tests.
4. Exercise a legacy adopter without objectives, a new adopter with its own
   objectives, a dangling link, duplicate key, changed objective meaning, and
   a reference-only edit. The first two stay usable; the latter cases produce
   the declared review/integrity result without changing the stage ladder.
5. Show a reviewer navigating objective → need → requirement → test evidence
   and identifying one deliberately misplaced need. A table with every row
   filled is not enough to prove the links explain the decomposition.

Adopters author their own objective text and keys. Bootstrap must not copy
this kit's six product objectives into an unrelated downstream project's
vision. Example identifiers are documentation, not inherited obligations.
