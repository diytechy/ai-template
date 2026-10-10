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

Landing order (scope critique, 2026-10-10): one deliverable, the recorded comparison; any successor it drafts is filed on trunk and claimed on its own.

## Trust

The sitting's verdict file can authorize successor minting and bless the closed Done-when text (`project-trajectory/PROCESS.md` §3, "When a guard is owed"):

- **Producer:** the independent adjudicator's retained session, launched by `project-trajectory/scripts/coordinator_adjudicate.py adjudicate --brief done-when`, which reserves the verdict path exclusively before launch. A failed call, a timeout or a structured error exits non-zero and leaves no accepted verdict; a partial or malformed verdict is refused by the entry point's verdict check and not committed as a judgement.
- **Consumers** (found by grep): `project-trajectory/scripts/coordinator_adjudicate.py` and `project-trajectory/scripts/kitlib/sitting.py` (accept or refuse the verdict), `project-trajectory/scripts/kitlib/done_when.py` and `project-trajectory/scripts/adjudicate_brief.py` (the digest-bound blessing of the judged text), `project-trajectory/scripts/intake.py` (mints the drafts in `## Dispositions`), and `project-trajectory/scripts/agent_loop.py` and `project-trajectory/scripts/integrate.py` (read the row's state).
- **Ruling:** an absent, unreadable, failed or malformed verdict blesses nothing and mints nothing; WI-886 stays open. A blessing binds to the exact closed Done-when text by its digest; a changed text is unblessed. Only drafts in an accepted verdict's `## Dispositions` are minted. WI-847's completed merge stands whatever the ruling.
