# WI-772 adjudication: SR-215, LLR-254, LLR-255, TC-247, TC-248, and the carried TC-036, TC-055, TC-209, TC-210, TC-211

Independent adjudicator: Claude Opus 5.5. I directed none of WI-747, WI-770 or WI-766/767.
The anchor is `docs/archive/last_approved` (SR copy d46c5278; LLR and TC copies db0bc37f).
I read batch N's verdicts as prior findings and checked whether they were answered; they bind nothing here.
I checked each row against `rejudge.py`, `observation_cadence.py`, `intake.py`, `gen_release_checklist.py`,
the gate-advance skill, `tests/test_rejudge.py`, `tests/test_intake.py` and `tests/test_skills_index.py`.

- [MEANING] SR-215 Requirement/AcceptanceCriteria/Rationale/Coincident/Title -> at a merge or a release, file one item per observation case whose declared inputs changed, whose result expired or which has none; one open item per case -> at a merge, a release or a stage gate, file one item per DUE case: no result or an expired result at once; otherwise only a declared trigger (files, component, release, stage gate) firing past a closed-work floor (raisable per case, never lowerable); with no trigger, changed inputs fire only past the same floor; policy read at the revision; a case citing no written pass criteria warns, never fails -> a correct old implementation (re-judging every changed case at every merge) fails the new text, and the new text adds a checkpoint, triggers, a floor and a warning. The Requirement and AcceptanceCriteria cells carry the move.
- [MEANING] LLR-254 Detail -> due_cases digests declared inputs at the revision and drafts for a changed digest, an expired record or no record -> checkpoint_for maps an explicit release or stage-gate Trigger to its checkpoint, else merge; due_cases applies the cadence floor and trigger before the digest rule; absence and expiry bypass the floor; a draft names the reason, the rubric and the fired trigger -> the decision now withholds drafts the old text required and names more in each draft.
- [MEANING] LLR-255 Detail/Title -> merge slot and `intake.py rejudge --checkpoint release`; the release checklist carries a required item naming that command and the due count -> adds the stage-gate entry, the refusal of a merge checkpoint at the command, and the gate-advance skill's required pre-sign step; the checklist count is the count due at the release checkpoint -> a new entry, a new refusal and a new prompt surface are obligations the old text did not impose.
- [MEANING] TC-247 Expected/Method -> check that changed, expired and unrecorded cases each get one draft naming the case and the change, an unchanged one none, an open item suppresses a second, inputs and links read at the revision -> check the floor bypass for absence and expiry, the floor on changed inputs, each trigger kind firing only past the floor, raise-but-not-lower, the draft naming reason, rubric and trigger with the inputs-digest prefix in its title, policy read at the revision -> new acceptance cases (floor, triggers, policy, rubric naming) were added.
- [MEANING] TC-248 Expected/Method -> merge and release each file one item per due case; the checklist carries the required item -> adds the stage-gate command (files once past the floor, not at merge, not twice), the CLI's merge refusal and the gate-advance skill's required step; the merge condition is now trigger plus floor -> a third checkpoint and two new checks were added.
- [MEANING] TC-036 Rubric/Trigger/MinWorkItems -> no rubric; due at the next merge after any declared input changed -> judged against `resync-inspection.md`; due only when ADOPTING.md or the downstream-resync skill changes and the 10-closed-WI floor has passed -> a change to its other declared input (SR-036) no longer makes it due, and its pass criteria are now fixed.
- [MEANING] TC-055 Rubric/Trigger/MinWorkItems -> due at the next merge after any declared input changed -> due only when a CMP-009-tagged module or owner changes past a 10-WI floor, judged against `dashboard-usability.md` -> the trigger set (now every CMP-009 module) and the timing (the floor) both moved.
- [MEANING] TC-209 Rubric/Trigger/MinWorkItems -> due when `inspection-procedures.md` or SR-184 changed -> due only at release preparation past a 10-WI floor, judged against `critique-provenance.md` -> an input change no longer fires it.
- [MEANING] TC-210 Rubric/Trigger/MinWorkItems -> due when `inspection-procedures.md` or SR-185 changed -> due only at release preparation past a 10-WI floor, judged against `counterpart-review.md` -> an input change no longer fires it.
- [MEANING] TC-211 Rubric/Trigger/MinWorkItems -> due when `inspection-procedures.md` or SR-186 changed -> due only at release preparation past a 10-WI floor, judged against `decomposition-proportionality.md` -> an input change no longer fires it.

