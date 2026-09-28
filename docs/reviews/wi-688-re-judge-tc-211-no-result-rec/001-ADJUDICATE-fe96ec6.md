# ADJUDICATE — WI-688 — re-judge TC-211 at fe96ec69

Independent re-judge of the observation case TC-211 (verifies SR-186,
`Verification=Inspection`, no result on record). Adjudicator: Claude Fable 5.1,
a session that authored neither the case, the procedure nor the decomposition
record inspected. Judged from the kit-rendered brief, by the case's Method
against its Expected, on the tree at fe96ec69, reading the declared inputs
(`docs/test/inspection-procedures.md`, SR-186). The procedure's own earlier
result subsection and every other prior note about the case were not taken as
evidence; the record, the registry cells and the scripts were read fresh.

Procedure followed as far as the tree allows:
`inspection-procedures.md#decomposition-proportionality-inspection` — read
the existing scoped decomposition/review record AND its applicable SR-161
applicability/no-finding record, confirm the required spine remains the scope
boundary, then inspect a small chain with a paraphrasing child (the one the
same document bounds under "Bounded abnormal inputs").

Scoped decomposition record inspected: the H5 section and the
"Implementation review subject (2026-09-06)" H5 paragraph of
`docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md`
(the SR-184 / SR-185 / SR-186 → TC-209 / TC-210 / TC-211 chain), against the
SR-186 cells at fe96ec69 and PROCESS.md's tier rule the record cites.

- [MINOR] Each additional child within a required tier carries an independent decision or verification purpose traceable to its parent -> the record names three distinct acceptance questions under three different needs (SR-184 Critique record provenance under SN-024; SR-185 counterpart agreement under SN-037; SR-186 proportionate decomposition under SN-012) and, per child TC, the verification the parent sentence does not perform (TC-209 normal / missing-provenance / TC-copied-rubric; TC-210 semantic agreement vs valid references; TC-211 a redundant child while required tiers are kept). I checked the three SR rows at fe96ec69: each is `Approved`, `Verification=Inspection`, cites the need the record says, and no two state the same obligation. Holds.
- [MINOR] The record states why further splitting stops at the independent-value boundary, keeping the required tiers -> the H5 paragraph records the stopping decision with its premise cited: an SR whose selected method is Inspection is LLR-exempt (`PROCESS.md:737-744`, which I confirmed at fe96ec69 says only Analysis / Inspection / Attest SRs are LLR-exempt and every SR still needs a TC), so a direct SR→TC link retains every tier that method requires, and "another LLR would duplicate these review judgments without defining a separate mechanism"; it adds that this is a scoped decision, not a quota. Holds; the SR-186 acceptance's second clause is met by this record.
- [MAJOR] The paraphrasing child (an unminted candidate under SR-186 → TC-211 saying "the process shall keep decomposition proportionate", verified by the same Inspection judgment, whose only stated purpose is to make the chain look more detailed) -> one Inspection finding: it restates its parent's requirement, adds no decision the parent does not already make, and its verification is the parent's own TC-211 judgment re-run, so it carries no independent decision or verification purpose within a required tier. Exactly the failure SR-186's acceptance names.
- [BLOCKER] The Method's positive sample: "the existing scoped decomposition/review record AND its applicable SR-161 applicability/no-finding record" -> the second half does not exist at fe96ec69. SR-161 (Approved, `Verification=Test`) requires a per-decomposition machine-readable perspective record that distinguishes not-applicable from considered-with-no-finding; LLR-183's own `detail` states the debt ("the no-finding half needs a per-decomposition artifact that does not exist"), `docs/status.md` lists resolving "the existing SR-161 per-decomposition perspective-record gap and complete TC-211's normal sample" as the next implementation, and the scripts hold only the `Hat-Refs` cell and the brief-side `hats.py applicable` block — a fact about a row and a fact about a brief, neither the per-decomposition no-finding record the procedure reads. The record itself says the same in its closing paragraph. So the Method cannot be executed in full on this tree: the two Expected clauses I could judge hold, but the procedure's normal sample is incomplete by the procedure's own definition, and a pass recorded on it would weaken the Method to obtain a green. No result recorded.

What is needed, and against which Expected: implement the SR-161
per-decomposition perspective-record producer (the obligation LLR-183 states
and `docs/status.md` already queues), produce that record for the scoped
SR-184/185/186 decomposition, then re-run this procedure over the complete
sample — record plus its SR-161 record — and record the result with
`python project-trajectory/scripts/record_observation.py --tc TC-211 --outcome pass|fail --by "<inspector>"`
against TC-211's Expected: a child with no independent decision or
verification purpose is an Inspection finding; otherwise the review records
that independent value and why further splitting stops. On the half of the
sample that exists today, both clauses hold and the paraphrasing child is
rejected, so the remaining question is only whether the SR-161 record, once
produced, changes that reading.

## Non-blocking findings (surfaced, not acted on)

1. TC-211's Method binds an Inspection-verified SR (SR-186) to a record
   another SR's chain (SR-161, `Verification=Test`, LLR-183) has not
   delivered, so the case is unpassable until that implementation lands
   regardless of how well SR-186's own record is written. Either the producer
   ships (the queued work) or the Method's dependence on the SR-161 record is
   re-attested as a separate clause — a decision for the tier authority, not
   this sitting.
2. Same as WI-686's finding: `inspection-procedures.md` restates a result
   the observation records now hold, inside the case's own declared input.

OUTCOME: NEEDS-JUDGEMENT result=-
