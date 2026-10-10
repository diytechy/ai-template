# WI-834 checkpoint sitting 006 (fa795ae9)

I read the cells and chains the brief gives, the live registries, the tests the
rows cite, and the lane's arms map, which I treated as an input, not a premise.
I checked by hand what the map marks covered, with one search: every test name
in `tests/test_blackout_window.py` and `tests/test_run_devsetup.py` compared
against `docs/test/test-cases.toml`. That search found blackout behaviour
exercised by tests that no TC cites, and two arms the map calls covered that no
test exercises. Both findings are named in the lines below.

## amendment

Every row moved meaning: each adds a blackout case its old text did not have.
I would bless eight of the nine as written. LLR-300 I would not: its new
hook-denial clause traces only to SR-229, whose text demands claim admission and
nothing about denying model launches. That clause answers SR-237's "pause new
model work", and the spine-authoring rule is never to trace a clause to a parent
whose text does not demand it. LLR-300 also leaves out the close-down
instruction the hooks now inject.

- [MEANING] TC-317 Expected, Method -> verify that every guarded claim route refuses after the threshold without blocking close-out -> also verify that an armed blackout refuses every claim before the guard dial and that the main-session hook denials apply at any dial -> a new case and a new dial-independence condition; I would bless it, since its text claims only what its cited blackout tests assert and it verifies LLR-300, so it needs no change when LLR-300's parent link is fixed
- [MEANING] SR-227 Requirement, AcceptanceCriteria -> retire a retained session only when no work it has a stake in is pending -> also retire, at the first keep after a blackout window, a session with no last use or last used before that window ended, even when its chain is pending; a wrap-up adjudication may resume inside the window, and no keep-warm ping fires there -> a new retirement case that overrides chain continuity, plus two in-window rules; I would bless it, since it removes the contradiction round 001 F2 found and keeps ordinary chain continuity
- [MEANING] LLR-270 Detail -> keep_for and the keep-warm path follow the lease, drain and clear-point rules -> a BLACKOUT stage, retire_after_blackout, runs before the drain and chain rules; _warm_candidates permits no ping inside a window; take_warm_lease retires before taking a lease -> new design obligations in two functions; I would bless it, since it implements exactly SR-227's new exception, which now demands it
- [MEANING] TC-267 Expected, Method -> verify every reset rule and the store's write-whole rule with the dial on -> also verify that blackout retirement overrides a pending chain, an in-window wrap-up can resume, and keep-warm is suppressed inside the window -> three new asserted cases; I would bless it (its evidence names the five blackout tests that assert them)
- [MEANING] SR-229 Title, Requirement, AcceptanceCriteria -> where the context guard is on, admit a claim only from the unlatched lease holder, on every route but the dispatcher's own -> inside an armed window, refuse a claim on every route, including the dispatcher's, at any dial and naming the window end; outside it, the old lease and latch rule, scoped to an enabled guard -> a new refusal that reaches a route that used to be exempt and applies with the guard off; I would bless it, since it resolves round 001 F4's scoping, and its acceptance keeps the dispatcher exempt from the context guard only
- [MEANING] LLR-300 Detail -> hook responses inject the latch instruction and never refuse a tool call -> window_refusal runs before the dial on every claim route; while a window is armed the hooks deny the main session's Agent, SendMessage and model-CLI calls at any dial; one quote-aware shell reading per dialect; a bounded set of unreadable lines is denied; window_check exits nonzero inside the window -> a new refusal class and a new reader; NOT blessed: the hook-denial clause traces to SR-229 alone, whose text demands no such denial (it is SR-237's pause on new model work), and the detail does not state the close-down instruction the hooks inject at SessionStart and on the monitored events (bring each lane to its pause point, write the handoff naming its next obligation, request no relaunch), so no spine row carries that delivered behaviour; returned through the Dispositions draft below
- [MEANING] SR-230 Title, Requirement, AcceptanceCriteria -> the holder's request starts exactly one successor at any session exit -> only outside an armed window; inside it, no relaunch is requested or launched, and a pending request is cancelled and recorded as blackout -> the launch obligation narrows and a cancellation case is added; I would bless it, since it resolves round 001 F5 (the clause "and leave resumption to the owner" is a grammar slip that leaves the obligation unambiguous)
- [MEANING] LLR-301 Detail -> request_relaunch accepts the holder and an existing handoff; session_end launches on a true exit -> request_relaunch refuses inside a window, the on_blackout SessionEnd dispatch cancels and records blackout, and reopening with the context latch still set needs the owner's recorded clear -> a new refusal, a new cancellation path and a stated reopen rule; I would bless it, since it names the dispatch path as round 001 F5 asked; the reopen clause restates LLR-300's latch rule, and its own test (`test_reopening_the_same_session_with_both_drains_needs_the_owners_clear`) is cited by no TC, which the LLR-300 draft below picks up
- [MEANING] TC-318 Expected, Method -> verify that an owned request starts one successor at a true exit and survives a launch failure -> also verify that window-check refuses, no request is written inside the window, and SessionEnd cancels a pending holder request -> three new asserted cases; I would bless it (its evidence names the three blackout tests)

