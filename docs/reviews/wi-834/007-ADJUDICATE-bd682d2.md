# WI-834 checkpoint sitting 007 (bd682d22)

This sitting re-judges the rows sitting 006 returned, now answered in
ce7e5b05..bd682d22. Those commits changed only tests and spine rows, not
shipped code.

What I observed:
- I ran the four affected suites: `tests/test_blackout_window.py`,
  `tests/test_run_devsetup.py`, `tests/test_coordinator_guard.py` and
  `tests/test_coordinator_adjudicate.py`. Result: `222 passed, 4 skipped`.
- The four skips are the POSIX-only fake-interpreter test and the three
  pseudo-terminal consent tests, which cannot run on this Windows host. I read
  those tests rather than ran them.
- I checked the new LLR text against `coordinator_guard.py`,
  `dev-setup.template.sh` and the `run.*` templates.

Sitting 006's returns are answered: the lease-release test, the three loop
routes driven whole, the part C/D rows and TC-342's LLR link. Two new defects
came with the answers. Both are text: LLR-300's close-down cadence and SR-237's
reworded retention clause.

## amendment

Every row moved meaning. Six I would bless; two I would not.

- [MEANING] SR-046 AcceptanceCriteria -> the listing, direct call, menu, empty declaration, descriptions, delegate launchers and scaffold -> also: a no-argument launch runs its readiness step once from the root before the menu and exits with guidance while the runtime stays missing; direct and discovery launches skip both the step and the closing pause; piped selection survives the step -> new acceptance cases; I would bless it, since the step is how an interactive operator reaches capabilities that can run, and the skip keeps the direct and discovery callers non-interactive, which are SR-046's own three caller kinds
- [MEANING] LLR-047 Detail -> the run.* launchers are thin delegates forwarding their args to run_menu.py -> the no-argument launchers cd to the root and run dev-setup's --for-run/-ForRun once before the menu, and a nonzero result leaves the menu unopened; direct and --list forms bypass it and Windows' closing pause; run.command delegates to run.sh, so the step runs once -> the launchers' design changed; I would bless it, since it matches `run.template.sh`/`.cmd` and resolves the contradiction sitting 006 found
- [MEANING] LLR-270 Detail -> no blackout stage -> retire_after_blackout before the drain and chain rules, no ping inside the window, and retirement before a keep-warm lease -> new design obligations; I would bless it (this text is unchanged since sitting 006 blessed it; it is still unanchored because the LLR registry copy is held)
- [MEANING] TC-321 Expected, Method -> verify the IF-284 outcomes, the reservation and the default route -> also verify that a blackout refusal on the coordinator's route is reported, releases its reservation, and neither waits nor launches -> a new asserted case; I would bless it (`test_the_coordinators_adjudication_reports_a_refusal` asserts exactly that, and it falls under LLR-306's pre-launch refusal releasing only what the call reserved)
- [MEANING] LLR-300 Detail -> the guard's hooks never refuse a tool call -> blackout claim refusal before the dial, a closed denial list, a quote-aware reading, and a close-down instruction "at SessionStart and on monitored events ... at the first event of a window and every twentieth thereafter" -> a new refusal class and a new instruction; NOT blessed: the cadence sentence puts SessionStart inside the every-twentieth count, but `_close_down` tells the close-down at EVERY SessionStart, and `_reminder_due` counts only monitored events, per session per window. So TC-339's own evidence (`test_session_start_and_the_monitored_events_tell_the_close_down`: told at SessionStart, then at the FIRST Stop, then the twenty-first) fails an implementation built to this text, and a session resumed mid-window would go untold. Returned through the Dispositions draft below; the SR-237 parent link and the closed list sitting 006 asked for are now right
- [MEANING] TC-316 Expected, Method -> verify that the latch holds until a declared recovery -> also verify that reopening after the blackout with the context latch set still needs the owner's recorded clear -> a new asserted case; I would bless it (it cites `test_reopening_the_same_session_with_both_drains_needs_the_owners_clear`, which asserts it)
- [MEANING] LLR-301 Detail -> request_relaunch and session_end apply at any time -> refusal inside the window, on_blackout cancellation, and the stated reopen rule -> as ruled at sitting 006; I would bless it (unchanged since then, and still unanchored for the same reason)
- [MEANING] SR-237 Requirement -> "pause new model work until the window ends ... except that an adjudication needed to bring an active lane to that point may proceed, and shall resume eligible work after the window WITHOUT RETAINING a session whose prior use predates that window's end" -> "... admitting only an adjudication needed ..., resuming eligible work after the window, and NOT RETAINING a session whose prior use predates that window's end" -> the admission clause now reads as an obligation to admit, not a permission. And the no-retention clause has lost its anchor to the post-window resume: inside the window, every retained session's prior use predates the window's end. NOT blessed: read as written, it now forbids the in-window wrap-up resume that approved SR-227 ("a wrap-up adjudication inside the window may resume its retained session") and LLR-270 permit. That restores the cross-row contradiction round 001 F2 removed. The approved text was coherent. Returned through the Dispositions draft below

