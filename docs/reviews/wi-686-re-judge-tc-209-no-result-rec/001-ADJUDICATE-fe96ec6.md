# ADJUDICATE — WI-686 — re-judge TC-209 at fe96ec69

Independent re-judge of the observation case TC-209 (verifies SR-184,
`Verification=Inspection`, no result on record). Adjudicator: Claude Fable 5.1,
a session that authored neither the case, the procedure, the rubric nor any
record inspected. Judged from the kit-rendered brief, by the case's Method
against its Expected, on the tree at fe96ec69, reading the declared inputs
(`docs/test/inspection-procedures.md`, SR-184). The procedure's own earlier
result subsection and every other prior note about the case were not taken as
evidence; the records below were read fresh.

Procedure followed: `inspection-procedures.md#critique-acceptance-provenance-inspection`
— one complete Critique acceptance record read against the applicable SN/SR
intent, then the two abnormal records the same document bounds under "Bounded
abnormal inputs" (missing provenance; copied rubric).

Complete record inspected: `docs/reviews/2026-09-06-oi85-record-closure-structured-opus.md`
(the attended Critique closure of the OI-85 scoped amendment record), with
`docs/reviews/2026-09-06-oi85-record-critique-structured-opus.md` (the prior
CHANGES_REQUESTED round) read as a second, findings-bearing sample of the same
record shape. Applicable intent: SN-024 / SR-184 as the record itself names
them, checked against the SR-184 cells at fe96ec69.

- [MINOR] Fresh non-author reviewer session identified -> the closure record names its route ("Attended Critique on the human-chosen Opus5/high route"), its assigned identity (the record's own path, "which the launcher binds to a fresh invocation log"), the tracked invocation (`docs/iteration/call_1603bfd28a3d4d3c9fa678845717bdf6-20260906-160650.log`, present at fe96ec69), and states what it did not author (the record, the prompts, the PROCESS_OPTIONS text, the skill, the rubric, the prior Critique). The absent provider session id is disclosed as not supplied, not invented. Accepted.
- [MINOR] Written rubric named with its revision, and its SN/SR intent sources -> `docs/rubrics/change-review-records.md` named by content digest SHA256 `81a0de90…31f8a`; I recomputed the digest of the rubric at fe96ec69 (raw and LF-normalized) and it matches, so the revision judged is the one on the tree. Intent sources named: SN-024, SN-037, SN-012 and SR-184, SR-185, SR-186 with the adjacent approved rows. Accepted.
- [MINOR] Rubric independently derived from the SN/SR intent, not copied from the verifying TC -> the record performs and writes down a rubric-against-intent check before scoring (G1←SR-184 identity/rubric/anchor duties, G2←SR-184's TC-copy failure clause and SN-024, G3←SR-185/SN-037, G4←SR-186/SN-012, G5←SR-186's "shall require … and record"), states "the rubric is not TC-derived (no TC text exists in the brief)", and the rubric's own header at fe96ec69 declares its derivation from SN-024, SN-037 and SN-012. Accepted as independent derivation.
- [MINOR] Every verdict and finding tied to a numbered rubric-anchor id -> the closure verdict is APPROVE with zero findings and records anchor coverage G1–G5, one judgment per anchor; the prior round's four findings each open with their anchors (F1 G3/B3, F2 G5/B5 and G1/B1, F3 G4/B4, F4 G5/B5) and its basis records G1–G5 coverage too. Accepted; SR-184's "record each verdict and finding against numbered rubric-anchor ids" holds on both samples.
- [MAJOR] Abnormal record 1, missing provenance (verdict APPROVE; reviewer/session not recorded; rubric not named; no SN/SR intent basis; no anchor citations) -> four Inspection findings, one per missing fact: (i) no fresh non-author session is identifiable, so author-independence cannot be reconstructed; (ii) no rubric is named, so nothing states the bar; (iii) no SN/SR intent basis, so the bar cannot be shown to derive from the stakeholder intent; (iv) no numbered anchor, so the APPROVE is not comparable with any other round. Each is the failure SR-184's acceptance names ("a record missing its reviewer, rubric, intent basis or anchor citation" fails).
- [MAJOR] Abnormal record 2, copied rubric (reviewer `fixture-reviewer`, session `fixture-session`, APPROVE at anchor R1 against `fixture-rubric revision 1`, intent sources SN-024 and SR-184 named, rubric stated to be copied verbatim from the TC-209 method without reading or deriving from those parents) -> one Inspection finding: every provenance slot is populated and the record still fails, because SR-184's acceptance makes the derivation, not the field, the obligation ("a record whose rubric is copied from the verifying TC without independent derivation from the SN/SR intent fails"). Naming the parents while declaring they were not read is the case the clause exists for.
- [MINOR] Artifact quality stays Critique's judgment -> this inspection judged the two records' process and provenance only. I formed and record no view on the adequacy of the OI-85 amendment record the Critique approved, nor on whether its APPROVE was right; SR-184's last clause ("never the adequacy of the produced artifact") is respected by the procedure's own scope and by this sitting.

Result: the case meets its Expected on the tree at fe96ec69 — complete,
independently derived provenance was accepted; each missing field and the
TC-copied rubric produced an Inspection finding; artifact quality was left to
Critique. Recorded `pass` with
`python project-trajectory/scripts/record_observation.py --tc TC-209 --outcome pass --by "Claude Fable 5.1, WI-686"`;
the record file it wrote is committed alongside this verdict.

## Non-blocking findings (surfaced, not acted on)

1. `docs/test/inspection-procedures.md` still carries a hand-written result
   subsection per procedure (the case's `evidence` cell points at it), while
   observation results now live in `docs/test/observations/` through the one
   writer. Two homes for one result will drift; the subsection also sits inside
   the case's declared input, so refreshing it by hand stales the very record
   it reports. Left untouched here; a future change might make the subsections
   point at the observation records instead of restating them.

OUTCOME: RECORDED result=pass
