+++
id = "WI-413"
title = "The bare sweep re-mints a disposition for a still-marked returned spec (WI-388 REVIEW-A round-2 finding 6, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: intake.py's by-hand recovery CLI, run bare (sweep with symbolic HEAD), tokenizes the disposition title with the CURRENT head - so a returned spec still carrying its Handback section re-mints a duplicate disposition on every sweep run until the first disposition closes. Bounded: by-hand CLI only (the slot's own intake passes the merge sha), visible in the queue, cancellable - which is why it rode the APPROVE as a recorded finding. THE FIX, in the reviewer's recorded direction (pick one and test it): derive the sweep's dedup token from the RETURN EVENT's own last-touch commit of the returned spec (git log -1 on the spec path - one event, one token, however many sweeps), or make the handback arm dedupe against an OPEN disposition row citing the same spec (state-based dedup instead of title-token). Tests: the reviewer's drive - sweep twice against one still-marked spec must mint ONE disposition; a genuinely new second handback (new return commit) must still mint a second. Scope: intake.py's sweep arm + tests."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit `b05dca68`.

THE DEFECT. The disposition title's event token came from `after7`: the merge
sha at the slot, but symbolic `HEAD` from the by-hand recovery CLI, which
`_rev7` resolves to whatever is checked out *now*. The mint's own bookkeeping
commit already moves it, so a bare `intake.py sweep` re-run — while the
returned spec still carried its `## Handback` section, which it keeps through a
defer or a re-queue — named one event with a fresh token and minted a duplicate
disposition on every pass.

THE FIX, and why this one of the two offered. `_return_event7` derives the
token from the return event itself (`git log -1` on the returned spec's path):
one event, one name, however many sweeps observe it. The reviewer's alternative
— dedupe the handback arm against an OPEN disposition for the row — was
declined because it cannot satisfy both halves of this row's own test list: it
would suppress the second return's disposition exactly while the first is still
open, and the row requires a genuinely new handback to still mint. The token
approach gets both, because `handback.returned_spec` rewrites the spec (a
`blockref` plus a `## Handback` note naming the lane and its commit span), so a
second return necessarily lands a new commit on that path.

THE LIMIT, STATED. Two returns whose rewritten spec text came out
byte-identical would leave no new commit on the path and would share a token.
The note embeds the lane name and commit span, which makes that unreachable in
practice — but it is the assumption the fix rests on, and it is written into
`_return_event7`'s docstring rather than left for someone to discover.

AN EXISTING GREEN TEST WAS CHANGED, DELIBERATELY AND VISIBLY.
`test_a_second_handback_of_the_same_row_mints_a_second_disposition` simulated
its second handback by committing an *unrelated* file and relying on the merge
sha moving. That stood in for a return only while the token was the merge sha;
under a token naming the return event it is not a second handback in any sense
— and it never was one in the repo either. The fixture now does what the
shipped code does. This is called out in the commit message and here because
editing a twice-reviewed green test to make one's own change pass is the move
that most deserves an independent look.

TESTS. Two new drives: a bare sweep run three times against one still-marked
spec mints exactly ONE disposition, and a genuinely new return (a real spec
rewrite) still mints its own. Mutation-checked — reverting the token to the
observer's `HEAD` fails the first.