VERDICT: MEANING rows=8

What the re-attestation can reach: it re-attests TC-316 and TC-321. Four
blessed rows stay unanchored:
- SR-046, because the SR registry copy is held by SR-237's unblessed drift;
- LLR-047, LLR-270 and LLR-301, because the LLR registry copy is held by
  LLR-300's.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-09 leg 03): commit ff1d291e, re-sat at sitting 008. No row is minted from these drafts.

```toml
title = "WI-834 spine: LLR-300 states the close-down cadence the hooks implement, and SR-237 keeps its no-retention clause after the window"
workstream = "requirements"
buildtier = "quick"
sr_refs = ["SR-229", "SR-237"]
```

Carries LLR-300 and SR-237, left unblessed at sitting 007. Text only; the code
and tests already do the right thing. Scope:
(1) LLR-300's cadence sentence: SessionStart injects the close-down whenever
it fires inside a window. Each main session's monitored events inject it at
that session's first monitored event in the window and every twentieth
thereafter, counted per session per window.
(2) SR-237's Requirement: re-anchor "not retaining a session whose prior use
predates that window's end" to the resume after the window, as the approved
text had it ("resume eligible work after the window without retaining ..."), so
it cannot read as forbidding the in-window wrap-up resume SR-227 permits.
Whether the adjudication clause is a permission or an obligation should be
deliberate.
(3) Re-sit both, with TC-339's matching correction (the first-approval
section's draft).

## first-approval

Most rows are now ready. Two kinds of block remain:
- TC-339 returns, because the LLR-300 text it verifies is not blessed and its
  Method repeats the same cadence misstatement.
- LLR-316 to LLR-322 are approved on merit but cannot be flipped in this
  sitting: flipping them copies the LLR registry, which LLR-300's unblessed
  drift holds. TC-335 to TC-338 and TC-343 to TC-345 then wait on those
  parents, because a child is approved only after its parent.

This sitting's flips are TC-341 and TC-342. Their parents are all
Approved-status rows: LLR-270, LLR-047, SR-227, SR-237, SR-032 and SR-046.

Observation, not a return: the content of dev-setup's `claude setup-token`
consent text sits under LLR-320's generic "offers each missing setup item" and
no row states it. `test_a_denial_changes_no_configuration_or_credential`
declines it and asserts nothing changed. A later spine pass may give it its own
clause.

