+++
id = "WI-676"
title = "adjudicate: SR-209, TC-242 - approved cells amended to the loop-lane ownership rule SR-209's blessed acceptance states; judge whether scope moved"
workstream = "process"
specref = ""
sr_refs = ["SR-209"]
needs = ["WI-673"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-209", "TC-242"]
priority = 2
+++

## Deliverable

The verdict `VERDICT: MEANING rows=2`, blessable, landed at e8ca47f7
(`docs/reviews/wi-676-adjudicate-sr-209-tc-242/001-ADJUDICATE-7f98adc.md`;
Codex Sol cross-review SOUND). Its re-anchor was refused on 2026-09-27
because WI-650 had since amended SR-217 and TC-250 in the live files. It is
taken here, in ONE act with WI-675's rows, on trunk 97815a8c:
`intake.py snapshot --reattests SR-209,TC-242,SR-217,LLR-257,TC-250`
(act ledger seq 3). Before relying on the verdict, the batch adjudicator
confirmed with `tomllib` that SR-209 and TC-242 are byte-identical, cell for
cell, at 97815a8c and at 7f98adc9, the commit the verdict judged.

## Context

**State at the 2026-09-27 handoff: verdict landed, re-anchor owed.** The
independent adjudicator's verdict, `VERDICT: MEANING rows=2`, is committed
(`docs/reviews/wi-676-adjudicate-sr-209-tc-242/001-ADJUDICATE-7f98adc.md`),
and Sol's cross-review of it was SOUND. Its re-anchor act (51970385 on
`build/wi-676`) was taken at 7f98adc9, before WI-650 amended SR-217 and TC-250
in the live files. On trunk that copy is no longer byte-identical to the live
registries, and the approval-record rule refuses it. So the re-anchor is owed
as ONE act together with WI-675's rows (SR-217, LLR-257, TC-250), taken on
current trunk once WI-675 is adjudicated:
`intake.py snapshot --reattests SR-209,TC-242,<WI-675's blessed rows>`.
Close this item in that commit.

SR-209's `acceptance_criteria` states the merge slot's lane-ownership rule:
the slot sees commits, not processes, so a lane is the loop's when its claim,
or any commit one of the loop's own writers made in its range, carries the
trailer; every commit of a loop lane is judged whoever runs the slot, a
person's included; the commits before the lane's first trailer-carrying
loop-writer commit are exempt; a person's own lane is not judged. That
acceptance was re-anchored by WI-669 as true of the code. The cells around it
still described the older actor rule, so WI-673 amended them in place, status
left `Approved`, with no behaviour change:

- SR-209 `requirement`: the trigger was "the unattended loop creates a
  commit"; it now also names a commit merged in a lane the loop owns, from the
  point the loop took that lane over (the exemption window).
- SR-209 `rationale`: the claim that trailers appear on only some loop
  commits and nothing checks them, no longer true, is made counterfactual
  (what a missing trailer would prove without a total floor); the
  who-not-when argument is scoped to where a commit
  is made, and the proxy is argued where a lane merges (the slot cannot tell
  an unmarked loop commit from a person's; a person's commit belongs in their
  own lane; the pre-takeover commits are exempt because nothing could have
  marked them); the local floor's bypass is now backed by the merge re-check
  as well as the history check.
- TC-242 `method`: states every case its evidence drives, adding the
  lane-ownership cases (a loop lane judged when the slot runs without the
  marker; a person's own lane not judged with or without it; a lane a person
  claimed and the loop later built judged from its first marked loop-writer
  commit, the earlier commits exempt), the admitted fully-marked lane, the
  grammar's refusal to format a bad session, the trailer joining git's
  trailer block, the slot accepting any well-formed session, the quarantine
  and mechanical-close writers, and the writers' subjects reading as loop
  writers' commits.
- TC-242 `expected`: a non-loop commit passes WHERE IT IS MADE, and no longer
  passes inside a loop lane at the merge; the lane-ownership rule and the
  exemption window are stated.

No traced pointer cell moved on either row. The evidence is
`tests/test_loop_provenance.py` and `tests/test_pre_commit_hook.py`
(`test_commit_msg_hook_holds_a_loop_commit_to_its_provenance_trailer`); the
code is `kitlib/provenance.py` (`loop_writer_commit`, `loop_lane_window`,
`loop_trailer_refusal`), `integrate.py` (`_loop_window`,
`_loop_trailer_refusal`) and `check.py` (`--loop-trailer`, run by the
commit-msg hook).

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in its own commit,
  naming exactly SR-209 and TC-242; one that is not gets its corrective work
  drafted in `## Dispositions`.
