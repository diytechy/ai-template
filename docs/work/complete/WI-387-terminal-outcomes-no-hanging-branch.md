+++
id = "WI-387"
title = "RULED 2026-07-31 (docs/concurrency-v2.md §A3) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. Make the owner's rule TRUE BY CONSTRUCTION rather than by sweep-up: WIs always land back into trunk, branches never hang. Leave no fourth option - EVERY lane ends in a merge. THREE TERMINAL OUTCOMES. MERGED: specs move to complete/, the ordinary case. CANCELLED: specs move to cancelled/ carrying the reason, and the branch MERGES ANYWAY so the cancellation is a trunk fact and the id stays retired - this is throw-the-work-away. HANDBACK: the work so far is committed as-is and the specs move back to queued/ (or draft/) with a ## Handback section naming what remains and a blockref if a human is wanted, and the branch merges. Handback IS the owner's quarantine requirement - the partial work lands in trunk where a future WI can pick it up, instead of living on a branch nobody will find. Neither exceptional outcome needs an adjudicator to sweep up, because neither is an exceptional PATH. WHAT THIS DELETES: the EXIT_NEEDS_HUMAN run-stop and the parked-branch stop. Today one WI wanting a human freezes an entire walk-away run; under handback the lane closes, the WI returns to trunk marked blocked and visible on the owner surface, and the dispatcher keeps working - same for any non-zero worker exit that is not a crash. A CRASHED worker is deliberately NOT a hang and keeps the machinery that already handles it: the branch exists and the specs are still in active/<branch>/, so the dispatcher re-assigns a lane (drive._parked_branches, unchanged). ONE MORE CONSTRAINT OF THE SAME SHAPE, while the file is open: _stranded_claims exists only because claim() does two writes (trunk commit, then branch cut) and a crash between them leaves a claim no lane can reach, costing an exit-2 refusal plus hand repair. Invert the order - commit-tree, then git branch, then advance trunk - and a crash leaves at worst an orphan branch whose claim commit is NOT an ancestor of trunk while its WI is still queued, which is definitionally an abandoned claim the dispatcher deletes and re-claims. The failure moves to the benign side, and _stranded_claims, its refusal path and its tests delete with it. THE RED-HANDBACK CASE IS RULED (owner decision 1, 2026-07-31): REVERT THE CODE and merge the spec move, the notes and the failing diff as a BAR-INERT artefact (a .patch under docs/work/), so the work is in trunk, findable, pickable by a future WI, and unable to red anything. The two rejected options were merging behind an expiring declared absence (honest, but it puts red code in trunk and adds an exclusion mechanism - a check where the governing principle wants a constraint) and conceding one legitimately parked case (spends the invariant). The frequency claim that originally motivated the ruling was CHALLENGED BY THE OWNER AND REFUTED, which strengthens rather than weakens it: §A6's failure table puts Class A - the WI's own code is broken - at ZERO at merge across this session's seven WIs, and none of the four EXIT_NEEDS_HUMAN causes in agent_loop.py is a red bar (no routable model / provider auth; a review escalation past the streak budget; critique budget exhausted still CHANGES-REQUESTED; a dual-plan page). The dominant handback shape is green-but-not-approved or cannot-proceed-for-config-reasons, both of which merge without trouble - so a genuinely rare path must earn neither an exclusion mechanism nor the invariant. A SECOND FINDING FROM THAT SAME READ MUST BE BUILT WITH THIS ROW: the verdict gate has to key off the OUTCOME, not off the claim. integrate._verdict_gate demands an APPROVE for every id in _claimed_wi_ids, which it reads from trunk's active/<branch>/, and a handback leaves those ids claimed at merge time - so as written the gate would demand an approval for work being RETURNED. Only the merged outcome asserts done and owes a verdict; cancelled and handback assert the opposite and owe none. This is not cosmetic: a review escalation is the most common handback cause, so without the fix the common path deadlocks on itself. Needs cancelled/ from WI-384 and the station protocol from WI-386. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-384", "WI-386"]
+++

## Deliverable

