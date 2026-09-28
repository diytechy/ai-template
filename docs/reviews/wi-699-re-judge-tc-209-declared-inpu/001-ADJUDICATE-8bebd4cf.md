# ADJUDICATE — WI-699 — re-judge TC-209 at 8bebd4cf

Independent re-judge of the observation case TC-209 (verifies SR-184,
`Verification=Inspection`), due because its declared inputs changed after its
last result. Adjudicator: Claude Fable 5.1, a session that authored neither the
case, the procedure, the rubric, the records inspected nor the earlier
verdict. Judged from the kit-rendered brief, by the case's Method against its
Expected, on the tree at 8bebd4cf, reading the declared inputs
(`docs/test/inspection-procedures.md`, SR-184) as they now stand. The earlier
result (`TC-209.2026-09-28T070936Z.toml`, WI-686) and the procedure's own
hand-written result subsection were not taken as evidence; the WI-686 verdict
was opened only to see which records it had inspected, and every record below
was re-read fresh at HEAD.

## What changed in the declared inputs since the last result

Verified with `git diff fe96ec69 8bebd4cf -- <path>` and a field-level TOML
diff of the SR row:

- `docs/test/inspection-procedures.md`: the intro now counts "one sampled
  assumption inspection", and a new section "Sampled new-reader inspection"
  (the TC-279 / DA-011 procedure, result "NOT YET TAKEN") was inserted between
  the proportionality procedure and the bounded abnormal inputs. The Critique
  acceptance provenance procedure, its abnormal inputs (missing provenance;
  copied rubric) and the scoping sentence "This procedure checks process and
  provenance; it does not make the Critique judgment about artifact quality"
  are byte-identical to fe96ec69.
- SR-184: gained `da_refs = ["DA-007"]` (the design assumption that a
  non-author, where configured cross-family, reviewer finds defects the author
  was blind to). `requirement`, `acceptance_criteria`, `rationale`, `sn_refs`,
  `boundary_refs`, `verification` and `status` are unchanged.

Neither change alters the Method, the Expected or the bar the acceptance
states, so the case was re-run in full rather than assumed still to hold.

## Procedure followed

`inspection-procedures.md#critique-acceptance-provenance-inspection`: one
complete Critique acceptance record read against the applicable SN/SR intent,
then the two abnormal records the same document bounds under "Bounded abnormal
inputs for the OI-85 inspection".

Complete record: `docs/reviews/2026-09-06-oi85-record-closure-structured-opus.md`
(the attended Critique closure of the OI-85 scoped amendment record), with the
prior CHANGES_REQUESTED round
`docs/reviews/2026-09-06-oi85-record-critique-structured-opus.md` read as a
second, findings-bearing sample of the same record shape. Applicable intent:
SN-024 (Approved) and SR-184 (Approved), read from the registries at HEAD.

