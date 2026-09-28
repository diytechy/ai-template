# ADJUDICATE — WI-700 — re-judge TC-210 at 8bebd4cf

Independent re-judge of the observation case TC-210 (verifies SR-185,
`Verification=Inspection`), due because its declared inputs changed after its
last result. Adjudicator: Claude Fable 5.1, a session that authored neither the
case, the procedure, the change record inspected nor the earlier verdict.
Judged from the kit-rendered brief, by the case's Method against its Expected,
on the tree at 8bebd4cf, reading the declared inputs
(`docs/test/inspection-procedures.md`, SR-185) as they now stand. The earlier
result (`TC-210.2026-09-28T071102Z.toml`, WI-687) and the procedure's own
hand-written result subsection were not taken as evidence; the WI-687 verdict
was opened only to see which record it had inspected, and the record and every
registry cell below were re-read fresh at HEAD.

## What changed in the declared inputs since the last result

Verified with `git diff fe96ec69 8bebd4cf -- <path>` and a field-level TOML
diff of the SR row:

- `docs/test/inspection-procedures.md`: the intro now counts "one sampled
  assumption inspection", and a new section "Sampled new-reader inspection"
  (the TC-279 / DA-011 procedure) was inserted before the bounded abnormal
  inputs. The requirement and interface counterpart review procedure and its
  "Reference-only counterpart" abnormal input are byte-identical to fe96ec69.
- SR-185: gained a `coincident` cell ("The need asks for an architecture that
  changes with the promises it serves; the change record naming the affected
  counterpart, with the change or its justification, is that outcome, judged
  by review."). `requirement`, `acceptance_criteria`, `rationale`, `sn_refs`,
  `boundary_refs`, `verification` and `status` are unchanged. The new cell
  restates the acceptance's shape (counterpart named, change or justification,
  judged by review) and introduces no new clause; it agrees with SN-037's
  "the architecture changes with those promises".

Neither change alters the Method, the Expected or the bar, so the case was
re-run in full rather than assumed still to hold.

## Procedure followed

`inspection-procedures.md#requirement-and-interface-counterpart-review-inspection`:
one reviewed change record where an interface side changed, then the abnormal
reference-existence-only record the same document bounds.

Semantic change record: the H3 paragraph of
`docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md`
"Implementation review subject (2026-09-06)" (P9R: IF-011's description
completed for its text-status mode; the rendering LLR source pointers moved),
with the independent reviewer's decision read from
`docs/reviews/2026-09-06-oi85-record-closure-structured-opus.md` G3. The
record's claims were checked against the live cells at 8bebd4cf: IF-011 and
IF-164 (`docs/requirements/interfaces.toml`), LLR-035, LLR-130 and LLR-198
(`low-level-requirements.toml`), SR-168 and SR-070
(`system-requirements.toml`), and IF-011's declared consumer.

- [MINOR] The record names the changed side -> yes: the interface side ("completes IF-011's description of its already-public text-status mode") and the LLR source pointers for the rendering implementation. Accepted.
- [MINOR] The record names the affected counterpart -> yes, at the requirement tier and not only the consumer: IF-011 → LLR-035 → SR-168 and SR-070, and the paired status surface IF-164 → LLR-198 → SR-168, each with the registry line range it read. Accepted.
- [MINOR] The record carries the corresponding change or an explicit justification for retaining the counterpart -> an explicit retention decision: "descriptive-only: the SR-168/SR-070 asserted behavior remains unchanged while the interface description records the existing status mode"; the command, its 0/1 exits and IF-164's writer are retained because "moving the private HTML implementation is not a reason to change a consumer's command". A reason a reader can test, not a citation. Accepted.
- [MINOR] The independent reviewer's semantic decision is recorded and not discharged by reference existence -> the record demands it ("The independent review must judge this semantic argument against the actual source and interface cells; a successful reference lookup is insufficient"), and the closure Critique's G3 records that it "judged that reason rather than resolving ids", naming the cell text it turned on (LLR-035's "status block via --status", LLR-130's "Implements stale/missing --check", SR-070's freshness acceptance, IF-164's owner) and a rejected MINOR it considered (LLR-130/LLR-079 not enumerated as counterparts). Accepted.
- [MINOR] Does the retention decision still hold at 8bebd4cf? (my own check of the counterpart, so the inspection does not rest on the record's say-so) -> IF-011 reads "0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --check", owner `scripts/gen_trajectory`, consumer `scripts/check`; LLR-035 (Approved, sr_refs SR-168 and SR-070) states "its status block via --status"; LLR-130 (Approved, SR-070) "Implements stale/missing --check"; SR-070's acceptance carries "a committed copy that has drifted from its sources fails its freshness contract while a current one passes"; IF-164's owner is `scripts/traj_status` and LLR-198 (Approved, SR-168) names `traj_status.py` as the shim that keeps the writer's name. The description and its requirement-side counterparts still say the same thing; the counterpart decision is explicit and true of the tree. Noted without finding: IF-011 and IF-164 remain `Drafted`, a first-approval act for another sitting, not a counterpart defect.
- [MAJOR] Abnormal record, reference-existence only (a synthetic change says IF-011's stale result is now exit 2 while LLR-035 / SR-168 / SR-070 and the callers keep the existing behavior; its review says only that every named id and endpoint resolves and therefore the change passes) -> one Inspection finding: the changed signal's MEANING moved (a stale copy exiting 2 where IF-011's consumer `scripts/check` and SR-070's freshness contract are written against 1) and the record neither carries the corresponding change at the counterpart nor records why retaining it preserves meaning. That every id resolves is the evidence SR-185's acceptance says cannot discharge the review ("not discharged by reference-existence tests"); a reference-existence result alone is insufficient.

Result: the case meets its Expected on the tree at 8bebd4cf — the counterpart
decision in the semantic change record is explicit and independently judged,
and reference-existence evidence alone was found insufficient. Recorded
`pass` with
`python project-trajectory/scripts/record_observation.py --tc TC-210 --outcome pass --by "Claude Fable 5.1, WI-700"`;
the record file it wrote is committed alongside this verdict.

## Non-blocking findings (surfaced, not acted on)

1. Coverage of SR-185 still rests on the one 2026-09-06 change record; the
   WI-655 C2 slice (bcf1e9a8) re-pointed `boundary_refs` on many SRs (B-05 →
   B-09 / B-10) and wrote each boundary interface's bridging, which is a change
   to the requirement/interface relationship at scale, yet no record in
   `docs/reviews/` frames it as a changed-side / counterpart decision in
   SR-185's shape. The reviewer prompt's counterpart clause is the place that
   should be producing such records; a future re-judge would benefit from a
   second worked sample.
2. Same as WI-687's and WI-699's finding: the re-judge was triggered by a
   sibling section added to the procedure file and an annotation cell on the
   SR, neither of which touched the procedure or the acceptance judged; and
   `inspection-procedures.md` restates a 2026-09-06 result inside the case's
   own declared input.

OUTCOME: RECORDED result=pass
