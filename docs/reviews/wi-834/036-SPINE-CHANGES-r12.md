# WI-834 round 12: spine change list

Row text owed by round 12 (`036-PLAN-r12.md`, F1 and F2). I edited no
registry row; the coordinator applies these.

## LLR-300, `detail` (F2)

- **Current:** `Hook responses inject the latch instruction once and bounded reminders thereafter.`
- **Proposed:** `Hook responses inject the latch instruction once and bounded reminders thereafter; inside a blackout window the latch is still recorded, but the blackout close-down, which requests no relaunch, is injected in their place.`
- **Why:** inside the window the context guard's drain text asked for the
  relaunch the window refuses (round 035 F2). The latch rule is unchanged;
  only what is said inside the window changes.

## TC-316, `method` (F2)

- **Current (last sentence):** `Assert that reopening the same session after the blackout with the context latch set still needs the owner's recorded clear.`
- **Proposed (last sentence):** `Assert that a context latch tripped inside the blackout window, and the latched holder's resumed start inside it, each record the latch and are told only the blackout close-down, never a relaunch request, and that reopening the same session after the blackout with the context latch set still needs the owner's recorded clear.`
- **Why:** the extended
  `test_reopening_the_same_session_with_both_drains_needs_the_owners_clear`
  (already in TC-316's evidence) now drives both cases the review names.

## TC-316, `expected` (F2)

- **Current:** `... Reopening after the clock drain ends remains refused until the owner records clear for the context latch.`
- **Proposed:** `... Inside the window a latched session is told only the blackout close-down, with no relaunch request. Reopening after the clock drain ends remains refused until the owner records clear for the context latch.`
- **Why:** as above.

## TC-340, `expected` (F1)

- **Current:** `No request is written during blackout and an existing request is cancelled at holder exit; the guard command in injected instructions runs on the hook's own interpreter.`
- **Proposed:** `No request is written during blackout and an existing request is cancelled at holder exit; the guard command in injected instructions runs on the hook's own interpreter, as typed in Bash and in PowerShell, from any working directory.`
- **Why:** the evidence test
  (`test_the_injected_guard_command_names_the_hooks_own_interpreter`, same
  name) now runs the emitted command in both shells, from outside the
  repository, for a plain path and a spaced one (round 035 F1).
