## 2026-08-02 — WI-413: identify the return by its own note, not by git archaeology

**Summary.** Closed WI-388 REVIEW-A finding 6 — a bare `intake.py sweep`, re-run
while a returned spec still carried its `## Handback` section, minted a
duplicate disposition every pass. The independent REVIEW-A (cross-family, OpenAI
`gpt-5.6-sol`) returned **REWORK** against the first attempt, with 1 BLOCKING
and 2 MAJOR findings; the shipped design is the reworked one.

**The defect.** The token came from `after7`: the merge sha at the slot, but
symbolic `HEAD` from the recovery CLI, which `_rev7` resolves to whatever is
checked out *now* — and the mint's own bookkeeping commit already moved it.

**Round 1 took the reviewer's first offered direction and it did not hold.**
Deriving the token from the returned spec's last-touch commit names the last
touch for *any* reason. REVIEW-A drove three breaks: clearing a `blockref` to
re-queue moved it; moving a still-marked spec `queued/` → `deferred/` moved both
it and the path embedded in the title; untracked or shallow history had no
answer and silently fell back to the changing observer. Worst of all, `%h`
returns an *unambiguous* abbreviation that git lengthens on collision, so
truncating to seven could make two distinct returns share a token and suppress a
judgement somebody was owed — an owed judgement disappearing silently is a worse
failure than a visible duplicate.

**What shipped.** `_return_token` digests the return's own `## Handback` note —
the record `handback._note` writes, naming the lane and the commit span of the
work that did not finish. No git history is consulted, so shallow clones and
untracked trees behave like any other tree; re-queue, defer and rename do not
move it, because none of them rewrite the note; a genuinely new return does
rewrite it and mints its own disposition. The relpath also came **out** of the
title, which is the dedup key: a still-marked spec legitimately moves, and a
move is not an event. The path still travels on `specref`, as a pointer rather
than an identity.

**The limit, stated precisely this time.** Round 1 claimed the limit was two
returns producing byte-identical spec text; the reviewer disproved it — a
handback *moves* the spec, so git records a touch whatever the content. The real
limit is narrower and inherent: two returns whose `## Handback` sections are
byte-identical share a token, meaning the same lane, the same span and the same
reason — a return that recorded nothing new.

**A green test was changed, deliberately and visibly.** The existing
second-handback test simulated its second return by committing an *unrelated*
file. Under a token naming the event that is not a second handback in any sense,
and it never was one in the repo either. The fixture now does what the shipped
code does. It was flagged to the reviewer rather than left in the diff; the
reviewer agreed the new fixture is the faithful one and caught that the test's
opening comment still said "merge sha", which is now corrected.

**Verification** (lane worktree, round-2 rework):

intake suite: 23 passed in 5.05s
<!-- fig: cmd="python -m pytest -q tests/test_intake.py" rev=b05dca68 -->
full suite: 1969 passed / 6 skipped / 0 failed in 330.63s (0:05:30)
<!-- fig: cmd="python -m pytest -q -n auto" rev=b05dca68 -->
mutation: reverting to the round-1 last-touch derivation fails both the
lifecycle drive (re-queue / defer-move) and the no-history drive.