VERDICT: MEANING rows=9

What the re-attestation can reach: the rung is released, so I re-attest
SR-227, SR-229, SR-230, TC-267, TC-317 and TC-318. LLR-270 and LLR-301 are
blessed in this verdict but cannot be anchored in this sitting: the LLR registry
copy is refused while LLR-300's unblessed text has drifted from its anchor.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-09 leg 03): commits ce7e5b05..bd682d2, re-sat at sittings 007 and 008. No row is minted from these drafts.

```toml
title = "WI-834 spine: trace LLR-300's blackout hook pause to SR-237 and state the coordinator's close-down instruction"
workstream = "requirements"
buildtier = "medium"
sr_refs = ["SR-229", "SR-237"]
```

Carries the corrections that leave LLR-300 unblessed in sitting 006, so that a
later sitting can re-attest it. Scope:
(1) add SR-237 to LLR-300's SR-Refs, because the hook denials pause new model
work; SR-229 governs only claim admission;
(2) state in LLR-300's Detail the blackout instruction the hooks inject at
SessionStart and on the monitored events, and its cadence: bring each open lane
to its pause point, using a wrap-up adjudication where needed; write the
handoff naming each lane and its next obligation; request no relaunch; end the
session;
(3) make the two "only" clauses read as one closed list: deny the main
session's Agent, SendMessage and model-CLI calls, and the bounded unreadable
lines;
(4) cite the tests no TC cites from the TC that verifies each arm:
`test_session_start_and_the_monitored_events_tell_the_close_down`,
`test_reopening_the_same_session_with_both_drains_needs_the_owners_clear` and
`test_the_cli_names_come_from_the_route_registry`.

Out of scope: any code change. The behaviour is built and tested; only the
spine text and its citations are owed.

## first-approval

SR-237's text is ready: it is observable, closed, and its acceptance resolves
the trigger "when armed" into refusal "during the interval". Its children do not
yet cover it all:
- the coordinator's main-session pause sits in LLR-300 under SR-229 (the
  amendment section's draft);
- its retention clause is carried by LLR-270 and TC-341 under SR-227 alone, so
  no TC citing SR-237 verifies it.

Those are defects in the children's links, so they return there, and SR-237 is
approved. Five TCs return:
- TC-339 verifies LLR-300, whose new text this sitting does not bless, and a
  TC is approved only after every row it verifies.
- TC-341 omits SR-237 and does not state its in-window cases.
- TC-336 and TC-337 do not exercise arms their LLRs state. Their LLRs' text is
  sound, so the LLRs are approved and the TCs return.
- TC-342 verifies a bare-run readiness step that no LLR states. The approved
  LLR-047 still calls the `run.*` launchers "thin delegates forwarding their
  args", which `run.template.sh` and `run.template.cmd` no longer are.

The arms map's four UNCOVERED arms are LLR-270 detail unchanged since the
lane's base. They are not this lane's to answer and do not bear on these rows.

