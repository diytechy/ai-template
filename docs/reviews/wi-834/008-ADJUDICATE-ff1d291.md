# WI-834 checkpoint sitting 008 (ff1d291e)

This sitting answers sitting 007's three returns. The answering commit,
ff1d291e, changes exactly three cells and no code:
- LLR-300's Detail;
- SR-237's Requirement;
- TC-339's Expected and Method.

I re-ran `tests/test_blackout_window.py` and `tests/test_run_devsetup.py`:
`93 passed, 4 skipped`. The skips are the same four as at sitting 007: one
POSIX-only test and three that need a pseudo-terminal, which this Windows host
lacks. I re-read the cadence code against the new text:
- `_close_down` tells the close-down at every SessionStart, for the main
  session only (`on_blackout` returns early for a subagent payload);
- `_reminder_due` counts monitored events per session, keyed by the window's
  end, and tells at counts 0, 20, 40 and so on.

The rows sitting 007 blessed or approved but could not anchor are carried here
unchanged, so this act can anchor them.

## amendment

- [MEANING] SR-046 AcceptanceCriteria -> listing, direct, menu, empty declaration, descriptions, delegate launchers, scaffold -> also: the readiness step runs once from the root before a no-argument menu, with an exit and guidance while the runtime stays missing; direct and discovery launches skip the step and any closing pause; piped selection survives -> new acceptance cases; blessed (unchanged since sitting 007 blessed it)
- [MEANING] LLR-047 Detail -> the run.* launchers are thin delegates -> the no-argument launchers cd to the root and run --for-run/-ForRun once before the menu; direct and --list bypass it and Windows' pause; run.command delegates once -> the launchers' design changed; blessed (unchanged since sitting 007; matches the run.* templates)
- [MEANING] LLR-270 Detail -> no blackout stage -> retire_after_blackout before the drain and chain rules, no ping inside the window, and retirement before a keep-warm lease -> new design obligations; blessed (unchanged since sittings 006 and 007 blessed it)
- [MEANING] LLR-300 Detail -> hooks never refuse a tool call -> blackout claim refusal before the dial, the closed denial list, the quote-aware reading, and the close-down instruction "at every SessionStart inside a window ... and each main session's ... first monitored event in the window and every twentieth thereafter, counted per session per window" -> a new refusal class and a new instruction; blessed: the cadence sentence now matches `_close_down` and `_reminder_due`, which answers sitting 007's return, and its SR-237 parent link and closed list stand as sitting 006 asked
- [MEANING] LLR-301 Detail -> request_relaunch and session_end apply at any time -> refusal inside the window, on_blackout cancellation, and the reopen rule -> as ruled at sitting 006; blessed (unchanged)
- [CLARITY] SR-237 Requirement -> pause new model work until the window ends, preserve each already claimed lane at its committed pause point, permit the adjudication that brings an active lane there, and resume eligible work after the window without retaining a session whose prior use predates the window's end -> "pause ... until the window ends, preserving each claimed lane at its committed pause point and starting no model work inside the window except an adjudication needed to bring an active lane to that point, then resume eligible work after the window without retaining a session whose prior use predates that window's end" -> the same obligation:
  - the adjudication is still a permitted exception, not an obligation to admit;
  - "starting no model work" restates "pause new model work", and leaves in-flight calls alone as before;
  - dropping "already" changes no set of lanes, since every claim inside a window is refused;
  - the no-retention clause is once more tied to the resume after the window, as in the anchored text.

  This answers sitting 007's return, and the row is re-anchored with the rest.

VERDICT: MEANING rows=6

The act re-attests all six: SR-046 and SR-237 in the SR registry; LLR-047,
LLR-270, LLR-300 and LLR-301 in the LLR registry.

## first-approval

Every row is ready. The only blocks at sittings 006 and 007 were LLR-300's text
and the TC-339 that verifies it, and both are answered. Once the amendment act
anchors the LLR registry, the LLR rows flip with their TCs in one act.

- [APPROVE] LLR-320 -> --for-run/-ForRun reports first, offers missing items only at a terminal, offers nothing and keeps menu input without one, exits 0 when ready and otherwise 1 with the step; --check is read-only and exits 0 -> SR-032's consent-first path to a green setup; matches `dev-setup.template.sh`; TC-343 covers every arm -> ready (as ruled at sitting 007)
- [APPROVE] LLR-321 -> the sign-in item is omitted at dial 0; otherwise signed-in, missing or unknown, the rest of the report still runs, and the token is never printed or stored -> SR-032's workstation report; matches the `SIGNIN` block; TC-344 covers every arm, including the canary -> ready
- [APPROVE] LLR-322 -> consent merges the guard hooks while keeping others; a decline or a guard-less example changes nothing -> SR-032's opt-in; matches `offer_hooks` and `enable_hooks`; TC-345 covers every arm -> ready
- [APPROVE] TC-343 -> verify report-before-offer, consent at a terminal, nothing offered and input kept without one, the missing-runtime exit, and a read-only standalone check -> it covers LLR-320 (its pseudo-terminal cases run on POSIX hosts) -> ready
- [APPROVE] TC-344 -> verify the omitted item at dial 0, the signed-in, missing and unknown readings on both families, and no token disclosure -> it covers LLR-321 -> ready
- [APPROVE] TC-345 -> verify the consented merge, the decline and the guard-less example -> it covers LLR-322 -> ready
- [APPROVE] TC-339 -> verify blackout claim refusal, the closed hook-denial list, the shell reading, the close-down at every SessionStart and at each main session's first monitored event and every twentieth, and registry-sourced CLI names -> its Expected and Method now state the cadence `test_session_start_and_the_monitored_events_tell_the_close_down` asserts (SessionStart, then the first Stop, then the twenty-first), and they verify LLR-300's now-blessed text under SR-229 and SR-237 -> ready (sitting 007's return answered)
- [APPROVE] LLR-316 -> blackout_at, the sole reader of the window -> unchanged since sittings 006 and 007; TC-335 -> ready
- [APPROVE] LLR-317 -> act's blackout refusal, the active-claim wrap-up exception, the lease release and through_blackout -> unchanged; TC-336 covers every arm -> ready
- [APPROVE] LLR-318 -> the loop's wait, and retry on each of its three routes -> unchanged; TC-337 drives each route whole -> ready
- [APPROVE] LLR-319 -> the dispatcher's refusal and the held assignment -> unchanged; TC-338 -> ready
- [APPROVE] TC-335 -> verify the window function's boundaries -> unchanged -> ready
- [APPROVE] TC-336 -> verify the refusal, the exception, the recording, the retry and the lease release -> unchanged since sitting 007 -> ready
- [APPROVE] TC-337 -> verify the wait and each route's single retry after the window -> unchanged since sitting 007 -> ready
- [APPROVE] TC-338 -> verify dispatcher refusal and the held assignment -> unchanged -> ready

OUTCOME: APPROVE rows=15

SITTING: JUDGED kinds=amendment;first-approval
