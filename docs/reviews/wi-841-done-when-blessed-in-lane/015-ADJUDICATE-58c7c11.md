# WI-841 amendment adjudication at 58c7c11

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchors copied at 61b8972f (LLR and TC).

- [MEANING] LLR-278 Detail -> every act the merge adds that NAMES a verdict must name an accepted one; an act naming no verdict is judged by the other scope rules alone -> every act an adjudication merge adds, held or released and including a first approval in it, is refused unless an accepted verdict of EACH KIND IT TAKES, among the branch's bindings, covers it, WHETHER OR NOT the act names a verdict -> the exemption for an act naming no verdict is removed, and coverage is now per kind (a flip needs a first-approval verdict, a re-attestation an amendment one) drawn from the branch's own bindings. A merge correct under the old text passes a verdict-less act that has no accepted binding behind it, and the new text refuses it
- [MEANING] TC-278 Method -> the cases permitted to merge need no stated binding; on a released rung an act naming an unaccepted verdict is refused -> each permitted act carries an ACCEPTED verdict of each kind it takes in the branch (written by `_bind_branch`); a named verdict must itself be accepted; and omitting `--verdict` does not waive the branch binding -> new fixture preconditions on every merging case, and a new refused case (the omitted verdict), so a run that met the old Method no longer meets the new one
- [MEANING] LLR-310 Detail -> every added act NAMING a verdict needs an accepted verdict -> every act an adjudication merge adds, naming a verdict or not, needs an accepted verdict of each kind it takes among the branch's own bindings -> the same widening as LLR-278: verdict-less acts now need kind-matched accepted coverage

All three rows are MEANING, and the LLR and TC tiers' rung is RELEASED, so the blessing is the adjudicator's to give. I would bless each new text:

- The three cells state one rule. An adjudication lane's act draws its authority from the accepted adjudications the lane actually ran, kind by kind, so omitting `--verdict` cannot skip the acceptance check.
- The code matches. `kitlib/sitting.py` reads the branch's bindings (`branch_verdicts`) and maps each act key to the kind it needs (`_ACT_KINDS`: approved -> first-approval, reattested -> amendment), and `acceptance_record.merge_approval_refusal` consumes it.
- `test_an_act_omitting_its_verdict_is_still_tied_to_an_accepted_one` drives the omitted-verdict refusal, and `_bind_branch` gives every merging fixture the accepted binding TC-278 now requires.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=3