- [RETURN] TC-342 -> a bare run checks once before its menu and stops on a missing runtime; direct and list forms neither check nor pause -> its Verifies names SR-032, SR-046 and three interface rows but no LLR; neither SR's acceptance asks for a readiness step, and SR-046's approved LLR-047 says the launchers only delegate to run_menu.py, which the shipped `run.*` templates now contradict by calling `dev-setup --for-run` / `-ForRun` first -> not ready: it verifies behaviour that no requirement in its chain demands; the readiness step needs its SR acceptance and LLR first (draft below)
- [RETURN] TC-341 -> verify blackout retirement of a missing or pre-window last use, an in-window wrap-up resume, and keep-warm never refreshing a stale record -> the same assertions verify SR-237's acceptance clause ("the first retained keep after the interval retires a record last used before its end"), but its Verifies names SR-227 only, so no TC citing SR-237 verifies that clause; its Method ("then make the first keep and keep-warm calls after it") leaves out the in-window calls its own evidence makes (the wrap-up resume, no ping inside), and its Expected never states "no ping inside the window" -> not ready: one parent link missing and two cases unstated (draft below)
- [RETURN] TC-339 -> verify blackout claim refusal on both routes, the hooks' main-session denials, quote-aware reading, expandable versus literal here-bodies, and unreadable-line denial -> it verifies LLR-300, whose amended text this sitting does not bless, and its hook cases verify SR-237's pause while it names SR-229 only -> not ready: its parent text is unblessed and it lacks SR-237 (draft below; it follows the amendment section's LLR-300 draft)
- [APPROVE] TC-340 -> verify that no relaunch request is written inside the window and that a pending request is cancelled at the holder's exit -> it verifies SR-230 and LLR-301, both approved and both blessed by this sitting's amendment section, and its three tests assert exactly those cases -> ready
- [APPROVE] SR-237 -> while an armed window is open, refuse new ordinary calls and claims, admit an adjudication that brings an active claimed lane to its committed pause point, wait and retry after the window, and retire a session last used before the window's end -> parent SN-027 (approved) asks that a declared pause stop claiming and drain in-flight work without double assignment; the derived label, lens and feedback are recorded; the acceptance is observable at named boundaries -> ready; its incomplete links in LLR-300 and TC-341 are the children's to fix
- [APPROVE] LLR-316 -> blackout_at is the sole reader of the declaration: it returns the inside flag, the exclusive end and the inclusive most recent end; disabled forms; weekday starts; a midnight wrap belongs to its start weekday -> it answers SR-237's acceptance boundary clauses exactly, and TC-335 asserts each arm by name -> ready
- [APPROVE] LLR-317 -> act decides on blackout before anything is built, admits only an active-primary-claim ADJUDICATE call carrying a work item, refuses every other call and releases its retained lease, and through_blackout waits and retries -> it answers SR-237's refusal and wrap-up exception; the text matches `session_service.act` (keep_release before the raise), but no test drives a refusal with a keep, so the lease-release arm is unverified (the arms map's "covered" is wrong) -> the text is ready; the coverage returns with TC-336
- [APPROVE] LLR-318 -> wait_out_blackout waits exactly to the exclusive end, and every loop launch, interactive call and recovery probe routes a refusal through through_blackout -> it answers SR-237's "the loop waits and retries"; the text matches the three call sites in `agent_loop.py` (:1442, :2727, :2881), but no test drives any of them, only the helper -> the text is ready; the coverage returns with TC-337
- [APPROVE] LLR-319 -> claim_work refuses a new assignment inside the window, naming the end, and run keeps a pre-window assignment and waits through an idle window without spinning -> it answers SR-237's claim refusal and pause-point preservation for the dispatcher, consistent with SR-229's dispatcher clause; TC-338 asserts both arms -> ready
- [APPROVE] TC-335 -> verify the exclusive end, the inclusive last end, weekday-start intervals, disabled values and the current-declaration read -> it covers every LLR-316 arm with named tests (the weekend-daytime test it does not cite is a redundant extra, not a gap) -> ready
- [RETURN] TC-336 -> verify that only an active-claim adjudication launches, that a refused call records nothing, and that the loop retries after the window -> LLR-317 also states that a refused call releases its retained lease, and no test or clause here checks it (no refusal test passes a keep) -> not ready: an arm of the row it verifies goes unverified (draft below)
- [RETURN] TC-337 -> verify that the loop waits only inside the interval and resumes its launch afterwards -> its two tests drive `wait_out_blackout` and the `through_blackout` helper with a lambda; launch_session, run_interactive and probe_route, the three routes LLR-318 names, are never driven, so removing through_blackout from any of them passes every cited test -> not ready: the Method's "launch paths" claims coverage the evidence does not supply (draft below)
- [APPROVE] TC-338 -> verify that a new dispatcher claim refuses inside the window and that an earlier assignment waits, then resumes -> it covers both LLR-319 arms with named tests -> ready

OUTCOME: RETURN rows=13

What the approval act can reach: the act flips SR-237 and TC-340. LLR-316,
LLR-317, LLR-318 and LLR-319 are approved in this verdict but cannot be flipped
in this sitting: the LLR registry copy is refused while LLR-300's unblessed text
has drifted from its anchor. TC-335 and TC-338 then wait on their parents
(LLR-316 and LLR-319), because a child is approved only after its parent.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-09 leg 03): commits ce7e5b05..bd682d2, re-sat at sittings 007 and 008. No row is minted from these drafts.

```toml
title = "WI-834 spine: TC-339 and TC-341 verify SR-237's pause and retention clauses directly"
workstream = "requirements"
buildtier = "quick"
sr_refs = ["SR-229", "SR-227", "SR-237"]
```

