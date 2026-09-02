## 2026-09-01 — the owner rules OI-78: STAND — the wi508 approval act was delegated, so its baseline stands; the delegation's target was the adjudicator, not a worker lane

The owner read the corrected card (`bb0c5edd`: the absorbed interfaces rows
are `Drafted` on both sides; what the whole-tree copy erased is the
change-disclosure census of the OI-67 reshaping, not an approval) and ruled
**STAND**: trunk's `docs/archive/last_approved/` baseline for the three
off-spine registries stays at the bytes the wi508 handback merge carried in.
The reseal successor's "stand" branch applies once its other predecessor (the
copy-scope fix) has landed, so the reseal re-seals the four spine rows and
nothing else.

The owner's reason, recorded because it reframes the delegation: the
2026-08-30 delegation was real, but its intended target was the
**adjudicator** — a trunk-side session with the whole chain in front of it —
not the worker lane that resumed the row. The supervising session of
2026-08-30 wrote the delegation as "the lane that resumes this row approves
the four Drafted rows", and the lane did. The owner's stated design intent:
approval acts on spine rows are the adjudicator's alone, partly for context
and partly for **concurrency** — two worker lanes touching the spine can
conflict at merge, and a serial trunk-side act cannot. The record's OI-45 (b)
sentence ("fully expected that an LLM session or adjudicator flips a row's
Status") was written with that session in mind and can be read wider; the
owner acknowledges the ambiguity. The executing change is the owner's next
ruling (a plan and row are drafted at the owner's confirmation of the exact
wording); it is not folded into this one.

Two facts the owner asked for, established from the record: the wi508 row
was classed `safety_class = "spine"`, which the scheduler dispatches as an
exclusive lane (no concurrent claim while it runs), so no second lane could
have touched the spine alongside it; and the snapshot still moved on that
lane's branch — the exclusivity guards the registries, not the baseline,
which is the copy-scope row's business.

Deferred open items: none — this entry records a ruling; the follow-on ruling on the approval act's owner is the owner's to word first.
