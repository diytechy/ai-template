+++
id = "WI-413"
title = "The bare sweep re-mints a disposition for a still-marked returned spec (WI-388 REVIEW-A round-2 finding 6, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: intake.py's by-hand recovery CLI, run bare (sweep with symbolic HEAD), tokenizes the disposition title with the CURRENT head - so a returned spec still carrying its Handback section re-mints a duplicate disposition on every sweep run until the first disposition closes. Bounded: by-hand CLI only (the slot's own intake passes the merge sha), visible in the queue, cancellable - which is why it rode the APPROVE as a recorded finding. THE FIX, in the reviewer's recorded direction (pick one and test it): derive the sweep's dedup token from the RETURN EVENT's own last-touch commit of the returned spec (git log -1 on the spec path - one event, one token, however many sweeps), or make the handback arm dedupe against an OPEN disposition row citing the same spec (state-based dedup instead of title-token). Tests: the reviewer's drive - sweep twice against one still-marked spec must mint ONE disposition; a genuinely new second handback (new return commit) must still mint a second. Scope: intake.py's sweep arm + tests."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

CANCELLED as SUPERSEDED (plan §11.9). Its defect — the bare sweep re-minting a disposition for a still-marked returned spec — was structural: the return event had no identity, so every dedup token had to be derived from a mutable proxy, and two independent REVIEW-A rounds rejected both derivations available inside this row's declared scope.

SN-031 dissolves the defect CLASS rather than fixing the instance: a close is an immutable per-close report under `docs/handbacks/`, the disposition's title keys on that report's PATH, and sweeping twice produces the same title twice for the mint's exact-title dedup to answer. There is no longer a token to get wrong.

This row also carried the last `## Handback` section in the repo — the one-file migration SN-031 measured — and that section is removed here with the contract it belonged to.
