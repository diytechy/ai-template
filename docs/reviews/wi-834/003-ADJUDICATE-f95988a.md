# WI-834 adjudication 003: dispute R2F2 (range a2c94eed..9bc1eb2a)

Scope bound: PROCESS.md §6 "Review threat model". R2F2 needs no compromised
host. It is an ordinary coverage claim against the lane's own spec, so it is in
scope.

## R2F2: no separate review-next / handoff scenario

**What holds.** The reviewer quotes the spec correctly. The Part B test list in
`docs/work/active/wi-834/WI-834-...md` says "a review-next lane pauses with the
obligation in the handoff". At 9bc1eb2a no test writes or reads a handoff for a
blackout pause, and none builds a lane whose next step is a review. The
instruction pin, `test_session_start_and_the_monitored_events_tell_the_close_down`
(:481), only checks that the injected text contains `next obligation`.

**What the extra scenario would exercise.** I read the code that would run.

- In `session_service.launch_refusal`, the blackout decision depends on three
  things only: the clock, `call.role`, and the primary checkout's claim status
  for `call.wi` (`claim_active`). It does not read the lane's commits, its review
  files or any handoff.
- So a review-next lane and a rework lane go down the same refusal and admission
  path. The paths are already covered:
  - `test_a_review_next_or_rework_launch_is_refused_for_an_active_claim`
    covers the REVIEW refusal for an active claim.
  - `test_a_wrap_up_verdict_asking_for_rework_leaves_the_rework_waiting`
    covers the committed-evidence lane, BUILD and REVIEW refused inside the
    window, and admission after it.
- No kit code reads a handoff's next obligation:
  - `coordinator_guard` uses a handoff for only one thing: its fenced session
    prompt, read when a relaunch is requested (`session_prompt`, `_promptless`).
  - `request_relaunch` is refused inside the window, and that refusal is tested
    separately.
  - The spec's own resume path is the owner reopening the session or releasing
    the lease. It parses no handoff.
- The coordinator writes the handoff as prose. The one part the kit's code
  carries is the instruction that asks for it, and that is pinned.

**Weighing it.** The scenario R2F2 asks for would reach no line of code the two
existing tests don't already reach. Its handoff assertions would check a file
the test itself wrote. It would catch no regression a current test misses. I ran
the relevant subset (`-k "rework or review_next or close_down"`): 5 passed. The
gap is real only as a mismatch with the wording of the spec's test list. Adding
a near-tautological test costs more than that mismatch. The right fix is
outside this ruling: reword or scope that test-list bullet at the lane's spine
checkpoint so it promises what the kit's code can carry (the pinned instruction
plus the role-based refusal and admission). One small gap, noted but not ruled:
after the window, the wrap-up test checks that BUILD is admitted but not REVIEW.
Both go through the same `launch_refusal` branch.

RULING: R2F2 DISMISS not-worth-cost the blackout refusal reads only role, WI and primary claim status, which the existing REVIEW-refusal and committed-lane wrap-up tests already cover, and no kit code reads a handoff's next obligation, so the asked-for scenario would assert a handoff file the test wrote itself and add no detection power; the fix is rewording the spec's test-list bullet at the checkpoint, not adding a test
