+++
id = "WI-413"
title = "The bare sweep re-mints a disposition for a still-marked returned spec (WI-388 REVIEW-A round-2 finding 6, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: intake.py's by-hand recovery CLI, run bare (sweep with symbolic HEAD), tokenizes the disposition title with the CURRENT head - so a returned spec still carrying its Handback section re-mints a duplicate disposition on every sweep run until the first disposition closes. Bounded: by-hand CLI only (the slot's own intake passes the merge sha), visible in the queue, cancellable - which is why it rode the APPROVE as a recorded finding. THE FIX, in the reviewer's recorded direction (pick one and test it): derive the sweep's dedup token from the RETURN EVENT's own last-touch commit of the returned spec (git log -1 on the spec path - one event, one token, however many sweeps), or make the handback arm dedupe against an OPEN disposition row citing the same spec (state-based dedup instead of title-token). Tests: the reviewer's drive - sweep twice against one still-marked spec must mint ONE disposition; a genuinely new second handback (new return commit) must still mint a second. Scope: intake.py's sweep arm + tests."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit `b05dca68` (round 1) and the round-2 rework
below. REVIEW-A returned **REWORK** (1 BLOCKING, 2 MAJOR, 1 MINOR) against the
round-1 design; what shipped is the reworked one.

THE DEFECT. The disposition title's event token came from `after7`: the merge
sha at the slot, but symbolic `HEAD` from the by-hand recovery CLI, which
`_rev7` resolves to whatever is checked out *now*. The mint's own bookkeeping
commit already moves it, so a bare `intake.py sweep` re-run — while the
returned spec still carried its `## Handback` section — minted a duplicate
disposition on every pass.

ROUND 1 TOOK THE REVIEWER'S FIRST DIRECTION AND IT DID NOT HOLD. Deriving the
token from the returned spec's last-touch commit (`git log -1 -- <path>`) names
the last touch for ANY reason, not the return. REVIEW-A drove three breaks:
clearing a `blockref` to re-queue moved the token; moving a still-marked spec
`queued/` → `deferred/` moved the token AND the path embedded in the title;
untracked or shallow history had no answer and fell back to the changing
observer. Worse, `%h` returns an *unambiguous* abbreviation that git lengthens
on collision, so truncating it to seven could make two distinct returns share a
token and silently suppress a judgement somebody was owed — the worst failure
class available here.

WHAT SHIPPED. `_return_token` identifies the return by a digest of its own `##
Handback` note — the record `handback._note` writes, naming the lane and the
commit span of the work that did not finish. It needs no git history, so
shallow clones and untracked trees behave like any other; it does not move when
the spec is re-queued, deferred or renamed, because none of those rewrite the
note; and a genuinely new return rewrites it and mints its own disposition. The
relpath also came OUT of the title, which is the dedup key — a still-marked
spec legitimately moves, and that is not a new event. The path still travels on
`specref`, where it is a pointer rather than an identity.

THE LIMIT, STATED PRECISELY THIS TIME. Round 1 claimed the limit was two
returns producing byte-identical spec text; REVIEW-A disproved it (a handback
MOVES the spec `active/` → `queued/`, so git records a touch whatever the
content). The real limit is narrower and inherent: two returns whose `##
Handback` sections are byte-identical share a token — the same lane, the same
commit span and the same reason, i.e. a return that recorded nothing new.

THE OTHER DIRECTION, DECLINED WITH A REASON. Deduping the handback arm against
an OPEN disposition for the row cannot satisfy both halves of this row's own
test list: it would suppress the second return's disposition precisely while
the first is still open, and the row requires a genuinely new handback to still
mint.

AN EXISTING GREEN TEST WAS CHANGED, DELIBERATELY AND VISIBLY.
`test_a_second_handback_of_the_same_row_mints_a_second_disposition` simulated
its second handback by committing an *unrelated* file. That stood in for a
return only while the token was the merge sha. The fixture now rewrites the
spec, which is what the shipped code does. Called out because editing a
twice-reviewed green test so one's own change passes is the move that most
deserves an independent look — and REVIEW-A did look, and agreed the new
fixture is the faithful one while flagging that the test's opening comment
still said "merge sha"; that comment is corrected.

TESTS, MUTATION-CHECKED. A bare sweep run three times against one still-marked
spec mints exactly ONE disposition; a genuinely new return still mints its own;
a re-queue, a defer-move and an untracked (uncommitted) returned spec each mint
nothing further. Reverting to the round-1 last-touch derivation fails the
lifecycle and no-history drives.
