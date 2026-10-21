+++
id = "WI-833"
title = "An owner's verdict stays bound to the decision text it judged"
workstream = "process"
sr_refs = ["SR-225"]
needs = ["WI-892", "WI-832"]
specref = "docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Deferred 2026-10-20 (owner; coordinator-2026-10-20 D-016): held until the owner reviews the consolidation drill's proposed re-scope for this row (`C:/Projects/ai-template.wt/review-tmp/2026-10-20e-consolidation/consolidation-drill.md`), which checked the WI-788 rows against the review-churn rulings; it returns to queued/ with its re-scope applied and its scope critique re-run at the claim.

Re-homed 2026-10-10 (D-015): the shared lane-commit walk this row rides
moved from WI-828 (closed partial) to WI-892, which landed the same day.
OI-113 was ruled (d), won't fix, on 2026-10-14, and WI-893 was cancelled: no
hook walks a hand merge, and the merge slot is the sanctioned landing path.

Filed by hand by the wave-16 coordinator on 2026-10-05 from the independent
adjudicator's separate finding F2 at WI-818
(`docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md`, "Separate findings";
reproduced in `probe1.py`, "samerun"): a commit may rewrite an entry's
`decided`, `alternative`, `reversal_cost` or `why_not_escalated` while its
`owner` key stays, so a `confirmed` or `overruled` verdict then stands on text
the owner never read. The retired `reviewed` key had the same property.

## Done-when

- The ruling sync refuses a commit that changes a disclosure field of an entry
  whose parent carries `owner`, unless the same commit removes that `owner` key
  (commit against its parent; no history walk, no marker), at the pre-commit hook
  and on each lane commit in the merge slot.
- On a hand squash landing, the ruling sync also judges each folded-in commit
  through the shared lane-commit walk (WI-892).
- Tests: a disclosure edit under a kept verdict is refused staged and at the
  merge; the same edit removing the verdict passes; an edit to an entry with no
  verdict passes; an unparseable parent side refuses as the overrule sync does.
- SR-225's rows (LLR-283 or a new LLR, a TC) state the binding and pass
  adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
