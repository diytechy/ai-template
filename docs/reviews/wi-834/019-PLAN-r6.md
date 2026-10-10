# WI-834 rework round 6: coverage plan

Answers `docs/reviews/wi-834/018-REVIEW-A-fd605d5-narrow.md` (F1, F2: its
two `[MAJOR]` lines, in order). Lane tip b486134a; round 5 is fd605d5b. F1
lies inside dispute 017's FIX ruling (D-020), so it needs no new sitting; F2
is a round-5 regression of the D-019 opt-in.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1: a PowerShell assignment is recognised by its operator, never by its target's shape, so every target form's right-hand command is read as a command | F1; D7; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | F2: the hook opt-in owns the guard's commands, not whole groups: it removes only those from existing groups and keeps every other command and the group's configuration | F2; D43; D51; SR-227; SR-230; TC-345 | IF-280 | |

## R1 (F1)

- **Confirmed** through the actual hook. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r5/f1-probe-r6.py`
  runs `coordinator_guard.py --root <scratch> hook` as a subprocess with
  `context_guard_pct = 0` and a window covering now, on lane fd605d5b. "no
  decision" means close-down context only, no deny:

  ```text
  '$response = claude -p x'                                    -> deny
  '$result.Answer = claude -p x'                               -> no decision (not denied)   review form
  '$answers[0] = claude -p x'                                  -> ALLOW                      review form
  '[string[]]$answers = claude -p x'                           -> ALLOW                      review form
  '$script:x = claude -p x'                                    -> deny                       extra probe
  '$global:x += claude -p x'                                   -> deny                       extra probe
  '$a.b[1].c = codex exec -'                                   -> ALLOW                      extra probe (nested property + index)
  '[System.Collections.Generic.List[string]]$l = claude -p x'  -> ALLOW                      extra probe (generic type)
  '$result.Answer = "claude -p x"'                             -> ALLOW (correct: a value)
  'echo a = claude'                                            -> ALLOW (correct: an argument)
  ```
- **Class:** round 5 recognised an assignment by enumerating target shapes
  (`_PS_TARGETS`: `$name`, `[type]$name`, `$env:NAME`, comma lists), so any
  unlisted shape hides its right-hand command.
- **Sites:** `coordinator_guard.py` `_PS_TARGETS` (:877), `_assigned`, and
  `_right_hand`; `kitlib/shell_line.py` `Word.quoted_at`, which is
  unchanged. Search:
  `rg -n "_PS_TARGETS|_PS_OPERATORS|def _assigned|def _right_hand|quoted_at" project-trajectory/scripts/coordinator_guard.py project-trajectory/scripts/kitlib/shell_line.py`.
- **Owning boundary:** `_assigned`, in the PowerShell dialect only. A
  statement whose first word is unquoted and starts with `$` or `[` is an
  assignment when an unquoted assignment-operator word follows its leading
  words. The operators are `=` `+=` `-=` `*=` `/=` `%=` `??=`: standalone,
  attached after the target (`$r=claude`, `$r= x`), or at a word's start
  (`$r =claude`). "Unquoted" means before the word's first quoted piece
  (`quoted_at`), so `$h['a=b']` does not count. Its command is the first word
  after the operator, read by the existing rule: a quoted or variable
  right-hand side is data. `(…)`, `&` and `$(…)` keep their existing handling
  as boundaries and substitutions. `_PS_TARGETS` is deleted. Nothing depends
  on the target's shape, so property, index, array-type, generic-type,
  scoped and future target forms are covered. A first word that is not a
  `$`/`[` word (`echo a = claude`) is never an assignment. One construction
  choice the instruction leaves open: a variable right-hand side that is
  itself an assignment (`$a = $b = claude -p x`, a chained assignment that
  runs `claude`) is read through the same rule (D-022).
- **Pins (red first, through the actual hook, TC-339's QUOTED_DENIED /
  QUOTED_ALLOWED):**
  - denied: the review's three forms, plus `$a.b[1].c = codex exec -`,
    `[System.Collections.Generic.List[string]]$l = claude -p x`,
    `$h['k=v'] = claude -p x`, `$r =claude -p x`, `$a = $b = claude -p x`;
  - allowed: `$result.Answer = "claude -p x"`, `$answers[0] = 'claude -p x'`,
    `echo a = claude`, `$x -match 'a=claude'`.

## R2 (F2)

- **Confirmed** on the real path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r6/f2-probe.py`
  runs the real `hooks --enable` against the shipped example. It then puts a
  user command and a matcher into the installed PreToolUse group beside the
  guard's command, and re-enables:

  ```text
  first enable -> on
  mixed group before: [{"hooks": [{..."coordinator_guard.py\" hook"...}, {"type": "command", "command": "echo user-audit-notification"}], "matcher": "Bash"}]
  state -> off
  re-enable -> on
  after: [{"hooks": [{..."coordinator_guard.py\" hook"...}]}]
  user command kept: False
  ```

  Round 5's `enable_hooks` drops any group `_is_guard` matches, whole, with
  its other commands and its matcher.
- **Class:** ownership at the wrong grain: the opt-in owns whole groups
  where it owns only the guard's commands.
- **Sites:** `coordinator_guard.py` `_is_guard` (group-level), `enable_hooks`
  (the filter), `hooks_state` (compares whole groups), and `_guard_entries`
  (selects the example's guard groups, which is correct: the example's
  groups are the kit's own). Search:
  `rg -n "_is_guard|def enable_hooks|def hooks_state|def _guard_entries|def _wanted" project-trajectory/scripts/coordinator_guard.py`.
- **Owning boundary:** one merge function, `_merged(hooks, wanted)`.
  - For each event the example registers, every existing group keeps its
    configuration and every command except the guard's own (a command whose
    text runs `coordinator_guard.py`).
  - A group is dropped only if removing the guard's commands leaves it with
    none.
  - Then the guard's bound groups are added.
  
  `enable_hooks` writes `_merged`'s result. `hooks_state` reads the same
  ownership: `on` exactly when `_merged` would change nothing. A re-run is
  therefore idempotent, and a denial still writes nothing.
- **Pins (red first, TC-345):** the existing in-process opt-in test gains a
  mixed PreToolUse group (a matcher, a user command and a stale guard
  command). Enable and re-enable must keep the user command and the matcher
  unchanged and move the guard command into the bound group; `hooks_state`
  must read `on` after enable. The test is extended rather than a new one
  added, because the smoke tier sits at its membership budget.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-317; TC-318; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-340; TC-341; TC-342 — the retention, relaunch, launcher, sign-in and adjudication paths are untouched by round 6 (F1 is the PowerShell assignment reading, F2 the opt-in's merge); they run in their tiers unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D8; D9; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D44; D45; D46; D47; D48; D49; D50; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (through round 5, fd605d5b) and not reopened by narrow round 018; it reopens only the hooks' launch reading (D7/D10/D25, F1) and the hook opt-in with its test (D43/D51, F2).
