92375227 NOT YET SOUND

**Round-1 findings**

The round-1 review contains seven MAJOR entries, despite its stated count of six; all are assessed below.

- **BLOCKER — SessionEnd non-overlap: partly resolved.** docs/specs/WI-822.md:80 excludes `clear` and `resume`, but heartbeat-based lease stealing still permits two live coordinators.
- **MAJOR — Relaunch ownership/consumption: partly resolved.** docs/specs/WI-822.md:75–92 adds session/repo ownership, working directory, atomic acquisition, failure restoration and expiry; lease exclusivity remains unsound.
- **MAJOR — Command-spelling enforcement: partly resolved.** docs/specs/WI-822.md:63 moves refusal to `integrate.claim`, covering wrappers/imports, but measurement still occurs after tool execution.
- **MAJOR — Worktree refusal blocks close-out: resolved.** docs/specs/WI-822.md:68 removes that refusal; the Done-when explicitly tests verification worktrees, landing, archive, sweep, pause restoration and removal.
- **MAJOR — Unlatched drain: resolved.** docs/specs/WI-822.md:53–58 requires persistence across lower readings, compaction and resume; the Done-when tests those cases.
- **MAJOR — Eligibility/event cadence: resolved.** docs/specs/WI-822.md:37–47 identifies the coordinator by session and transcript, excludes foreign/subagent callbacks, and adds failed-tool, prompt and stop events.
- **MAJOR — Shipping/schema boundary: resolved.** docs/specs/WI-822.md:104–111 requires matching template keys, threshold-zero disabling and a RESYNC entry; tooling shipping remains an explicit decision.
- **MAJOR — Status prose prevents claiming: resolved.** docs/status.md:34 names the guard by title; every remaining `WI-<number>` token is inside the generated block.
- **MINOR — Compaction marker invents a cause: resolved.** docs/specs/WI-822.md:96–100 records trigger, occupancy and guard state, then classifies the event without introducing recovery.
- **MINOR — Occupancy fixture evidence: resolved at scope level.** docs/work/queued/WI-822-coordinator-context-guard.md:35–39 requires versioned fixtures covering branches, compaction, resume, malformed/partial usage and window mismatch.

**BLOCKER**

- docs/specs/WI-822.md:43 — **Heartbeat expiry does not establish that the previous coordinator ended.** Coordinator A remains open while awaiting owner input or a long-running tool, exceeding the expiry without a hook heartbeat. Coordinator B then takes the explicitly permitted stale lease. A’s subsequent hooks become foreign-session no-ops under lines 41–43, while both sessions remain available to coordinate. Recording the steal does not revoke A or establish non-overlap. Require mechanical exclusive ownership and verified termination/transfer; elapsed silence cannot authorize takeover.

**MAJOR**

- docs/specs/WI-822.md:45 — **The threshold can be detected after admitting a new lane.** The last measured response is below threshold. The next assistant response reaches the threshold and invokes `integrate.claim` as its first tool call. Admission checks the still-unlatched lease under lines 64–65; `PostToolUse` measures and latches only after the claim succeeds. The specified boundary therefore enforces “no claims once latched,” which is weaker than “no new lanes after the threshold.” Require current occupancy evaluation and latching before admission, with an offline fixture for this exact sequence.

**MINOR**

none

**Verified**

The spec and Done-when otherwise agree, and their behavioral checks can be exercised offline. Exit-reason filtering matches the [official SessionEnd reference](https://code.claude.com/docs/en/hooks#sessionend); the documented [hook lifecycle](https://code.claude.com/docs/en/hooks#hook-lifecycle) confirms that post-tool measurement follows execution.

Coordinator identity, a persistent drain latch, claim-boundary enforcement, exclusive ownership transfer, and atomic session/repo-bound request consumption are proportionate to the owner’s two requirements. Automatic heartbeat-expiry takeover adds an unnecessary second ownership path and undermines exclusivity. Request expiry and compaction telemetry are optional hygiene, not prerequisites for those requirements. No files changed; no pytest ran; the worktree remained clean.

**Commands**

PowerShell ranged reads below used line-numbering pipelines.

- `Get-Content CLAUDE.md` — read contributor rules.
- `Get-Content .agents/skills/antidote/SKILL.md; Get-Content .agents/skills/session-protocol/SKILL.md` — read review and claim conventions.
- `git status --short` — confirmed clean initial state.
- `Get-Content docs/reviews/2026-10-04-wi822-scope/sol-review-1.md` — read every original finding.
- `Get-Content docs/reviews/2026-10-04-wi822-scope/sol-review-1-brief.md` — read owner intent and review constraints.
- `git diff da34d0f6 92375227 -- docs/specs/WI-822.md docs/work/queued/WI-822-coordinator-context-guard.md docs/status.md docs/handoff-2026-10-04-wave13-coordinator.md` — inspected scoped fixes.
- Numbered `Get-Content` reads of the spec, WI row and status — confirmed fixed text and citation lines.
- `rg -n 'def _status_prose_refusal|def claim|status_prose_refusal|def store_dir|lease|SessionEnd' project-trajectory/scripts/integrate.py project-trajectory/scripts/session_keep.py` — located admission and shared-store mechanisms.
- `git rev-parse HEAD` — confirmed HEAD is `92375227`.
- `git show --stat 92375227` — inspected commit inventory and recorded claims.
- `rg -n 'WI-[0-9]+|BEGIN|END' docs/status.md` — confirmed WI tokens occur only inside the generated block.
- Ranged `Get-Content` reads of `integrate.py`, `session_keep.py` and `test_dogfood_sync.py` — checked claim admission, prose refusal, common-directory lookup and schema equality.
- Ranged `Get-Content docs/status.md` — checked all hand-authored working prose.
- `rg -n 'worktree|claim|Session|end procedure|exit|pause' docs/handoff-2026-10-04-wave13-coordinator.md` — checked close-out obligations.
- `git diff --check da34d0f6 92375227 --` followed by the four scoped paths — no whitespace findings.
- Official hooks-reference `open` and `find` calls — verified event ordering, context delivery and SessionEnd reasons.
- `git diff --quiet; git status --porcelain` — confirmed unchanged, clean final state.