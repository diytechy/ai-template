WI-834 spec NOT YET SOUND

| Round-1 finding | Resolution | Assessment of amended text |
|---|---|---|
| **1 — Historical window and lazy retirement** | **PARTLY** | Shared current/historical calculation, wrap semantics, missing timestamps and current-value reads are specified. Exact-end retirement remains ambiguous; the new-session test also needs qualification. See N2. |
| **2a — Service launch refusal** | **PARTLY** | Every caller now reaches the launch boundary, including interactive calls and probes. The active-row eligibility proof is false, and its service-visible identity needs completion. See N1. |
| **2b — Hook command coverage** | **PARTLY** | Shell forms, PowerShell, resumed subagents and IF-274/275 are covered. The blanket wrapper guard conflicts with admitted wrap-up adjudication. See N3. |
| **2c — Claim refusal NOTE** | **RESOLVED** | The existing dispatcher discriminator and guard-off ordering are explicitly retained at [WI-834:170](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:170). Its consequence for eligibility belongs to 2a/N1. |
| **3 — Drain cause, recovery and pending relaunch** | **RESOLVED** | Blackout is clock-derived; pending requests are cancelled; same-session and fresh-session recovery are named at [WI-834:176](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:176). The combined context-latch case merits N7. |
| **3 — Active-lane NOTE** | **RESOLVED** | Scheduled waiting preserves the claim; human-owed stops close partial. [WI-834:48](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:48). |
| **3 — Wrap-up eligibility NOTE** | **PARTLY** | An eligibility rule is supplied, but it does not establish pre-window admission. See N1. |
| **3b — Consent, denial and authentication states** | **PARTLY** | Denial preserves configuration/credentials; detection reports three states. Launch behavior for **unknown** remains unspecified. See N5. |
| **3b — Launcher scope** | **RESOLVED** | Owner ruling (g) settles the bare-product-run check. The agent-resume path stays prompt-free by specification. Remaining implementation-contract gaps are N4, not an objection to that ruling. |
| **3b — Read-only home resolution** | **RESOLVED** | Explicitly required at [WI-834:239](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:239). |
| **4 — Review-next pause point** | **RESOLVED** | Committed finished-step evidence is sufficient; reviews and rework remain pending in the handoff. Both requested fixtures are included. [WI-834:205](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:205). |
| **4 — Existing-bounds MINOR** | **RESOLVED** | “Existing bounds” and encouraged coordinator shutdown replace the overstated universal timeout guarantee. |
| **5 — Shared adjudication request** | **RESOLVED** | Required identities and deadline-related lease are named; shared composition is extracted once; WI-801 deletes the temporary CLI and migrates callers/tests. [WI-834:122](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:122). |
| **5 — Second retention mechanism NOTE** | **RESOLVED** | The justification correctly concerns bypassing kit planning, home overlay and bookkeeping. |
| **5 — Subagent persistence MINOR** | **RESOLVED** | The incorrect persistence claim is removed. [WI-834:65](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:65). |
| **6 — Omitted spine/interface contracts** | **RESOLVED** | Every contract originally identified is now listed, alongside the runtime-flow update and preservation of IF-278. [WI-834:255](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:255). |
| **6 — Threshold retirement MAJOR** | **RESOLVED** | Threshold draining waits for a clear point; blackout explicitly overrides chain continuity. |
| **6 — Capability-level SR NOTE** | **RESOLVED** | Capability voice without concrete artifacts is expressly required. |
| **6 — RESYNC visibility NOTE** | **RESOLVED** | Window, retention and bare-run changes are separately disclosed. Documentation completeness remains N6. |
| **7 — Responsibility grouping NOTE** | **RESOLVED** | Parts A/B/C have separate acceptance checks and can land as one lane under ruling (h). No split is requested. |

New and remaining findings follow, ranked by impact. Owner rulings (a)–(h) are treated as decisions.

**N1 — MAJOR: `active` does not prove pre-window eligibility, and the registry/role inputs are incomplete.**

[WI-834:166](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:166) says claims are refused inside blackout, therefore an active row predates it. The following claim rule expressly exempts the dispatcher.

