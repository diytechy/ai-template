WI-834 spec NOT YET SOUND

Reviewed the complete amended working-tree spec and its diff. Owner rulings (a)–(g) are treated as decisions, not defects. The blockers concern how Done-when implements them.

1. **Lazy retirement — MAJOR: the historical window boundary is undefined.**

   The record already supports this: `last_used` and `last_used_epoch` are written after calls, and `reset_reason` accepts a string such as `blackout` ([session_keep.py:783](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:783), [session_keep.py:525](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:525)). Lazy retirement needs no daemon.

   However, `blackout_wake` returns only the remaining duration of a window active **now**, or `None`; it cannot supply “the most recent window’s end” after the window ([agent_common.py:569](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:569)). WI-834 requires that historical calculation while declaring this function the only window reader ([WI-834:108](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:108), [WI-834:139](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:139)).

   Wrap windows also expose an existing inconsistency: the docstring says “honored on its start weekday,” but the implementation excludes weekends using **the current date** before calculating the interval ([agent_common.py:576](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:576)). A read-only check confirmed `22:00-02:00` blocks Friday 23:00, permits Saturday 01:00, and blocks Monday 01:00.

   **Smallest spec change:** define one shared interval calculation used by current admission and historical retirement. State its weekend/wrap semantics, strict comparison at the end, missing-timestamp behavior, and whether a changed dial applies retrospectively or only prospectively. A wrap-up ending inside the window must retire after its end; a call ending after the window does not meet the stated last-use test. Add boundary fixtures for those cases and dial changes.

