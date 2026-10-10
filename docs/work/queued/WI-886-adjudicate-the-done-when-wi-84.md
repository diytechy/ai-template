+++
id = "WI-886"
title = "adjudicate the Done-when WI-847 changed in its own lane wi-847 - does the close still answer the row as claimed? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = "docs/archive/work/complete/WI-847-loop-reviewer-resumes-in-lane.md"
buildtier = "medium"
safety_class = "adjudication"
brief = "done-when"
adjudicates = ["WI-847"]
+++

## Context

`docs/archive/work/complete/WI-847-loop-reviewer-resumes-in-lane.md` closed with a Done-when that differs from the one it was claimed with (ticks and trailing evidence already set aside), and no in-lane verdict or owner ruling blesses the closed text. A reviewer maps coverage against that list, so a change made by the lane it judges is the goalposts moving:

- at claim, no longer present as written: "The loop's REVIEW role can resume its session within one lane's review chain, through the same keep operation, the store and the lease (`retain_for` gains the review class behind its own dial; shipped off)."
- at claim, no longer present as written: 'The review that gates a merge is always a fresh session over the full lane (claim base to tip), never a resumed one.'
- at claim, no longer present as written: 'Tests: two iteration rounds resume one session; the merge-gating round mints fresh and covers the claim base to the tip; dial off changes nothing.'
- at claim, no longer present as written: "The narrow round's reading scope (the round's delta) is a render of `prompts/reviewer.template.md` through `prompts.py`, the same render the coordinator's reviews use."
- at claim, no longer present as written: 'SR-227 amended to cover the review class, or a new SR; its rows state it and pass adjudication on the one adjudication path.'
- added since claim: "The narrow round's reading scope (the round's delta) is a render of `prompts/reviewer.template.md` through `prompts.py`, the same render the coordinator's reviews use, with one home for the narrow range sentence."
- added since claim: 'A template override that cannot carry the slots refuses the render.'
- added since claim: "Tests: the loop's narrow render carries the delta and the attended render's range sentence; an override without the slots refuses."
- added since claim: 'The rows the change makes untrue or incomplete (LLR-045, TC-082) state it and pass adjudication on the one adjudication path.'

Judge whether each change only clarifies or moves the scope. A moved scope is a successor row, never a reversal - the merge stands.
