+++
id = "WI-850"
title = "A spine row is approved only after the rows it hangs from are"
workstream = "process"
sr_refs = ["SR-178"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
needs = ["WI-828"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.2,
row P3), carrying the owner's ruling 4 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`): a child is approved
only after its parent. The owner expected the check to exist. It does not:
LLR-281 and TC-291 have been Approved under SR-224, which is still `Drafted`,
since WI-615 (2026-09-28), and neither `trace.py --strict-integrity` nor a plain
`trace.py` run mentions it.

SR-224 sits on a released rung here (the dial is `DevStg-Boundary`), so an
adjudication sitting can settle its chain before the check lands.

## Done-when

- First, in its own act: SR-224's chain is settled. Either SR-224 is
  adjudicated for first approval, or LLR-281 and TC-291 return to `Drafted`.
- A commit that leaves an approved row (`Approved` or `Founded`) under a parent
  that is not approved is refused, where the commit moved either row's status.
  An SR waits for every SN it cites, an LLR for every SR, and a TC for every
  row it verifies. It is refused at pre-commit and on each lane commit through
  the shared lane-commit walk (WI-828).
- `trace.py --strict-integrity` reports any standing case as an integrity
  finding, naming the child, the parent and both statuses.
- `spine-authoring`'s parent-first rule (WI-848) names this check as its
  enforcer.
- Its rows (SR-178's chain, or a labelled derived SR if no approved row demands
  the rule) are authored as one change set and judged in one combined sitting.
- Tests: each tier pair; `Founded` counts as approved; demoting a parent under
  an approved child is refused; the standing finding.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. An adopter with an approved
  child under an unapproved parent sees the new integrity finding at upgrade,
  and the entry names the two remedies.
