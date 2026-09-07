# Inspection procedures

These are the durable procedures for the three drafted decomposition
inspections, one section per subject. Each result subsection stays explicit
until a reviewer records the person, date, and result. Results below distinguish
completed document inspections from an incomplete positive sample; none is an
artifact approval or a machine-coverage result.

## Critique acceptance provenance inspection

Read one complete Critique acceptance record against the applicable SN/SR
intent. Confirm the fresh non-author reviewer session, the written rubric and
its intent sources, and a numbered rubric-anchor id for every verdict and
finding. Then read an abnormal record with one or more of reviewer, rubric,
intent basis, or anchor citation missing. Record each missing field as an
Inspection finding, including a rubric copied from the verifying TC without
independent derivation from the SN/SR intent. This procedure checks process and
provenance; it does not make the Critique judgment about artifact quality.

### Critique acceptance provenance inspection result

**PASS — 2026-09-06, [fresh Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** The inspector read the actual
[Critique closure](../reviews/2026-09-06-oi85-record-closure-structured-opus.md)
and its linked invocation. It identified fresh non-author review identity,
rubric revision/intent sources and coverage of all five numbered anchors. It reported all four
missing facts in the abnormal record and rejected the fully populated
TC-copied rubric. This establishes record process/provenance; artifact quality
and Drafted-row approval remain separate.

## Requirement and interface counterpart review inspection

Read one reviewed change record where a requirement or interface side changed.
Confirm that it names the changed side and affected counterpart, carries the
corresponding change or an explicit justification for retaining it, and records
an independent semantic decision. Then inspect an abnormal record in which all
ids, endpoints, and references resolve but the counterpart meaning is absent.
Record a finding. A reference-existence result alone cannot discharge this
procedure.

### Requirement and interface counterpart review inspection result

**PASS — 2026-09-06, [fresh Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** The inspector read the actual
[scoped H3 record](../ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md#implementation-review-subject-2026-09-06),
IF-011/IF-164, LLR-035/LLR-198 and SR-168/SR-070. It identified the retained
counterparts and the independent counterpart semantic judgment, and rejected the
reference-only counterexample. The separate
[P9R source review](../reviews/2026-09-06-oi85-p9r-selector-structured-opus.md)
checks facade compatibility against source; the document inspector did not
execute that source.

## Decomposition proportionality inspection

Read one actual completed decomposition review record, the declared hats roster,
and the decomposition brief used by that review. Resolve the applicable hats,
confirm that the brief presents every applicable hat's question and that the
review record names each hat's outcome. Confirm the required spine remains the
scope boundary, then inspect the complete reviewed chain and a small chain
containing a child that only paraphrases or duplicates a parent's decision or
verification. A missing applicable-hat outcome or a child within a required tier
with no independent decision or verification purpose is an Inspection finding.
Record why further splitting stops at the independent-value boundary. This
procedure uses the existing brief and review record and does not impose a
row-count threshold, extra depth, new record carrier, or machine coverage check.

### Decomposition proportionality inspection result

**PASS — 2026-09-06, [fresh Opus 5/high Inspection](../reviews/2026-09-06-sn036-inspection-structured-opus.md).** The independent inspector re-derived the
applicable set from the roster and exact parent/work context, confirmed every
applicable question in the [actual brief](../reviews/2026-09-06-sn036-decomposition-brief.md),
and read a reasoned outcome for each in the [completed review](../reviews/2026-09-06-sn036-closure-structured-opus.md).
It checked the chain's distinct child purposes, the permitted direct Inspection
tiers and the stated stopping reason. It rejected the missing TEST-ENGINEER
outcome and the paraphrasing-child cases. This is document Inspection evidence;
it does not approve artifact text or claim software-test execution.

The inspector separately requested corrections to the review's transcribed
rubric digest, the preflight and the adjudication ledger. The
[disposition record](../reviews/2026-09-06-sn036-review-dispositions.md) records
those corrections; the original verdict bodies and historical result remain.
The extra negative brief-question example is a queued future improvement, not
an execution claimed here.

**Historical INCOMPLETE — 2026-09-06, [earlier Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** That inspector accepted the
independent purposes of SR-184/SR-185/SR-186 and their direct Inspection cases,
read the stopping reason, and rejected the paraphrasing child. The procedure
then required a machine-produced SR-161 perspective record that did not exist,
as LLR-183 then stated. The later [owner ruling](../log.d/2026-09-06-sn036-owner-ruling.md)
replaced that obligation with the existing hat-by-hat review path; this sitting
amended LLR-183 accordingly. The earlier result remains incomplete for the
procedure it actually executed. A new Inspection of the revised procedure is
recorded separately; the ruling itself supplies no test result.

## Bounded abnormal inspection inputs

These are synthetic counterexamples for the procedures above. They do not amend
live requirements or impersonate actual reviews. The positive subjects are the
real scoped amendment record and its independently logged Critique; the
inspector must identify the exact versions it reads.

- **Missing provenance:** verdict `APPROVE`; reviewer/session not recorded;
  rubric not named; no SN/SR intent basis; no numbered anchor citations.
  This one abnormal record deliberately omits all four required facts.
- **Copied rubric:** a synthetic reviewer `fixture-reviewer`, session
  `fixture-session`, records `APPROVE` at anchor `R1` against synthetic rubric
  `fixture-rubric revision 1`. The record names SN-024 and SR-184 as intent
  sources, but states that the rubric was copied verbatim from the verifying
  TC-209 method without reading or independently deriving from those parents.
  Every provenance slot is populated; the declared derivation is still invalid.
- **Reference-only counterpart:** a synthetic change says IF-011's stale
  result is now exit 2, while LLR-035/SR-168/SR-070 and callers retain the
  existing behavior. Its review says only that all named IDs and endpoints
  resolve and therefore the change passes. It records neither a corresponding
  behavioral change nor a reason why retaining it preserves meaning.
- **Missing perspective outcome:** the actual completed review record with its
  TEST-ENGINEER outcome omitted, while the applicable-hat brief and all other
  outcomes remain. The Inspection must identify that omitted applicable hat.
- **Paraphrasing child:** the actual SR-186→TC-211 chain gains an unminted
  candidate child saying “the process shall keep decomposition proportionate,”
  verified by the same Inspection judgment without another decision or case.
  Its only stated purpose is to make the chain look more detailed. This adds
  no independent decision or verification purpose within a required tier.

The historical incomplete result records what that earlier inspection examined.
The later TC-211 execution above inspected the actual completed review record
and recorded its own reviewer, date, subject and findings; the owner ruling
itself supplied no Inspection result.
