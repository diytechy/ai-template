# WI-834 checkpoint sitting 038 (cb6a3267)

## amendment

The three rows record the lane's answers to review 035 (commit 5935b631).
- **The drain text inside a window.** Inside a blackout window, a context
  latch is still recorded, but the context guard's drain text is replaced by
  the blackout close-down. The drain text asks for the relaunch the window
  refuses (F2).
- **The guard command.** The command the injected instructions name runs as
  typed in Bash and in PowerShell, from any working directory, on the hook's
  own interpreter and the guard file's absolute path (F1).

What I observed at cb6a3267:
- **The latch change.** In `coordinator_guard.on_blackout`, `_is_drain`
  recognises the drain text by its `DRAIN_MARK` opening and drops it, and
  `_close_down(..., tell=True)` tells the close-down on that event. The latch
  record is untouched.
- **The command change.** `_guard_command` writes one line when both paths
  are plain. Otherwise it writes a single-quoted Bash line and an `& '…'`
  PowerShell line side by side.
- **Tests.** The blackout, guard, guard-e2e, run/dev-setup and evidence-join
  suites gave `218 passed, 4 skipped` (pseudo-terminal and POSIX-only cases).
  - `test_reopening_the_same_session_with_both_drains_needs_the_owners_clear`
    trips the latch inside the window (PostToolUse) and resumes (SessionStart).
    Each response carries the close-down and never "request the relaunch". The
    lease stays draining, and after the window only the owner's clear lets the
    claim through.
  - `test_the_injected_guard_command_names_the_hooks_own_interpreter` runs
    each emitted line, plain and with a spaced interpreter path, in sh and in
    PowerShell, from a directory outside the repository. Each exits 0.

- [MEANING] LLR-300 Detail -> hook responses inject the latch instruction once and bounded reminders thereafter, in every case -> the same, except inside a blackout window: the latch is still recorded, but the close-down (which requests no relaunch) is injected in its place -> the content a latched session is told inside a window changed; an implementation that sent the drain instruction there, asking for the relaunch the window refuses, now fails; blessed: it resolves a real conflict between the two drains in favour of the window's rule (SR-230: no relaunch inside the window), and the code and test match it
- [MEANING] TC-316 Expected, Method -> verify the latch and its recoveries, and that reopening after the blackout needs the owner's clear -> also verify that a latch tripped inside the window, and the latched holder's resumed start there, each record the latch and are told only the close-down, never a relaunch request -> a new asserted case; blessed (the reopening test above asserts exactly this)
- [MEANING] TC-340 Expected -> verify the guard command in injected instructions runs on the hook's own interpreter -> also on the guard file's own absolute path, as typed in Bash and in PowerShell, from any working directory -> a stronger acceptance condition: a relative-path or single-shell command that met the old text fails it; blessed (the emitted-line test runs every form in both shells from outside the repository)

VERDICT: MEANING rows=3

The act re-attests LLR-300, TC-316 and TC-340.

Observation, not a return: TC-340's guard-command clause (the hook's
interpreter and the guard's absolute path, runnable in both shells) states a
behaviour of the injected instruction texts that neither LLR-300 nor LLR-301
names. LLR-300 describes what the instructions say, not how the command they
name is written. This has been so since sitting 023 added the interpreter half.
A later spine pass may give it a clause in LLR-300, beside the instruction
texts, so the TC verifies a stated arm.

SITTING: JUDGED kinds=amendment
