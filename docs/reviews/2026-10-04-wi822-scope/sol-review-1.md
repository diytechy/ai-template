da34d0f6 NOT YET SOUND

## BLOCKER

- docs/specs/WI-822.md:36 — **SessionEnd does not guarantee coordinator non-overlap.** It also fires on `/clear` and interactive `/resume`, while the CLI remains available for another conversation. With a pending request, the specified hook launches another coordinator while the existing CLI continues. Require explicit exit-reason handling and a mechanically verified ownership transfer; test clear, resume, and process exit separately. [Official hook reference](https://code.claude.com/docs/en/hooks#sessionend).

## MAJOR

- docs/work/queued/WI-822-coordinator-context-guard.md:45 — **Relaunch ownership and consumption are incomplete.** Only the threshold instruction is explicitly keyed by `session_id`; the request is launched merely because it exists, then consumed. A request left by session A can therefore launch on session B’s exit. Concurrent handlers can both observe it before consumption. Require session/repo ownership, atomic acquisition, launch-failure semantics, and duplicate/stale-request tests. Declare the coordinator directory explicitly: a handoff path alone does not establish the launch working directory.

- docs/specs/WI-822.md:29 — **The guard recognizes command spellings rather than owning admission.** `python helper.py` can invoke `integrate.claim()` or spawn Git internally without exposing either forbidden command in the tool input. The existing integrator already owns claim admission at project-trajectory/scripts/integrate.py:650. Specify enforcement through that boundary, with the hook supplying session state; otherwise a routine wrapper bypasses the promised prohibition.

- docs/work/queued/WI-822-coordinator-context-guard.md:42 — **The worktree prohibition blocks required close-out work.** The row refuses `git worktree add` without distinguishing new lanes from verification worktrees. The coordinator’s end procedure explicitly requires a detached worktree for the final suite at docs/handoff-2026-10-04-wave13-coordinator.md:148. The scope needs operation-specific acceptance cases covering that worktree, already-claimed lanes, landing, archive, sweep, pause restoration, and removal.

- docs/specs/WI-822.md:29 — **Drain mode is not specified as latched.** Refusal applies “past the threshold,” and instructions are emitted per crossing. After compaction lowers occupancy, that condition no longer holds, allowing new claims in the same coordinator session even though it was instructed to close out. Specify whether drain mode persists until ownership transfer, including resumed-session behavior, and test above → compacted-below → claim.

- docs/specs/WI-822.md:23 — **Coordinator eligibility and notification delivery are unspecified.** Project hooks also run for subagent tool calls. Without distinguishing the coordinator from builders/adjudicators, a subagent callback can consume the once-per-session notification intended for its parent. The design also monitors successful tool calls only, leaving failed calls and responses without tools outside its stated cadence. Require coordinator identification and fixtures for parent/subagent callbacks, no-tool turns, and failure events. [Official hook reference](https://code.claude.com/docs/en/hooks).

- docs/work/queued/WI-822-coordinator-context-guard.md:52 — **The deferred shipping decision conflicts with existing schema enforcement.** Adding threshold/window keys only to docs/process.toml fails the exact section/key equality enforced by tests/test_dogfood_sync.py:225. Adding them to the shipped template already changes an adopter-facing surface. Resolve this boundary before implementation; “RESYNC_PACK: none” at line 61 cannot settle it by itself.

- docs/status.md:34 — **The new “build first” instruction prevents claiming WI-822.** The commit introduces its ID into hand-authored status prose. project-trajectory/scripts/integrate.py:285 detects precisely that token, and line 690 invokes the refusal during claim admission. A scoped unpause does not remove this separate refusal.

## MINOR

- docs/specs/WI-822.md:40 — **The compaction marker asserts a cause it cannot establish.** Manual `/compact` below 50%, or compaction during legitimate draining after the instruction fired, still produces “the 50% path was missed.” Record trigger, occupancy, and guard state; classify a miss from those facts. This is useful telemetry, but should not become a second recovery path. [Official hook reference](https://code.claude.com/docs/en/hooks#precompact).

- docs/work/queued/WI-822-coordinator-context-guard.md:35 — **The occupancy fixture contract needs stronger evidence.** Cache-inclusive accounting matches the documented input-only formula. However, a fixture containing one convenient assistant usage record cannot establish selection across transcript branches, compaction, or resume. Require version-identified transcript fixtures and expected selection for those cases, plus malformed/partial usage and denominator mismatch. The documented status-line usage becomes null immediately after compaction, illustrating why “newest historical usage” needs an explicit validity rule. [Official status-line documentation](https://code.claude.com/docs/en/statusline#context-window-fields).

**Verified:** The intended coordinator handoff and session-end relaunch match the owner’s request. Stdlib Python, Windows/POSIX launchers, tracked project hooks, and the explicitly recorded Codex gap are coherent choices. Most Done-when items are checkable offline, but the current stubbed-launch dry run does not establish lifecycle exclusivity, ownership, or actual hook registration behavior. I confirmed the findings above from the scope, existing code, and official documentation; I did not establish the claimed per-reply transcript schema or undocumented auto-compaction threshold as stable contracts. No files were changed and no pytest ran.

**Commands:** PowerShell read pipelines below included line numbering/range filtering.

- `Get-Content CLAUDE.md; Get-Content .agents/skills/antidote/SKILL.md` — read contributor rules and review skill.
- `git show da34d0f6 --` — inspected commit; generated dashboard output was truncated.
- `Get-Content` on the WI row, spec, wave-13 handoff, and docs/process.toml — read scope and coordinator policy.
- `git show --stat da34d0f6` — confirmed seven changed files.
- `git show da34d0f6 -- docs/handoff-2026-10-04-wave13-coordinator.md docs/status.md` — inspected coordinator instruction changes.
- `rg` searches in the wave-13 handoff, PROCESS.md, test_dogfood_sync.py, integrate.py, and .gitignore — located lifecycle, admission, schema, and state rules.
- `rg --files .claude; git ls-files .claude` — confirmed tracked Claude surfaces; no tracked settings.json.
- `Get-Content .agents/skills/session-protocol/SKILL.md` — checked claim and close-out rules.
- Ranged `Get-Content` reads of integrate.py, wave-11/wave-13 handoffs, test_dogfood_sync.py, PROCESS.md, status.md, CLAUDE.md, and process.toml — confirmed cited locations.
- `rg -n 'settings.local|settings.json|claude' .git/info/exclude .gitignore tests/test_dogfood_sync.py` — local `.git/info/exclude` path unavailable; other files searched.
- `git diff --quiet; git status --short; git status --porcelain` — worktree remained clean; status checks repeated during review.
- Official-doc browser `open`, `find`, and search calls — checked hooks, status-line accounting, settings scope, and model/compaction documentation.