That exemption is real: [dispatch.py:1085](C:/Projects/ai-template/project-trajectory/scripts/dispatch.py:1085) claims with `dispatch_lock_held=True`; [integrate.py:804](C:/Projects/ai-template/project-trajectory/scripts/integrate.py:804) skips the guard; the dispatch tick admits work without a blackout check at [dispatch.py:1468](C:/Projects/ai-template/project-trajectory/scripts/dispatch.py:1468). This is also documented explicitly at [docs/process.toml:227](C:/Projects/ai-template/docs/process.toml:227). An adjudication row can consequently become active inside blackout and satisfy the proposed exception.

The service already sees `Call.role`, so an explicit `role == "ADJUDICATE"` condition needs no bypass flag. However, [Call:98](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:98) has no independent WI field; `Keep.wi` exists only when retention applies. The exception must work when retention is off too.

The registry copy also matters. [load_wi_registry:770](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:770) reads the lane’s checked-out registry. The close-first rule moves its spec terminal before the final verdict ([session-protocol:163](C:/Projects/ai-template/.agents/skills/session-protocol/SKILL.md:163)), while its primary-checkout claim can still be active.

**Smallest spec change:** apply blackout claim refusal to the dispatcher too, preserving its exemption from the **context** guard. Define launch eligibility as `ADJUDICATE` plus a named WI with an active claim in the primary-checkout registry; carry that identity independently of `Keep`. If dispatcher blackout claims remain admitted, require explicit pre-window admission evidence instead of inferring it from status.

**N2 — MAJOR: historical lookup excludes the exact instant when admission reopens.**

The historical query asks for an end **“before `t`”** at [WI-834:152](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:152), while admission retains an exclusive end. Existing tests explicitly admit a call exactly at 19:00 ([test_agent_loop_policy.py:136](C:/Projects/ai-template/tests/test_agent_loop_policy.py:136)).

With a strict historical comparison, a first keep call at Monday 19:00 finds an older completed window. A session last used Monday 18:30 therefore escapes retirement. Successful bookkeeping then advances its last-use timestamp ([session_keep.py:783](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:783)), preventing later retirement against Monday’s end.

The ordinary inside-window wrap-up is otherwise coherent: if it finishes at 18:30, `last_used < 19:00` retires it after blackout. Clock-derived drain needs no latch to achieve that.

A wrap-up finishing at 19:01 is different: bookkeeping records completion, so it **does not** satisfy the retirement predicate. The unqualified “resumes … under a new session” acceptance line at [WI-834:221](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:221) must account for this case.

**Smallest spec change:** say “most recent window whose end is **at or before `t`**.” Pin three fixtures: wrap-up ending inside, exactly at, and after the end; qualify fresh-session acceptance by the stated last-use predicate. Include a keep-warm-first fixture: its existing lease path bypasses `_before_launch` ([session_keep.py:869](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:869)), so retirement must precede any timestamp-refreshing ping.

**N3 — MAJOR: wrapper admission can block the permitted wrap-up before the service evaluates it.**

The service admits active-row adjudication, but [WI-834:188](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:188) requires coordinator launch scripts to call a guard subcommand that exits nonzero throughout blackout.

Part A’s temporary adjudication entry point is itself a coordinator launch script. Applying that blanket guard blocks its permitted call. The admission data belong at the service boundary, which already receives the role ([session_service.py:99](C:/Projects/ai-template/project-trajectory/scripts/session_service.py:99)).

**Smallest spec change:** explicitly exempt service-backed adjudication entry points from the unconditional wrapper check. Have them use the service’s eligibility decision; apply the wrapper check to coordinator model launches outside that service path.

**N4 — MAJOR: Part C lacks a complete run-to-dev-setup contract.**

Both check tiers deliberately return **0 even when components are missing** ([dev-setup.sh:190](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.sh:190), [dev-setup.ps1:133](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.ps1:133)). They expose a human report, not a defined missing-components result for `run`. [WI-834:232](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:232) requires conditional installation without defining how that decision crosses the seam.

There are concrete launcher constraints:

- POSIX `run` currently exits before reaching anything else when Python is absent ([run.sh:13](C:/Projects/ai-template/project-trajectory/scripts/run.template.sh:13)). If runtime installation is declined, it cannot fulfill an unconditional “then shows the menu.”
- The Windows dev-setup wrapper changes directory into `scripts/` ([dev-setup.cmd:11](C:/Projects/ai-template/project-trajectory/scripts/dev-setup.template.cmd:11)); blindly chaining it does not preserve repository-root policy/home resolution.
- macOS `run.command` delegates to `run.sh` ([run.command:7](C:/Projects/ai-template/project-trajectory/scripts/run.template.command:7)); adding a check to both would run it twice.
- The menu supports piped selections ([run_menu.py:230](C:/Projects/ai-template/project-trajectory/scripts/run_menu.py:230)). Setup consent must not consume them. Windows argument forms also need to bypass the existing final `pause` ([run.cmd:32](C:/Projects/ai-template/project-trajectory/scripts/run.template.cmd:32)) to satisfy “never prompt.”