Carries TC-339 and TC-341, returned at sitting 006. Scope:
(1) add SR-237 to TC-339's Verifies, once LLR-300 cites SR-237 (the amendment
section's draft);
(2) add SR-237 to TC-341's Verifies;
(3) state in TC-341's Expected and Method the in-window calls its evidence
already makes: a wrap-up resume inside the window, and no keep-warm ping inside
it.

Then re-sit both for first approval. No code or test change.

```toml
title = "WI-834 tests: drive the blackout lease release and each loop call site through a refusal"
workstream = "process"
buildtier = "medium"
sr_refs = ["SR-237"]
```

Carries TC-336 and TC-337, returned at sitting 006. Scope:
(1) a test that drives `session_service.act` inside the window with a retained
keep and asserts the lease is released before BlackoutRefused is raised
(LLR-317);
(2) tests that drive launch_session, run_interactive and probe_route
(`agent_loop.py`) through a refusal and assert each waits and retries
(LLR-318);
(3) amend TC-336 and TC-337 so their Expected, Method and Evidence state these
cases. `test_the_coordinators_adjudication_reports_a_refusal`, which no TC
cites, belongs with the coordinator route's TC.

Out of scope: changing the refusal behaviour itself. The code already does what
LLR-317 and LLR-318 state.

```toml
title = "WI-834 part C/D spine: the bare run's readiness step, dev-setup's sign-in report and the hook opt-in get their requirement rows"
workstream = "requirements"
buildtier = "medium"
sr_refs = ["SR-032", "SR-046"]
```

Carries TC-342, returned at sitting 006, and the gap it exposed. Parts C and D
shipped behaviour that no SR acceptance or LLR states, so the run launchers no
longer match approved LLR-047 ("thin delegates forwarding their args to
run_menu.py"). Scope:
(1) amend SR-046's acceptance (or the right SR) and LLR-047, or add an LLR, for
the bare run's once-per-run readiness step before the menu;
(2) state there that direct and list forms skip both the check and the closing
`pause`, and that piped menu input survives;
(3) give TC-342 that LLR in its Verifies;
(4) author the LLR and TC rows for the dev-setup readiness operation, the
sign-in report (signed in, missing, unknown, off) and the consented hook
opt-in. Their tests exist and no TC cites them:
`test_the_sign_in_is_reported_signed_in_missing_or_off`,
`test_the_sign_in_reads_unknown_without_a_runtime`,
`test_the_powershell_check_reports_the_sign_in`,
`test_a_denial_changes_no_configuration_or_credential`,
`test_the_hooks_command_reports_and_switches_on`,
`test_a_bare_run_cmd_stops_with_the_step_when_the_runtime_stays_missing`,
`test_the_sign_in_reading_is_off_while_retention_is_off`,
`test_the_sign_in_reading_names_signed_in_and_missing`,
`test_the_hook_opt_in_merges_and_keeps_existing_hooks` and
`test_the_hook_opt_in_with_no_guard_hooks_changes_nothing`.

Out of scope: behaviour changes. The launchers and dev-setup are built.

## done-when

One test bullet was swapped, and the Done-when machinery counts that as two
changes. The scope moved, and I bless the move.

The claimed bullet promised that a review-next lane "pauses with the obligation
in the handoff". The handoff is the coordinator's prose, and no kit code reads
or writes its next obligation. The current bullet promises what the code
carries:
- the close-down instruction that asks for the handoff;
- the review or rework launch refused inside the window and admitted after it.

That is the remedy dispute 003 (R2F2) ruled. The purpose stated in the Context
still holds: lanes pause at a committed point and resume after the window. The
handoff remains the resume map that ruling (f) leaves to the coordinator.

- [MOVED] a review-next lane pauses with the obligation in the handoff, and a wrap-up verdict that requires rework waits -> a scenario in which a review-next lane's handoff carries its obligation and a rework verdict's launch waits -> replaced by the item below, which no longer owes a check of a handoff's contents -> a close that satisfied the old list would owe handoff-content evidence the new one does not, so the scope narrowed; blessed, because only coordinator prose carries a handoff and the narrowing is the R2F2 remedy
- [MOVED] the close-down instruction (SessionStart and the monitored events) tells the coordinator to write a handoff naming each lane's next obligation; for a lane whose next step is a review or a rework a wrap-up verdict asked for, that launch is refused inside the window and admitted after it -> (absent at claim) -> the instruction text is pinned, and the review or rework launch is refused inside the window and admitted after it -> it adds an explicit "admitted after it" condition and names the instruction as the evidence; blessed, since it is the same pause-and-resume work the owner directed

DONE-WHEN: BLESSED changes=2 digest=sha256:0f7c7de2dd54670d

SITTING: JUDGED kinds=amendment;first-approval;done-when
