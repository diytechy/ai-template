# ADJUDICATE — WI-687 — re-judge TC-210 at fe96ec69

Independent re-judge of the observation case TC-210 (verifies SR-185,
`Verification=Inspection`, no result on record). Adjudicator: Claude Fable 5.1,
a session that authored neither the case, the procedure nor the change record
inspected. Judged from the kit-rendered brief, by the case's Method against its
Expected, on the tree at fe96ec69, reading the declared inputs
(`docs/test/inspection-procedures.md`, SR-185). The procedure's own earlier
result subsection and every other prior note about the case were not taken as
evidence; the record and the registry cells were read fresh.

Procedure followed: `inspection-procedures.md#requirement-and-interface-counterpart-review-inspection`
— one reviewed change record where an interface side changed, then the
abnormal reference-existence-only record the same document bounds under
"Bounded abnormal inputs".

Semantic change record inspected: the H3 paragraph of
`docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md`
"Implementation review subject (2026-09-06)" (the P9R change that completed
IF-011's description of its text-status mode and moved the rendering LLR
source pointers), with the independent reviewer's decision on it read from
`docs/reviews/2026-09-06-oi85-record-closure-structured-opus.md` G3. The
record's claims were checked against the live cells at fe96ec69: IF-011,
IF-164 (`docs/requirements/interfaces.toml`), LLR-035, LLR-198
(`low-level-requirements.toml`), SR-168, SR-070 (`system-requirements.toml`).

- [MINOR] The record names the changed side -> yes: the interface side, "completes IF-011's description of its already-public text-status mode", plus the LLR source pointers for the rendering implementation. Accepted.
- [MINOR] The record names the affected counterpart -> yes, at the requirement tier and not only the consumer: IF-011 → LLR-035 → SR-168 and SR-070, and the paired status surface IF-164 → LLR-198 → SR-168, each with the registry line range it read. Accepted.
- [MINOR] The record carries the corresponding change or an explicit justification for retaining the counterpart -> an explicit retention decision: "descriptive-only: the SR-168/SR-070 asserted behavior remains unchanged while the interface description records the existing status mode"; the command, its 0/1 exits and IF-164's writer are retained because "moving the private HTML implementation is not a reason to change a consumer's command". Accepted as a justification a reader can test, not a citation.
- [MINOR] The independent reviewer's semantic decision is recorded and not discharged by reference existence -> the record itself demands it ("The independent review must judge this semantic argument against the actual source and interface cells; a successful reference lookup is insufficient"), and the closure Critique's G3 records that judgment: the reason was judged against the cells rather than by resolving ids, with the specific cell text it turned on (LLR-035's "status block via --status", SR-070's freshness acceptance, IF-164's owner). Accepted.
- [MINOR] Does the retention decision still hold at fe96ec69? (my own check of the counterpart, so the inspection does not rest on the record's say-so) -> IF-011's data cell reads "0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --check"; LLR-035 (Approved) states "its status block via --status"; SR-070's acceptance carries the freshness contract that fails on drift; IF-164's owner is `scripts/traj_status` and LLR-198 (Approved) names `traj_status.py` as the shim that keeps the writer's name. The description and its requirement-side counterparts say the same thing today; the counterpart decision is explicit and true of the tree. Noted without finding: IF-011 and IF-164 are `Drafted` at fe96ec69, so the interface-side text is not yet approved text — a first-approval act for another sitting, not a counterpart defect.
- [MAJOR] Abnormal record, reference-existence only (a synthetic change says IF-011's stale result is now exit 2 while LLR-035 / SR-168 / SR-070 and the callers keep the existing behavior; its review says only that every named id and endpoint resolves and therefore the change passes) -> one Inspection finding: the changed signal's MEANING moved (a stale copy now exits 2 where IF-011's consumer `scripts/check` and SR-070's freshness contract are written against 1) and the record neither carries the corresponding change at the counterpart nor records why retaining the counterpart preserves meaning. That every id resolves is exactly the evidence SR-185's acceptance says cannot discharge the review ("not discharged by reference-existence tests"); a reference-existence result alone is insufficient.

Result: the case meets its Expected on the tree at fe96ec69 — the counterpart
decision in the semantic change record is explicit and independently judged,
and reference-existence evidence alone was found insufficient. Recorded
`pass` with
`python project-trajectory/scripts/record_observation.py --tc TC-210 --outcome pass --by "Claude Fable 5.1, WI-687"`;
the record file it wrote is committed alongside this verdict.

## Non-blocking findings (surfaced, not acted on)

1. The one semantic change record the procedure can point at is the
   2026-09-06 amendment record; no later change record on the tree records a
   changed-side / counterpart decision in this shape (the WI-676 verdict names
   IF-194 / IF-197 as the seams TC-242 exercises but does not frame a
   counterpart decision). Coverage of SR-185 therefore rests on one worked
   record; a future re-judge would benefit from a second, and the reviewer
   prompt's counterpart clause is the place that should be producing them.
2. Same as WI-686's finding: `inspection-procedures.md` restates a result the
   observation records now hold, inside the case's own declared input.

OUTCOME: RECORDED result=pass
