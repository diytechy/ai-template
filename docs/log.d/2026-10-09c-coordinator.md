## 2026-10-09c: coordinator (attended): WI-834 brought to landing

The owner stopped overnight leg 03 at 15:20 and released its lease, leaving
WI-834 parked at its round bound (D-016: gate 012's MAJOR, the readiness
check and the run launcher choosing Python separately). The owner directed
that the rounds continue until the lane could land (D-018). This session took
the lease at 20:31Z.

- **Rounds 4-12** (builders: kit-builder Opus at medium; a fresh builder from
  round 9 after a safety classifier cut off a brief that asked for every
  form escaping the hook):
  - **4:** one floor-resolved interpreter, resolved by the launcher, handed
    to the readiness check and run by the menu. The launcher's candidates
    are pinned equal to each dev-setup's runtime search.
  - **5:** two fixes.
    - A PowerShell assignment's right-hand command is read as a launch
      (dispute 017, FIX).
    - The hook opt-in binds the guard to its interpreter in the
      machine-local settings. This followed an owner ruling (D-019) among
      three options; WI-880 takes the kit-wide leftovers.
  - **6-7:** two more fixes, plus a new module.
    - Assignments are recognised by their operator, whatever the target.
    - Words carry every quoted span.
    - The guard owns only commands of its example's exact shape.
    - `kitlib/guard_hooks.py` was split out at the 1000-SLOC ratchet.
  - **8:** two fixes.
    - PowerShell's dot invocation (dispute 025, FIX). The sitting drew the
      coverage line at the shell grammar's command word, with wrapper
      commands outside it.
    - The readiness check queries Git only once it has found it.
  - **9-10:** a grammar-word table skips `time -p`, `coproc` and `coproc
    NAME` before a compound opener (dispute 031, FIX). Sitting 031 ruled
    that later grammar-only forms no agent writes are dismissed.
  - **11:** two changes.
    - This repo's Windows readiness check now offers a missing runtime.
      It is pinned in a real console; the typist race was found and
      designed out, 60 of 60 runs green.
    - The lane's own installed-hook test was weekday-dependent and is fixed
      test-only. The guard has no clock seam, and none was added.
  - **12:** guard commands run as typed in Bash and PowerShell, from any
    directory. A context latch tripped inside a blackout is recorded, and
    the session is told only the close-down.
- **Checkpoints:** Terra (retained session `01a1212d…`) reconciled the
  spine change lists four times. Sittings 015, 023, 027 and 038 blessed every
  amendment, all MEANING.
- **Gates:**

  | Gate | Result |
  |---|---|
  | 016 | 2 MAJOR |
  | 024 | 2 MAJOR |
  | 028 | 1 MAJOR |
  | 032 | 1 MAJOR |
  | 035 | 2 MINOR |
  | 039 | 1 MINOR, dismissed by dispute 040 (not-worth-cost: fails closed) |

  The lane landed on gate 039 (D-027).
- **Landing:** squash `fb1990aa` after a no-op rebase (trunk unchanged at
  `ed2533cb`). Acts run to seq 90; the landing commit's message says 89,
  which is wrong. The re-mint WI-879 is closed as settled (`102486f7`).
  `archive/lanes` is at `9a7d7ddd`.
- **Smoke budget:** read over (62-104 s) while the workstation was in heavy
  desktop use. The parent commit, timed in the same window, was equally
  over; quiet readings were 40-50 s. Every commit's bar results were green
  (2393 passed).
- **Codex:** one usage limit at 21:09. The owner switched accounts.
- **Recipes:** three lessons folded into the coordinator-cycle recipes:
  - hook-coverage briefs are framed as grammar reading;
  - `review_brief.py file` picks the round number;
  - a smoke budget breach under load is A/B-timed against the parent.
- **Full suite** at `102486f7`: **1 failed, 5626 passed, 21 skipped** in 803 s. The failure, `test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`, asserts a `wall < 40` s kill. It also fails 3 of 3 on the pre-landing base `ed2533cb` under this evening's machine load, and passed in leg 02's quiet full suite. It is a load-sensitive timing test that predates WI-834; the next session re-runs it on a quiet box.