Routed or traced pointers the brief did not render, read and ruled, not counted in rows=N:
LLR-254 CodeSymbol gained `checkpoint_for`, which exists in `rejudge.py` tagged `Implements: SR-215, LLR-254` and which the new Detail now states (batch N finding 4, answered).
TC-248 Evidence gained `tests/test_skills_index.py::test_gate_advance_names_the_stage_gate_rejudge_step`, which exists and pins the skill step.
Both are sound.

## Batch N's findings, checked

1. "No result is due immediately" parsed two ways. Answered: "A case with no result is due at once".
2. The rubric authoring clause in SR-215's acceptance. Answered: replaced by the observable half, a warning that never fails, even under strict. `trace.py --strict` no longer prints SR-215's CRITIQUE-instrument advisory (run at 2256e4e3).
3. SR-215's Coincident and Title were stale. Answered. The new Coincident names the needs' outcome (SN-008, an honest pass; SN-024, a written rubric) and states the floor's cost bound openly rather than hiding it.
4. `checkpoint_for` had no obligation in LLR-254's Detail. Answered.
5. TC-248 no longer checked that the checklist item is required and names the command. Answered, and `test_the_release_checklist_carries_the_required_rejudge_item` asserts both.
6. Addendum: TC-247 left LLR-254's naming clause unverified. Answered. TC-247's Method names the reason, rubric and trigger; `test_trigger_waits_for_closed_work_floor` asserts the rubric and fired-trigger lines.
7. The stage-gate prompt was missing at the gate. Answered by LLR-255's clause and the shipped skill paragraph (`project-trajectory/skills/gate-advance/SKILL.md`).

## Re-attestation

The dial releases these tiers, so the re-attestation is mine. I would bless all ten rows as written.
They carry out the owner's signed direction in WI-747: a rubric first; first judgement as today; a declared trigger with a floor (a default in `docs/process.toml`, raisable per case); `max_age` as the backstop; and the input-change rule under the floor when no trigger is declared.
Ruling R2 holds: no SR-215 cell names a script, command, file or function. The five rubrics the carried cases cite exist under `docs/rubrics/`.
They are named in the combined act's `--reattests`.

Findings that do not withhold the blessing, for the record:
- TC-247's Method says policy is read at the revision and "uncommitted changes affect neither". No test asserts this for the policy file; `tests/test_rejudge.py` checks it for inputs only. That is a test lagging its text, not a text defect. The test-only addition is folded into the follow-up drafted in WI-773's `## Dispositions`.
- LLR-254's "suppressing an open item by its typed Brief and Adjudicates cells" means that an open item, found by its typed cells, suppresses the draft. "Never by title" makes the reading unambiguous. Worth tightening at the next amendment that touches the row; not a reason on its own.
- The gate-advance paragraph says the stage-gate command files items for cases whose `stage-gate` trigger is due. The command also files no-result and expired cases and other triggered cases at that revision. The paragraph is not a row under judgement, and its required step is correct.

VERDICT: MEANING rows=10

## Addendum 2026-10-03 (after the Sonnet cross-review of 1d0c7bf2)

The recorded lines, the machine line and the re-attestations in act seq 22 stand. Two misses are recorded here, and the coordinator has ruled that the act is not redone for them.

1. **TC-055's Expected was not read.** I ruled TC-055 on its amended cells alone (Rubric, Trigger, MinWorkItems). Its unamended `expected` still states the old cadence: "re-judged at a merge or release checkpoint when no result of it is on record, when a declared input changes, or when the record passes its declared max_age". With the Trigger now `component:CMP-009` and a floor of 10, an input change no longer makes it due. So the re-attested row carries a stale sentence. That sentence is a standing limit in the row's Expected, not its pass criterion, but it is false. Had I read it, I would have withheld TC-055's re-attestation and routed the fix to the successor lane. The exact replacement of TC-055 `expected` is now in the follow-up drafted in `docs/work/queued/WI-773-adjudicate-llr-293-llr-294.md` `## Dispositions`. That lane's merge mints an amendment adjudication for it.
2. **SR-215's Rationale overclaims a bound.** "It lets an accepted judgement outlive changes to what it judged for at most the configured number of closed work items" holds only for a case with no trigger, where an input change fires it. A `release` or `stage-gate` trigger, or a `files:` or `component:` trigger that a change does not match, lets a judgement outlive more, bounded only by expiry. The Requirement and AcceptanceCriteria cells state the rule correctly; the Rationale's gloss on it does not. An exact replacement sentence is in the same follow-up, and its merge re-adjudicates SR-215.

Sonnet also noted that TC-247 was blessed under a looser standard than the rows I returned: its Method's policy-file clause has no test. The verdict above already routes that test to the follow-up lane, and the follow-up keeps it.
