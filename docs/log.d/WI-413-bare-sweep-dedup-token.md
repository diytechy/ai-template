## 2026-08-02 — WI-413: the token names the return, not the sweep that saw it

**Summary.** Closed WI-388 REVIEW-A finding 6: a bare `intake.py sweep`, re-run
while a returned spec still carried its `## Handback` section, minted a
duplicate disposition every pass.

**The defect.** The disposition title's event token came from `after7` — the
merge sha at the slot, but symbolic `HEAD` from the by-hand recovery CLI, which
`_rev7` resolves to whatever is checked out *now*. The mint's own bookkeeping
commit already moves it, so the same return event kept getting new names. The
row's blast radius was small (visible extra queued row, cancellable, by-hand CLI
only), which is why it rode an APPROVE as a recorded finding rather than
blocking.

**The fix, and why this one.** `_return_event7` derives the token from the
return event itself — `git log -1` on the returned spec's path. One event, one
name, however many sweeps observe it. The reviewer offered a second direction,
deduping the handback arm against an OPEN disposition for the row; that was
declined because it cannot satisfy both halves of the row's own test list. It
would suppress the second return's disposition *precisely* while the first is
still open, and the row requires a genuinely new handback to still mint. The
token approach gets both, because `handback.returned_spec` rewrites the spec (a
`blockref` plus a `## Handback` note naming the lane and its commit span), so a
second return necessarily lands a new commit on that path.

**The limit, stated rather than hidden.** Two returns whose rewritten spec text
came out byte-identical would leave no new commit on the path and would share a
token. The note embeds the lane and span, which makes that unreachable in
practice — but it is the assumption the fix rests on, and it lives in
`_return_event7`'s docstring, not in someone's memory.

**An existing green test was changed, deliberately and visibly.**
`test_a_second_handback_of_the_same_row_mints_a_second_disposition` simulated
its second handback by committing an *unrelated* file and relying on the merge
sha moving. That stood in for a return only while the token *was* the merge sha;
under a token naming the return event it is not a second handback in any sense —
and it never was one in the repo either, since a real return rewrites the spec.
The fixture now does what the shipped code does. Flagged here and in the commit
message because editing a twice-reviewed green test to make one's own change
pass is the move that most deserves an independent look.

**Verification** (lane worktree, work commit `b05dca68`):

intake suite: 21 passed in 4.65s
<!-- fig: cmd="python -m pytest -q tests/test_intake.py" rev=b05dca68 -->
full suite: 1963 passed / 10 skipped / 0 failed in 337.85s (0:05:37)
<!-- fig: cmd="python -m pytest -q -n auto" rev=b05dca68 -->
mutation: reverting the token to the observer's `HEAD` fails the new
bare-sweep drive.
