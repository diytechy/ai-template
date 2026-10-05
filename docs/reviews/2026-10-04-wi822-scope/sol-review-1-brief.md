You are a REVIEWER (Codex 6.1 Sol, gpt-6.1-sol, medium effort) for the ai-template repo. A Claude Opus coordinator wrote this scope; you are the other family's independent eye on it. Review only. Do NOT edit, create, stage or commit any file in this worktree. Your one writable scratch area is `C:/Projects/ai-template.wt/review-tmp/`.

## What you review

A newly filed work item's SCOPE, before anything is built: WI-822, the coordinator context guard.

- The row: `docs/work/queued/WI-822-coordinator-context-guard.md` (Context and Done-when).
- Its spec of record: `docs/specs/WI-822.md` (the design).
- The commit: `git show da34d0f6` (also touches `docs/handoff-2026-10-04-wave13-coordinator.md` and `docs/status.md`).

The owner's intent, in their words (2026-10-04): a coordinator session in Claude Code (the hand path that also runs the in-lane adjudication cycle) accumulates context over many lanes; "Is it possible to prime the adjudicator to prepare a handoff and close out current work items (without starting new lanes) if it's context grows over 50%? In theory it could also schedule a cmd file to launch a new session from said handoff." Then: "agree with WI-822 and a relaunch on session end". A single adjudication is not the risk; growth across lanes is.

Context to read as needed: `CLAUDE.md`; `project-trajectory/PROCESS.md` where touched; the wave-13 handoff (how the coordinator works: scoped unpause, claims via `integrate.py claim`, lane worktrees, squash landings, archive, sweep); `docs/process.toml` (the one dial home); `.claude/` (no tracked `settings.json` exists yet; `settings.local.json` is local); the owner's standing rules: fix a single point of failure rather than add a fallback or second path; enforce mechanically at the commit/tool call rather than by convention; judgements independent of what they judge.

The Claude Code facts the scope relies on came from the claude-code-guide agent reading the official docs: hook events include PostToolUse, PreToolUse, Stop, SessionEnd, PreCompact; every hook input carries `transcript_path` and `session_id`; a hook can add context (`additionalContext`) and a PreToolUse hook can refuse a call; transcripts carry each assistant message's `usage`; no context percentage is exposed; the auto-compaction threshold is undocumented. Treat these as claims: if you know any to be wrong or version-dependent, say so.

## Judge

1. **Fidelity to the owner's intent.** Does the scope do what the owner asked, no more and no less?
2. **Soundness.** Find concrete failure scenarios: occupancy computed wrongly (cache accounting, the newest-usage choice, subagent transcripts, a resumed session), the trigger firing never or repeatedly, the PreToolUse refusal being bypassable or blocking legitimate close-out work (landing, archive, the scoped-unpause restore, worktree removal), the SessionEnd relaunch launching twice, launching while the old session lives, launching in the wrong directory, or on a non-Windows host, a stale relaunch request from an earlier session, the `out/` state surviving across sessions incorrectly.
3. **Mechanisms vs the owner's rules.** Anything that is a fallback or second path, anything enforced only by convention that could be mechanical, any hard-coded value that should be a declared dial.
4. **Testability.** Is each Done-when item checkable without a live session? What is missing?
5. **Scope boundaries.** Is "this repo's tooling, shipping decided later" coherent with the kit's rules (stdlib, cross-platform, dogfood sync, the tracked `.claude/` surfaces)? Is the Codex-coordinator gap stated honestly?

Report findings as claims you confirmed by reading, never as guesses. Do not run pytest.

## Your final message (the review)

- First line, exactly: `da34d0f6 SOUND` or `da34d0f6 NOT YET SOUND`.
- Then **BLOCKER**, **MAJOR** and **MINOR** sections. Give each a `file:line` and a concrete failure scenario. Cite locations as plain repo-relative `path:line` text, never as markdown links. Write "none" for an empty section.
- Then a short **Verified** paragraph, and **Commands**: each command you ran, with its summary line.
