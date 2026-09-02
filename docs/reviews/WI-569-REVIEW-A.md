# WI-569 — REVIEW-A rollup

Compiled by the supervising session (2026-09-02) from the round files under
`docs/reviews/wi-569-wi-508-spine-reseal-one-clean/`, time-ordered, governing
line last. Rounds 002–004 were drawn by the supervisor through an independent
Opus reviewer with a hostile brief; no mechanized round exists, for the reason
in the note below. `001-REVIEW-A-2f660cb7-spine-rows.md` is NOT a verdict on
this lane's diff: it is WI-569's own deliverable, the cross-family round on the
four SR-163 spine rows, and it is summarised here only because the lane's work
follows from it.

### Supervisor note — NOT a round, does not govern

How this lane was finished. The scheduler claimed WI-569 and WI-575 together
(both spine class, so one exclusive lane) and the worker assignment named
both. The single build session took WI-569 only, closed it, and stopped; the
weekday blackout opened three minutes later, so no second session ran and
WI-575 sat untouched in the claim. On the owner's direction the supervisor
stopped the loop, performed WI-575 by hand, and drew the lane's rounds. The
dispatch defect is the owner's to address separately.

The constraint the owner's 2026-09-01 ruling placed on lanes held throughout,
re-driven at every tip: `lane_approval_refusal` returns None over base..tip,
no `status` cell moved, nothing under `docs/archive/last_approved/` was
written. The lane amends three approved rows' text, which is the intended
route to the amendment adjudication this merge mints.

### The drawn round on the four rows (WI-569's deliverable, tip 2f660cb7)

Drawn on the cross-family strong route (gpt-5.6-sol) against a hostile
read-only brief naming the four rows and the standing-claim rule. It found
TC-199 and TC-200 stand with no finding, and that LLR-203 and LLR-204 did
NOT stand: trunk had moved under them and both still asserted that
mechanisms since delivered did not exist. Two MAJORs, both against the
approved LLR rows. The lane then corrected three false statements on LLR-203
and one on LLR-204, which round 002 below re-derived independently.

### REVIEW-A — Round 2 — supervisor-drawn, independent Opus, hostile brief — tip 4566ca2

The constraint clean and the substance sound: every corrected spine claim
re-derived true against the code, nothing true regressed, the drawn round
genuine and cross-family, both routed BLOCKERs discharged by accurate
annotations with the route named. Three MAJORs, all record defects: the
fragment's `Deferred open items:` declaration sat below its headings so
`gen_open_items --check` exited 1 on two lane-introduced findings and the
close claimed a green it had not produced; the Deliverable asserted in the
present tense that all four rows are cell-for-cell identical to `b8d57e9f`,
which the lane's own `33aee707` had made false; and the round file cited a
rollup that did not yet exist. Two MINORs: LLR-203's cell stated the
exclusion-carrier grammar with a hyphen where the parser partitions on a
literal spaced em dash, so a row written to its instruction would exclude
nothing; and the row amendment was a third act beyond the two arms this row
had been narrowed to.
(Full text: `002-REVIEW-A-4566ca2-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=5

### REVIEW-A — Round 3 — supervisor-drawn verification — tip 9f8cab1

Four findings closed and each correction verified by driving: the declaration
now sits above the first heading with the ruled OI token dropped, and the
check emits only the trunk-owned stale-surface advisory; the re-tensed
Deliverable sentence is true cell-for-cell against both `b8d57e9f` and the
lane base, with the drift correctly attributed; the cell now quotes exactly
what the parser partitions on, with the consequence traced through the
finding policy; the scope extension is recorded knowingly. One new finding:
the rework section said three findings were reworked where four were, the
fifth's remedy having landed in the same commit that called it out of scope.
(Full text: `003-REVIEW-A-9f8cab1-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 4 — supervisor-drawn verification — tip 4e8bbb0

The count corrected and reconciled against what the commits actually touched;
the closing paragraph's claims true clause by clause; no surviving
contradiction; the diff since the previous tip exactly the fragment and the
prior round file, with no registry, spec, ratify or plan file moved; the
constraint re-driven None at the tip; the check down to the trunk-owned
advisory alone.
(Full text: `004-REVIEW-A-4e8bbb0-supervisor.md`.)

VERDICT: APPROVE findings=0