2. **Enforcement sites — BLOCKER: caller exceptions and command coverage are not sufficiently defined.**

   **(a) Service launch refusal.** The service cannot distinguish the loop from the coordinator today. `Call.route_id` is a roster identity, and `Call` has no caller-origin or wrap-up eligibility field ([session_service.py:98](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:98)). The loop supplies the same ordinary `Call` structure ([agent_loop.py:2636](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:2636)). Implementing “any route but the loop’s” requires a new discriminator or an implicit heuristic.

   The exemption also leaves a real admission gap: the loop checks blackout at iteration entry, then routes and launches later without rechecking ([agent_loop.py:3274](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:3274), [agent_loop.py:3312](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:3312)). Its interactive route and recovery probes call the service directly ([agent_loop.py:1390](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:1390), [agent_loop.py:2790](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:2790)).

   **Smallest spec change:** make the service’s launch boundary apply to **every caller**. Specify a refusal result that the loop handles by waiting and retrying. Define wrap-up eligibility from a named WI/lane and recorded pending adjudication, rather than adding a caller-selected bypass flag.

   **(b) Hook denial.** The input is sufficient for direct `Agent` and shell-call inspection: Claude documents `tool_name` and `tool_input.command`, plus JSON denial with exit 0. Existing wiring already invokes the hook for every PreToolUse event ([settings.json:26](C:/Projects/ai-template/.claude/settings.json:26), [Claude hooks reference](https://code.claude.com/docs/en/hooks#pretooluse)).

   But deriving executable names does not establish shell semantics. The repository’s template tokenizer identifies command tokens; it does not inspect scripts or recursively interpret wrappers ([agent_session.py:72](C:/Projects/ai-template/project-trajectory/scripts/agent_session.py:72)). A `bash sol_review.sh` command does not expose the model executable as its first token; `timeout`, environment assignments, shell chains and substitutions require an explicitly defined grammar.

   “Exactly these calls and no other” also leaves resumed subagent work unblocked: Claude documents `SendMessage` resuming a completed subagent without an `Agent` invocation. On supported Windows configurations, model commands may use `PowerShell` instead of Bash. These are documented launch paths, not hypothetical evasions ([subagent resume documentation](https://code.claude.com/docs/en/sub-agents#resume-subagents), [shell hook inputs](https://code.claude.com/docs/en/hooks#pretooluse)).

   **Smallest spec change:** enumerate the supported direct shell forms and require script wrappers to use the guarded service. Cover model-starting subagent resumes and supported shell tools. Amend IF-274’s input fields alongside IF-275’s denial response. Describe the hook as supervision within that coverage, not complete inspection of arbitrary shell programs.

   **(c) Claim refusal — NOTE: feasible without a new route flag.** `integrate.claim` already distinguishes the live dispatcher through `dispatch_lock_held` and combines the guarded refusal before the normal claim ladder ([integrate.py:744](C:/Projects/ai-template/project-trajectory/scripts/integrate.py:744), [integrate.py:804](C:/Projects/ai-template/project-trajectory/scripts/integrate.py:804)). Move the blackout refusal ahead of `claim_refusal`’s context-guard early return ([coordinator_guard.py:484](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:484)). Outside blackout, preserve the existing context-guard decision.

3. **Coordinator close-down — MAJOR: lease recovery, latch cause and pending relaunch behavior are missing.**

   Blackout currently cannot reach the hook with the context guard off: `hook` returns immediately, while monitored calls additionally require the lease holder’s identity ([coordinator_guard.py:669](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:669), [coordinator_guard.py:532](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:532)). Simply removing that return is insufficient: `latch_reading` compares occupancy against the threshold, so threshold zero would latch on any known positive occupancy ([coordinator_guard.py:466](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:466)).

   The lease still provides useful coordinator identity with the context guard off, but its lifecycle must be declared. Contrary to the question’s premise, **not every entry point is disabled**: `take`, `release` and `clear` currently operate independently of the dial ([coordinator_guard.py:382](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:382)). Hooks do not automatically identify an ordinary newly started session as the coordinator.

   Manual resume is also incomplete. Same-holder `take` preserves the latch; another holder is refused. SessionEnd without a relaunch request leaves the lease intact ([coordinator_guard.py:392](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:392), [coordinator_guard.py:792](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:792)). Thus resuming the same session needs an owner clear; starting a fresh coordinator needs owner release followed by take. Elapsed time clears neither.

   Finally, a relaunch request written **before** blackout still launches at exit: neither request creation nor SessionEnd checks blackout ([coordinator_guard.py:714](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:714), [coordinator_guard.py:776](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:776)). Existing instructions explicitly request relaunch for every drain ([coordinator_guard.py:143](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:143)).

   **Smallest spec change:** define blackout as a distinct drain cause, specify coordinator identification when only blackout is armed, and state the owner’s same-session/fresh-session recovery procedure. Suppress both new and already-pending automatic relaunch requests across the blackout, with a stated disposition for pending requests. Amend the existing close-out recipe, which currently says the procedure is identical every time and always requests relaunch ([session-protocol:175](C:/Projects/ai-template/project-trajectory/skills/session-protocol/SKILL.md:175)).

   **NOTE:** staying `active` with the matching branch and worktree does not introduce an OI-70 held state. The registry expressly defines active as claimed ([work/README.md:70](C:/Projects/ai-template/docs/work/README.md:70)). Clarify that a scheduled wait preserves the claim; a human-owed stop still uses the partial-close procedure.

   The wrap-up exception has the same missing eligibility proof identified in 2(a); service role `ADJUDICATE` alone does not establish “brings an open lane to its pause point.”

**3b. dev-setup consent — MAJOR: buildable, but denial and launcher scope need correction.**

The consent shape fits: check mode reports and exits before mutation; baseline/full offer individual commands with default-no consent. The Windows `.cmd` delegates to the PowerShell implementation ([dev-setup.sh:190](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.sh:190), [dev-setup.ps1:133](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.ps1:133), [dev-setup.cmd:20](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.cmd:20)).

Detection without a model call is supported by `claude auth status`; its JSON identifies the config directory and authentication method. Claude documents directory-specific credentials on Windows/Linux and directory-specific Keychain entries on macOS. Checking only for `.credentials.json` would therefore be insufficient ([CLI reference](https://code.claude.com/docs/en/cli-reference#cli-commands), [credential management](https://code.claude.com/docs/en/authentication#credential-management)).

Two spec gaps remain:

- **Denial:** WI-834 says retention “stays off,” yet enables the declared dial at 55 and requires denial to change nothing ([WI-834:159](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:159), [WI-834:174](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:174)). Today retention is enabled solely by that dial; no sign-in condition participates ([session_keep.py:135](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:135)). **Change:** define denial as leaving configuration and credentials unchanged, and specify the resulting launch/preflight behavior when retention is requested but authentication is missing. Distinguish absent, authenticated and unknown/error results.
- **Launcher scope:** shipped `run.*` are product launchers; `run.template.cmd` delegates to `run_menu.py`, not `agent_common.preflight` ([run.template.cmd:3](C:/Projects/ai-template/project-trajectory/scripts/run.template.cmd:3), [run.template.cmd:28](C:/Projects/ai-template/project-trajectory/scripts/run.template.cmd:28)). **Change:** name downstream `agent-resume.*` and the shared model-launch boundary. If a product-menu action starts an agent, apply the check to that action. Editing shipped templates is within the meta-repo’s scope; making ordinary product launches depend on adjudicator sign-in is the misplaced coupling.

Also require check mode to resolve the home without creating it: the existing `dedicated_home_env` creates directories ([session_keep.py:343](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:343)).

4. **In-flight completion versus pause points — MAJOR: the review-next case lacks an acceptance definition.**

   Rulings (d) and (f) can coexist: finish the already-running call, record its result, and permit only the eligible wrap-up adjudication. But Done-when says to bring *every* lane to its step record without defining what is recorded when the next obligation is REVIEW-A, REVIEW-B, rework or another prohibited launch ([WI-834:122](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:122), [WI-834:129](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:129)).

   **Smallest spec change:** explicitly allow a pause after the finished call’s evidence is committed, with the next review/rework obligation pending in the handoff. Do not require completing the review cycle to reach the pause point. Add a review-next fixture and a wrap-up adjudication whose verdict requires work that must wait.

   **MINOR:** “bounded by its existing session timeout, on either route” overstates the current guarantee. The root launcher supplies a default wall bound, but attached calls ignore their timeout and the interactive coordinator has no guard-enforced wall deadline ([agent-resume.cmd:76](C:/Projects/ai-template/agent-resume.cmd:76), [session_service.py:135](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:135)). Qualify this as retaining each call’s existing bounds; describe coordinator shutdown as encouraged, matching ruling (f).

5. **One path — MAJOR: absorption is plausible, but the temporary entry’s contract is incomplete.**

   WI-801 already requires only `ask` to launch or draw routes, and directs the hand recipe to `ask.py` ([WI-801:35](C:/Projects/ai-template/docs/work/queued/WI-801-ask-one-entry-point.md:35), [WI-801:54](C:/Projects/ai-template/docs/work/queued/WI-801-ask-one-entry-point.md:54)). WI-834 can precede it cleanly if the temporary entry only composes existing service operations.

   “Composed brief file and route” is insufficient input today. `plan_keep` requires a retained **brief class**, family and route; the loop also supplies WI identity, registry rows, governing template identity and a lease duration tied to the call deadline ([session_service.py:431](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:431), [agent_loop.py:2590](C:/Projects/ai-template/project-trajectory/scripts/agent_loop.py:2590)). These affect whether retention applies and whether retirement is safe.

   **Smallest spec change:** define an adjudication request carrying those identities, or identify their authoritative derivation. Extract the loop’s request-to-keep composition once. Require WI-801 to delete the temporary CLI and migrate its callers/tests; “absorbs it” should not leave a compatibility launcher indefinitely.

   **NOTE:** resumed Claude subagents would indeed be a second retention mechanism: they bypass the kit’s `Keep` planning, dedicated-home overlay and bookkeeping ([session_service.py:164](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:164), [session_service.py:229](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:229)). That is sufficient justification.

   **MINOR:** remove “lost when the coordinator session ends.” Claude documents restoring subagents after restarting and resuming the same parent session. The accurate objection is that this mechanism is outside the kit’s retention contract ([WI-834:60](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:60), [subagent persistence](https://code.claude.com/docs/en/sub-agents#resume-subagents)).

6. **Spine and shipping — MAJOR: the amendment list omits affected contracts.**

   SR-227/LLR-270 are correct retention homes. But SR-229 explicitly conditions its entire lease/latch behavior on the context guard, and its acceptance says guard-off admission reads no state ([system-requirements.toml:1739](C:/Projects/ai-template/docs/requirements/system-requirements.toml:1739)). LLR-300 repeats guard-off and never-deny semantics ([low-level-requirements.toml:3163](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:3163)). IF-271 promises unconditional admission at dial zero ([coordinator_guard.py:45](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:45)).

   Preventing previously requested relaunch also touches SR-230/LLR-301, whose existing obligation is exactly one successor after the holder exits with a valid request ([system-requirements.toml:1753](C:/Projects/ai-template/docs/requirements/system-requirements.toml:1753), [low-level-requirements.toml:3175](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:3175)).

   **Smallest spec change:** explicitly include LLR-300, IF-271, IF-274, the service refusal contract IF-246, and SR-230/LLR-301 where relaunch behavior changes. Update the relevant runtime flow in the same change, as PROCESS requires ([PROCESS.md:410](C:/Projects/ai-template/project-trajectory/PROCESS.md:410)). Keep IF-278’s owner/token transfer rule intact.

   **MAJOR:** the threshold test contradicts current retention semantics. WI-834 requires a session reaching the dial to reset before its next call. Existing code drains it and continues related chains until a clear point ([WI-834:170](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:170), [session_keep.py:530](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:530), [system-requirements.toml:1712](C:/Projects/ai-template/docs/requirements/system-requirements.toml:1712)). **Change:** require threshold draining followed by clear-point retirement; make blackout retirement the explicit exception that overrides pending-chain continuity.

   **NOTE:** no concrete-artifact SR wording is necessary. State delivered admission, pause, retention and handover behavior; keep script/function/file names at LLR/IF level. The existing SRs already demonstrate capability-level wording.

   **NOTE:** the RESYNC_PACK claim is true for the **window change** under current shipped values: blackout is disabled by `12:00-12:00`, retention ships at 0, and the context guard ships at 0 ([process.toml.template:227](C:/Projects/ai-template/project-trajectory/process.toml.template:227), [process.toml.template:393](C:/Projects/ai-template/project-trajectory/process.toml.template:393), [process.toml.template:425](C:/Projects/ai-template/project-trajectory/process.toml.template:425)). Qualify it accordingly: the new adjudication entry and sign-in step can become visible when retention is enabled without arming blackout. WI-802 later ships retention at 55 independently ([WI-802:33](C:/Projects/ai-template/docs/work/queued/WI-802-session-families-reset-terms.md:33)).

7. **Size — NOTE: decompose by responsibility; no confirmed 1,000-SLOC breach yet.**

   The repository’s own `module_sloc` calculation reported coordinator guard **607**, retention rules **504**, and service **392** SLOC. Raw file length therefore does not establish that this change crosses the stated practice.

   Nevertheless, the row combines three independently reviewable changes ([WI-834:110](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:110), [WI-834:143](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:143), [WI-834:152](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:152)):

   - Shared coordinator adjudication request/entry, using existing retention and logging.
   - Blackout admission, close-down, lazy retirement and resume contracts.
   - Dedicated-home authentication detection and consent-first onboarding, followed by enabling 55.

   **Smallest spec change:** split onboarding from launch/window behavior, or declare these as dependency-ordered slices with separate acceptance checks. Keep shared admission and retention decisions in their owning boundaries, following PROCESS’s consolidation rule ([PROCESS.md:196](C:/Projects/ai-template/project-trajectory/PROCESS.md:196)).

No files were edited, created, staged or committed. The only checks executed were read-only inspection and pure blackout/SLOC calculations; no model call or live relaunch was attempted.