Every lane now ends in a merge, by construction. A lane declares its outcome by
the directory it moves its claimed specs into — the same move that already made
the branch finished — so `integrate.OUTCOME_DIRS` + `branch_outcomes()` read it
back off the tree: `complete/` = merged, `cancelled/` = cancelled, any open
folder = handback. There is no fourth answer and no state file that could hold
one; a claimed spec that landed nowhere resolves to nothing and the slot refuses
rather than guessing.

`_verdict_gate` is keyed off that outcome instead of off the claim: only
`merged` asserts done and owes an APPROVE. Without this the commonest handback
cause (a review escalation) would have deadlocked on itself, since a handback
leaves its ids claimed at merge time.

`hand_back` and `quarantine` ship in the new sibling `handback.py`. A handback
commits the work so far as-is, returns each spec to `queued/` with a
`## Handback` section naming what remains and the commit range it lives in, and
sets `blockref` to the spec's own path — which is what keeps the returned WI off
the ready frontier (`schedule._disposition` reads queued+blockref as blocked) and
so what stops the driver claiming and returning the same WI forever. The ruled
red arm reverts the product paths to the merge base and keeps the failing diff as
a bar-inert `.patch` under a `handback/` directory in `docs/work/`; nothing is lost, because the
reverted commits stay reachable in trunk history once the branch merges.

`drive.py` decides, `handback.py` writes: a DECIDED worker exit hands back and
the run keeps going, a CRASH keeps the parked-resume path unchanged, a lane that
already closed its specs merges on the outcome its tree names, and a red refresh
on a branch that merges nothing is quarantined once and refreshed again.
Deleted with all of that: the `EXIT_NEEDS_HUMAN` run-stop, the parked-branch
stop, and `drive._stranded_claims` — the last because `integrate.claim` now
writes `commit-tree` → `git branch` → trunk advance, moving the window between
its two ref writes to the benign side (an orphan branch `_abandoned_claim`
convicts on four facts — the exact claim subject, not an ancestor of trunk, a
parent that is, and a commit touching only bookkeeping surfaces — and the next
claim deletes and re-cuts, naming the sha it deleted).

The `## Handback` section joined the spec body grammar in all three F5 loader
copies plus the converter, which is what the section needed to exist at all: a
body the grammar does not know makes the row silently absent from the scheduler
while `check_trajectory` ERRORs on the same file.

REVIEW-A round 1 found six, all real, all fixed: the ruled red arm mis-parsed
`git diff --name-status -z` renames (three fields, not two) and reverted the
wrong paths while discarding four git return codes; `_abandoned_claim` matched a
subject SUFFIX and would delete a one-commit branch carrying real work;
`branch_outcomes` resolved a spec left in two folders silently, toward the
outcome that skips the verdict gate; two sentences of the claim rationale were
false and are retracted in place; a decided exit *after* a lane closed its specs
stopped the run; and the `EXIT_BUDGET`/`EXIT_STALL` walk-away cost was unrecorded.
Rounds 2 and 3 closed three more each — the unchecked `git branch -D`, a content
rule still wide enough to destroy a log fragment, and two stale size figures.

Merging trunk `4fb02de4` (this row is the last of four lanes) conflicted once, in
`_verdict_gate`'s docstring, where WI-378's freshness census met this row's
outcome keying. Both stand: they govern different halves of the same gate — which
paths stale an APPROVE, and which ids owe one — and the resolution adds only a
bridge naming where they meet. The `EXIT_TRAIN_END` exclusion turned out to be
load-bearing rather than cautious: WI-383's deletion landed, so naming that
constant would have made `drive.py` an `AttributeError` at import.

Tests: `tests/test_handback.py` (new, 13 tests, all constructing their own git
topologies; the rename parse mutation-proven), plus the outcome/claim-inversion
groups in `tests/test_integrate.py` — now with negatives that fail if the
matcher loosens — and the run-stop deletions driven end to end in
`tests/test_drive.py` against a conditional stub bar. Full record, deviations
and four findings owed their own rows: `docs/log.md`.