- [MINOR] Fresh non-author reviewer session identified -> the closure record states its route ("Attended Critique on the human-chosen Opus5/high route"), its assigned identity (the record's own path, bound by the launcher to a fresh invocation log), the tracked invocation `docs/iteration/call_1603bfd28a3d4d3c9fa678845717bdf6-20260906-160650.log` (present at HEAD), and what it did not author (the record, the prompts, the PROCESS_OPTIONS text, the skill, the rubric, the prior Critique). The absent provider session id is stated as not supplied, never invented. The reviewed record itself is the Codex-authored amendment document, so the reviewer is a non-author by session and by family. Accepted.
- [MINOR] Written rubric named with its revision, and its SN/SR intent sources -> `docs/rubrics/change-review-records.md` is named by content digest SHA256 `81a0de90…31f8a`; I recomputed the digest of that file at 8bebd4cf (raw and LF-normalized) and both equal `81a0de90c98ad2dac0b9774fd94c611181fc49bfde083cc22c52d1fb1ac31f8a`, so the revision judged is the one on the tree. Intent sources named: SN-024, SN-037, SN-012 and SR-184, SR-185, SR-186, with SR-154, SR-162, SR-070, SR-168, SR-170 read as adjacent Approved homes. Accepted.
- [MINOR] Rubric independently derived from the SN/SR intent, not copied from the verifying TC -> the record performs and writes down a rubric-against-intent check before scoring (G1←SR-184 identity/rubric/anchor duties, G2←SR-184's TC-copy failure clause and SN-024, G3←SR-185/SN-037, G4←SR-186/SN-012, G5←SR-186's "shall require … and record"), tests two permissiveness risks, and states "the rubric is not TC-derived (no TC text exists in the brief)"; the rubric's own header at HEAD declares its derivation from SN-024, SN-037 and SN-012. Accepted as independent derivation.
- [MINOR] Every verdict and finding tied to a numbered rubric-anchor id -> the closure verdict is APPROVE with zero findings and records anchor-by-anchor judgment G1–G5 ("coverage recorded because the verdict has zero findings"); the prior round's four findings each open with their anchor pair (F1 G3/B3, F2 G5/B5 and G1/B1, F3 G4/B4, F4 G5/B5). SR-184's "record each verdict and finding against numbered rubric-anchor ids" holds on both samples. Accepted.
- [MAJOR] Abnormal record 1, missing provenance (verdict APPROVE; reviewer/session not recorded; rubric not named; no SN/SR intent basis; no numbered anchor citations) -> four Inspection findings, one per missing fact: (i) no fresh non-author session is identifiable, so author-independence cannot be reconstructed; (ii) no rubric is named, so nothing states the bar; (iii) no SN/SR intent basis, so the bar cannot be shown to derive from stakeholder intent; (iv) no numbered anchor, so the APPROVE is comparable with nothing. Each is a failure SR-184's acceptance names ("a record missing its reviewer, rubric, intent basis or anchor citation" fails).
- [MAJOR] Abnormal record 2, copied rubric (`fixture-reviewer` / `fixture-session`, APPROVE at anchor `R1` against `fixture-rubric revision 1`, intent sources SN-024 and SR-184 named, rubric declared copied verbatim from the TC-209 method without reading or deriving from those parents) -> one Inspection finding: every provenance slot is populated and the record still fails, because SR-184's acceptance makes the derivation, not the field, the obligation ("a record whose rubric is copied from the verifying TC without independent derivation from the SN/SR intent fails"). Naming the parents while declaring they were not read is exactly the case the clause exists for.
- [MINOR] Artifact quality stays Critique's judgment -> this inspection judged the records' process and provenance only. I formed and record no view on the adequacy of the OI-85 amendment record the Critique approved, nor on whether its APPROVE was right; SR-184's last clause ("never the adequacy of the produced artifact") and the procedure's own scoping sentence are both respected.
- [MINOR] The new `da_refs` (DA-007) against the complete record -> DA-007's `holds_when` asks that the reviewer receive the rubric or requirement text rather than the author's self-assessment and not be of the authoring family; the closure record states it received the rubric and intent text, read the prior Critique "only as finding history, never as author self-assessment", and reviewed a Codex-authored record as Opus. The assumption is consistent with the record. It adds no acceptance clause to SR-184 and none was applied as one.

Result: the case meets its Expected on the tree at 8bebd4cf — complete,
independently derived provenance was accepted; each missing field and the
TC-copied rubric produced an Inspection finding; artifact quality was left to
Critique. Recorded `pass` with
`python project-trajectory/scripts/record_observation.py --tc TC-209 --outcome pass --by "Claude Fable 5.1, WI-699"`;
the record file it wrote is committed alongside this verdict.

## Non-blocking findings (surfaced, not acted on)

1. The re-judge was triggered by inputs whose change did not touch the
   procedure section or the acceptance clause the case judges (a sibling
   section added to the same file; an assumption reference on the SR). The
   declared-input granularity is the whole file and the whole row, so any
   edit to either re-opens the case; that is the conservative side to err on,
   and no finding follows from it, but the cost is one full re-inspection per
   unrelated section added to `inspection-procedures.md`.
2. Same as WI-686's finding: `inspection-procedures.md` still restates a
   result (dated 2026-09-06) that the observation records now hold, inside
   the case's own declared input; the case's `evidence` cell points at that
   subsection rather than at `docs/test/observations/`.

OUTCOME: RECORDED result=pass
