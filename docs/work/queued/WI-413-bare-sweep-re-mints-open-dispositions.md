+++
id = "WI-413"
title = "The bare sweep re-mints a disposition for a still-marked returned spec (WI-388 REVIEW-A round-2 finding 6, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: intake.py's by-hand recovery CLI, run bare (sweep with symbolic HEAD), tokenizes the disposition title with the CURRENT head - so a returned spec still carrying its Handback section re-mints a duplicate disposition on every sweep run until the first disposition closes. Bounded: by-hand CLI only (the slot's own intake passes the merge sha), visible in the queue, cancellable - which is why it rode the APPROVE as a recorded finding. THE FIX, in the reviewer's recorded direction (pick one and test it): derive the sweep's dedup token from the RETURN EVENT's own last-touch commit of the returned spec (git log -1 on the spec path - one event, one token, however many sweeps), or make the handback arm dedupe against an OPEN disposition row citing the same spec (state-based dedup instead of title-token). Tests: the reviewer's drive - sweep twice against one still-marked spec must mint ONE disposition; a genuinely new second handback (new return commit) must still mint a second. Scope: intake.py's sweep arm + tests."
specref = "docs/reviews/WI-388-REVIEW-A.md"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
blockref = "docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md"
+++

## Handback

Returned unfinished from lane `wi-413-bare-sweep-dedup-token`: NEEDS-HUMAN: a correct fix needs a return-event identity PERSISTED AT HANDBACK TIME (an immutable id written into the returned spec by handback.py), which is outside this row's declared scope of "intake.py's sweep arm + tests". Two independent REVIEW-A rounds rejected both derivations available inside that scope - the spec's last-touch commit, and a digest of the `## Handback` note. Owner ruling needed on widening scope, plus a migration answer for specs already returned. Both verdicts: docs/reviews/WI-413-REVIEW-A.md

**What remains:** whatever this spec asks for that `51224025ab..b5ea06478e` did not finish. Read that range (`git log --oneline 51224025ab..b5ea06478e`, `git diff 51224025ab..b5ea06478e`) before re-claiming — the work so far is in trunk, not on a branch. Clearing the `blockref` puts this back on the ready frontier.