**Smallest spec change:** define one dev-setup-owned check/offer operation for bare run, preserving standalone check’s read-only, always-green contract. Specify repository-root execution, one invocation through macOS delegation, skipped consent without an interactive terminal, and an actionable exit when the runtime remains unavailable.

**IF clarification:** IF-048 exists, but it is the capability **stdout** seam ([interfaces.toml:828](C:/Projects/ai-template/docs/requirements/interfaces.toml:828)), not the setup invocation/result seam. Preserve its machine listing and declare the new seam; IF-157/158 describe existing argv and exit behavior.

**N5 — MINOR: “unknown” authentication has no launch disposition.**

Part C reports signed-in, missing and unknown; Part A refuses only missing authentication ([WI-834:138](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:138), [WI-834:237](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:237)). A failed status command or unreadable response leaves the builder choosing between launch, refusal and an interactive offer.

Conditional appearance also requires reading the retention dial. That is feasible with stdlib Python: [keep_config:145](C:/Projects/ai-template/project-trajectory/scripts/session_keep.py:145) already supplies its semantics. Shell/PowerShell should call that shared reader when a suitable runtime exists, while preserving dev-setup’s ability to report on an unprovisioned workstation ([test_onboard_devsetup.py:162](C:/Projects/ai-template/tests/test_onboard_devsetup.py:162)).

**Smallest spec change:** define unknown as a diagnostic refusal, without automatic sign-in; name the shared dial/home reader and the reporting behavior when it cannot run.

**N6 — MINOR: shipping documentation still promises behavior this row changes.**

The start-weekday wrap rule is correct: Friday’s tail extends into Saturday; Monday’s early tail cannot originate on Sunday. It preserves `[start, end)`. No existing wrap/weekend assertion I found requires the old incorrect behavior: wrap tests use Tuesday, and weekend tests use a non-wrapping daytime interval ([test_agent_loop_policy.py:140](C:/Projects/ai-template/tests/test_agent_loop_policy.py:140), [test_agent_loop_policy.py:156](C:/Projects/ai-template/tests/test_agent_loop_policy.py:156)). The “weekends are never blacked out” comment needs narrowing.

Other published promises directly conflict with the amendment:

- No new coordinator session during blackout: [PROCESS_OPTIONS.md:842](C:/Projects/ai-template/project-trajectory/PROCESS_OPTIONS.md:842), [process.toml.template:203](C:/Projects/ai-template/project-trajectory/process.toml.template:203).
- Keep-warm fires through blackout: [process.toml.template:400](C:/Projects/ai-template/project-trajectory/process.toml.template:400).
- Guard-off hooks do nothing: [process.toml.template:422](C:/Projects/ai-template/project-trajectory/process.toml.template:422).

**Smallest spec change:** add these documentation updates explicitly to Done-when, including start-weekday wrap semantics, the adjudication exception, suppressed pings and blackout operation at guard dial zero.

**N7 — MINOR: same-session recovery needs a condition when both drain causes occur.**

Blackout expires by clock, but the context latch remains unchanged. Reopening the same holder preserves that latch ([coordinator_guard.py:392](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:392), [coordinator_guard.py:612](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:612)); claims remain refused ([coordinator_guard.py:493](C:/Projects/ai-template/project-trajectory/scripts/coordinator_guard.py:493)).

Thus [WI-834:201](C:/Projects/ai-template/docs/work/queued/WI-834-coordinator-blackout-retained-adjudicator.md:201) describes sufficient recovery only when blackout was the sole drain cause.

**Smallest spec change:** state that a still-latched context drain requires the owner’s recorded clear for same-session claim recovery, or release/take for a fresh holder. Add a combined-drain fixture.

All requested IDs exist, including IF-278 with the stated owner/token-transfer rule. Reviewed against `df9cda7b`; no files were edited, created, staged or committed, and no mutating tests or live launches were run.