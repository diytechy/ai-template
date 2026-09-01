# WI-555 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-555-wi508-partial-close/`, time-ordered, governing line
last. Two rounds were mechanized (Terra, cross-family, medium); two were drawn
by the supervisor through an independent Opus reviewer with a hostile brief
after a trunk merge on the lane (`5c8a007a`) staled the round-004 APPROVE at
the verdict gate. The verdict gate requires this per-WI rollup and nothing in
the kit writes it yet (the verdict-carrier repair is queued), so it is
compiled by hand.

### Supervisor note — NOT a round, does not govern

Why the lane needed a trunk merge and two more rounds. This lane was cut at
`6d3d9db4`, before its own worker performed the OI-71 conversion directly on
trunk (`979c3e5f` merge, `551d1b2c` mint), which moved
`docs/archive/last_approved/` and the registries there. The station refresh
(`merge --no-ff --no-commit` trunk, `add -A`, bar) then staged trunk's
snapshot delta, and two checks misread the refreshed index: the staged mirror
rule took the delta for a snapshot WRITE (integrity ERROR), and approval-fresh
compared the committed old snapshot against the live merged registries
(STALE). The refresh was refused twice on a tree whose plain merge passes both
checks. The precedented remedy (the wi508 branch's own `9bdd56b6`) — merge
trunk into the lane as a plain commit so the refresh carries no delta — was
applied, and the round it cost was drawn rather than waived. Blast radius:
this lane only (later lanes are cut from a trunk that already carries the
snapshot); the misfire is recorded as a kit finding in the session log.

### REVIEW-A — Round 2 — OPENAI-TERRA (medium) — tip a5a75d9

Reviewed the lane branch's own tree (base `6d3d9db4`), which still showed the
pre-conversion state because the conversion was performed on trunk under
OI-71's sanctioned manual special case. One MAJOR: the Deliverable asserted a
converted, merged and minted state that the branch tree did not contain, and
`integrate._merge_refusal` on that tree refused the wi508 claim as
outcome-less. Harness `RESULT: PASS`, strict integrity `integrity=0`.
(Full text: `002-REVIEW-A-a5a75d9.md`.)

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 4 — OPENAI-TERRA (medium) — tip 8c78410

Verified the rework's reconciliation: the finding was a pre-refresh artifact
of the record-only claim branch, not a live blocker — on trunk the real
admission read returns `claimed_specs=[]`, `check.py --jobs 0` `RESULT:
PASS`, strict integrity `integrity=0`; the default `check_trajectory` path is
clean and the strict-only failure is the unrelated pre-existing seam ERROR.
No findings.
(Full text: `004-REVIEW-A-8c78410.md`.)

VERDICT: APPROVE findings=0

### REVIEW-A — Round 5 — supervisor-drawn, independent Opus, hostile brief — tip 5c8a007

The conversion stands (commit range `ff29fef8..6ba27110` real, 44 commits;
`_claimed_specs(wi508)=[]`; WI-508 off `schedule.py ready`; strict integrity
`integrity=0`; brief current). Three record-level MAJORs: (1) the handback
merge carried the BRANCH's `docs/archive/last_approved/` bytes onto trunk,
collapsing `CURRENT.md`'s off-spine re-attestation census from "132 changed,
30 added, 3 removed" to "1 changed, 0 added, 1 removed" — trunk's unsigned
off-spine approval debt absorbed into the approved baseline by a `partial`
lane, undisclosed (not an authority breach under `human_approval_through =
"DevStg-Needs"`); (2) the immutable handback report's `## Delivered` says
"four Drafted" rows where LLR-203/LLR-204 are Approved; (3) Done-when arm 4's
"unflipped" premise is false as written (inherited from OI-72's wording).
Six MINORs: no `wi508-architectural-remap` ref exists (origin still `-HELD-`,
owner-owed); `CURRENT.md` regenerated on the branch, not by a trunk commit;
fragment without a file-level `Deferred open items:` line and a
`check_trajectory: clean` overstatement; bare `git mv` bypassing
`spec_move.py`; WI-568's 184-char minted Title; `render_report` boilerplate
inventing a "worker exited or crashed" reason. Routes: lane discloses and
corrects the record; OWNER rules restore-or-stand; WI-568 carries the
keep/discard; three kit rows.
(Full text: `005-REVIEW-A-5c8a007-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=9

### REVIEW-A — Round 6 — supervisor-drawn verification, independent Opus — tip 0143813

All three MAJORs discharged and verified claim by claim: the Deliverable's
"Corrected by round 005" paragraph and the fragment's final section carry the
pre-merge anchor (`6d3d9db4` / `13593db9`), the branch writers
`580df781`/`4824c0ba`, the exact census figures, the true 2-Approved /
2-Drafted split, and restore-or-stand named as the owner's ruling carried by
WI-568; `APPROVAL_RUNGS` + `human_approves` independently confirm "no
authority breach"; the `open_item` route WI-568 cites is a real mechanism
(`intake._inject_open_item`). `gen_open_items.py --check` accepts the
file-level declaration; `## Deliverable` still precedes `## Context`;
`check.py --jobs 0` `RESULT: PASS`. Five MINORs remain, none the lane's to
fix before merge: "nine rulings" should read ten (an error inherited from
round 005 itself); the spec's item 4 still says `check_trajectory` is clean
with the narrowing only in the fragment; WI-568's Title still warns; the three
kit findings have no row yet; `Deferred open items: none` is arguable.
(Full text: `006-REVIEW-A-0143813-supervisor.md`.)

VERDICT: APPROVE findings=5