- [APPROVE] LLR-320 -> --for-run/-ForRun reports first, offers missing items only at an interactive terminal, offers nothing and keeps menu input without one, exits 0 when ready and otherwise 1 with the step; --check reports only, writes nothing, exits 0 -> parent SR-032 asks that dev-setup run to a green setup, and this is its consent-first path to one; the text matches `dev-setup.template.sh`; TC-343 covers each arm with named tests -> ready
- [APPROVE] LLR-321 -> the report omits the sign-in item with retention off; otherwise signed-in only for a readable token, missing, or unknown without a runtime, the rest still reported, and the token never printed or stored -> SR-032's workstation report; matches the `SIGNIN` block (no line at dial 0, as `test_the_sign_in_is_reported_signed_in_missing_or_off` asserts); TC-344 adds the canary test for non-disclosure -> ready
- [APPROVE] LLR-322 -> with the example's guard hooks off, interactive consent merges them in, keeping existing hooks and settings; a decline changes nothing; an example with no guard hooks changes nothing -> SR-032's opt-in setup step; matches `offer_hooks` and `enable_hooks`; TC-345 covers all three arms -> ready
- [APPROVE] TC-342 -> verify that a bare run checks once from the root before the menu and stops on a missing runtime, and that direct and list forms neither check nor pause -> it now verifies LLR-047, whose amended detail states exactly this, under SR-046's amended acceptance; its eight tests cover both launcher families, the piped input and this repo's menu -> ready (sitting 006's missing-LLR finding is answered)
- [APPROVE] TC-343 -> verify report-before-offer, consent at a terminal, nothing offered and input kept without one, the missing-runtime exit, and a read-only standalone check -> it covers every LLR-320 arm with named tests (the pseudo-terminal ones run on POSIX hosts only, a statement about where they run, not about the text) -> ready
- [APPROVE] TC-344 -> verify the sign-in item is off or omitted at dial 0, the signed-in, missing and unknown readings on both families, and no token disclosure -> it covers every LLR-321 arm; "off" in its Expected reads as the item's absence, which is what the test asserts -> ready
- [APPROVE] TC-345 -> verify that consent merges the guard hooks while keeping others, a decline changes nothing, and a guard-less example changes nothing -> it covers every LLR-322 arm -> ready
- [APPROVE] TC-341 -> verify blackout retirement of a missing or pre-window use, an in-window wrap-up resume, no ping inside the window, and no stale refresh -> sitting 006's return is answered: SR-237 is in Verifies, and the in-window calls are stated in the Expected and the Method; the clause it verifies, SR-237's unchanged acceptance, is consistent with SR-227 -> ready
- [RETURN] TC-339 -> verify blackout claim refusal, the closed hook-denial list, the shell reading, the close-down instruction "at the first window event and every twentieth thereafter", and registry-sourced CLI names -> it verifies LLR-300, whose amended text this sitting does not bless, and its Method carries the same cadence misstatement: the test it cites tells at SessionStart AND at the first monitored event -> not ready (draft below)
- [APPROVE] LLR-316 -> blackout_at is the sole reader: inside flag, exclusive end, inclusive last end, disabled forms, weekday starts, wraps to the start weekday -> unchanged since sitting 006 approved it; TC-335 covers it -> ready
- [APPROVE] LLR-317 -> act decides blackout first, admits only an active-claim ADJUDICATE call, refuses the rest and releases their lease; through_blackout waits and retries -> unchanged; the lease arm is now verified by `test_a_refused_retained_call_releases_its_lease` (the lease is gone and the session record is kept after the refusal) -> ready
- [APPROVE] LLR-318 -> wait_out_blackout waits only inside the window; the loop launch, interactive call and recovery probe each retry through through_blackout -> unchanged; `test_each_loop_route_waits_out_a_refused_launch_and_retries` drives launch_session, run_interactive and probe_route whole, with only the outer runner substituted, each waiting 5 h then launching once at the end -> ready
- [APPROVE] LLR-319 -> the dispatcher refuses a new assignment inside the window and keeps a pre-window one, waiting without spinning -> unchanged; TC-338 covers it -> ready
- [APPROVE] TC-335 -> verify the window function's boundaries -> unchanged since sitting 006 approved it -> ready
- [APPROVE] TC-336 -> verify only an active-claim adjudication launches, a refusal records nothing, the loop retries, and a refused retained call releases its lease -> sitting 006's return is answered by the new clause and its test -> ready
- [APPROVE] TC-337 -> verify the loop waits only inside the window, and each of its three refusal routes retries once afterwards -> sitting 006's return is answered: the Method now names, and its evidence drives, all three routes -> ready
- [APPROVE] TC-338 -> verify dispatcher refusal and the held assignment -> unchanged since sitting 006 -> ready

OUTCOME: RETURN rows=17

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-09 leg 03): commit ff1d291e, re-sat at sitting 008. No row is minted from these drafts.

```toml
title = "WI-834 spine: TC-339 states the close-down cadence its test asserts"
workstream = "requirements"
buildtier = "quick"
sr_refs = ["SR-229", "SR-237"]
```

Carries TC-339, returned at sitting 007. Scope: correct TC-339's Expected and
Method to the cadence `test_session_start_and_the_monitored_events_tell_the_close_down`
asserts. The instruction comes at every SessionStart inside a window, then at
the main session's first monitored event and every twentieth thereafter. Re-sit
TC-339 for first approval once the amendment section's draft has fixed
LLR-300's matching sentence. Text only.

SITTING: JUDGED kinds=amendment;first-approval
