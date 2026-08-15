+++
id = "WI-458"
title = "Complete the re-tier's class-A authoring calls: the seven unruled mint/merge/re-classify decisions the top-down read surfaced (H1 the unminted B-05 MAPPING observable; H4 the SR-148/SR-153/SR-059 triple statement of SN-025; H5 the SR-031/SR-137 duplicate tomllib-vs-sh observable, already diverged; M1 the four rows that escaped demotion against the campaign's own criterion, two of them Verified; M3 the three needs with zero textual coverage despite orphans=0; X1/X2 the two crossing attributions revised in act 7 and flagged for overrule), plus SR-165's missing design row and test case without which it cannot leave Draft. Each call carries a recommendation; the owner rules, the builder executes. Same class as the SR-141 merge already performed inline this month - NOT a sitting."
specref = "docs/plans/2026-08-15-retier-completion.md#2-blocker-class-a--seven-unruled-authoring-calls"
workstream = "process"
sr_refs = ["SR-008", "SR-021", "SR-030", "SR-031", "SR-059", "SR-133", "SR-137", "SR-139"]
needs = []
buildtier = "strong"
safety_class = "adjudication"
priority = 1
+++

## Context

The re-tier merged as `partial` 2026-08-15. This row is the first of the three
that finish it — the **authoring calls**, all judgement, none mechanical. The
full statement of each, with evidence and the interface rows it moves, is
[the completion analysis](../../plans/2026-08-15-retier-completion.md) §2; the
needs of M3 are SN-026, SN-029 and SN-037. The originating detail is the lane ledger
[2026-08-14-wi451-slice2-ledger.md](../../plans/2026-08-14-wi451-slice2-ledger.md)
lines 330–334.

**These are a deliverable of the campaign, not a failure of it** (owner, log
`13s`). A layer that did not exist an act earlier could be read as one, and
reading it produced a ranked list instead of a feeling.

## The sequencing rule that must not be inverted

**Rule these BEFORE any interface-registry work.** Measured: class A moves
**11 interface rows'** `sr_refs` — six via SR-153 (H4), two via SR-031 (H5),
three via SR-008/SR-030 (M1). The ruled interface model (log `2026-08-15a`)
moves **zero** SR ids, because its owner cell lands on the IF row. The churn is
one-directional. Reversed, those 11 rows are re-pointed twice.

## Two guards on the calls themselves

**M1's attestation objection is DISSOLVED.** SR-008 and SR-133 are `Verified`.
The owner ruled 2026-08-15 that overriding a historical attest is fine where it
improves the design — *"that is the entire purpose of this exercise: to rebuild
the breakdown and reassign the work to verify the design."* So `Verified` is no
longer a reason to leave a row mis-tiered. **The demotion calls themselves are
still owed**, and a demotion that moves an attested row must surface on the
re-attest brief rather than ride in quietly.

**X1/X2 cannot be delegated to a checker.** `trace.py` verifies that a crossing
reference *resolves*, never that it is the *right* crossing. Nothing mechanical
can catch a wrong answer, so if these are not looked at deliberately they stand
unexamined — which is the state that produced them.

## Done-when

- Each of H1, H4, H5, M1, M3, X1, X2 has a recorded ruling and its executed
  consequence, or an explicit deferral naming what it waits on.
- `SR-165` carries a design row and a test case, or its Draft status has a
  stated reason to persist.
- The 11 interface rows the calls move are re-pointed in the same act, with
  `trace.py` reporting zero dangling IF→SR pointers.
- No Status flip that belongs to sitting 3's ratification wave happens here —
  this row re-tiers rows, it does not sign them.
- The full suite (`pytest -q -n auto`, unfiltered) is green and pasted. **Not
  smoke**: smoke was green through all four defects this campaign found late,
  two of them at the merge bar.
