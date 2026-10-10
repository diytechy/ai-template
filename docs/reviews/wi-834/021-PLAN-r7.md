# WI-834 rework round 7: coverage plan

Answers the two sibling observations narrow round 020 recorded
(`docs/reviews/wi-834/020-REVIEW-A-70d6901-narrow.md`, its "Pre-existing
observations" at lines 42-46; verdict APPROVE, findings=0), called O1 and O2
here. Lane tip f238ed2c; round 6 is 70d69014.

020 carries no finding line, so plan_coverage reads no `F#` clause from it.
These rows therefore cite the spec's D-clauses and the item's SRs and TCs,
and O1 and O2 are named in the titles only. See the report for what
`--findings` accepts.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | O1: the reader knows, for every character of a word, whether it was quoted, so an assignment operator after a quoted piece in the same word is found | D7; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | O2: a command belongs to the guard only in the exact shape the opt-in writes, defined once from the shipped example; the merge and hooks_state read that one definition | D43; D51; SR-227; SR-230; TC-345 | IF-280 | |

## R1 (O1)

- **Confirmed** through the actual hook. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r5/f1-probe-r6.py`
  on lane f238ed2c runs `coordinator_guard.py --root <scratch> hook` as a
  subprocess at `context_guard_pct = 0` inside a window covering now. "no
  decision" means close-down context only, no deny:

  ```text
  "$h['answer']=claude -p x"     -> no decision (not denied)   review form
  "$o.'Answer'=claude -p x"      -> ALLOW                      review form
  '$o."A"=claude -p x'           -> ALLOW                      extra probe (double-quoted member)
  "$h['answer'] = claude -p x"   -> deny
  "$o.'Answer' = claude -p x"    -> deny
  "$h['k=v'] = claude -p x"      -> deny
  "$x -match 'a=claude'"         -> ALLOW (correct)
  ```
- **Class:** quotedness inside a word. `Word.quoted_at` records only where
  the first quoted piece starts. `_operator_end` therefore searches only the
  text before it, and misses an unquoted operator that comes after a quoted
  piece in the same word.
- **Sites:** `kitlib/shell_line.py` `Word` (`quoted_at`) and `_Scanner._word`
  (where it is set). The `coordinator_guard.py` readers of `quoted_at` are
  `_assigned`, `_operator_end`, `_tail` and `_right_hand`. Search:
  `rg -n "quoted_at" project-trajectory/scripts tests`.
- **Owning boundary:** the scanner records each quoted piece's span once
  (`Word.spans`, half-open offsets into the word's text). `Word.quoted(i)`
  answers for one character, and `Word.opens_quoted` says whether the word
  starts quoted. `quoted_at` is deleted, leaving one representation.
  `_operator_end` returns the end of the first operator none of whose
  characters is quoted, anywhere in the word, and `_tail` shifts the spans.
- **Pins (red first, through the actual hook, TC-339):** `$h['answer']=claude -p x`,
  `$o.'Answer'=claude -p x` and `$o."A"=claude -p x` are added to
  QUOTED_DENIED. `$h['k=v'] = …` stays denied (already in QUOTED_DENIED) and
  `$x -match 'a=claude'` stays allowed (already in QUOTED_ALLOWED).

## R2 (O2)

- **Confirmed** on the real path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r6/o2-probe.py`
  runs the real `hooks --enable` against the shipped example. It puts
  `ruff check project-trajectory/scripts/coordinator_guard.py` and a matcher
  into the installed PreToolUse group beside the guard's command, then
  re-enables:

  ```text
  first enable -> on
  state -> off
  re-enable -> on
  after: [{"hooks": [{..."coordinator_guard.py\" hook"...}]}]
  user command kept: False
  ```
- **Class:** identifying the guard's own commands. `_is_guard` matches any
  JSON that mentions `coordinator_guard.py`, so any user command naming the
  file counts as the guard's.
- **Sites:** `coordinator_guard.py` `_is_guard` (used by `_guard_entries` to
  select the example's guard groups, and by `_without_guard` to remove owned
  commands), `_merged`, `hooks_state`, `enable_hooks` and `_wanted`. Search:
  `rg -n "_is_guard|_without_guard|_merged|_wanted|_guard_entries" project-trajectory/scripts/coordinator_guard.py`.
- **Owning boundary:** ownership is defined once, from the shipped example's
  own guard commands. `_guard_shapes` returns each one as (its interpreter
  word, the rest: the guard script and its hook subcommand). A settings
  command is the guard's only if it is exactly one of those shapes, with
  either the example's own interpreter word (the bare `python` an older or
  hand-copied install holds) or a double-quoted absolute path (what the
  opt-in's binding writes) in front. `_without_guard` and `_merged` read
  only that definition, and so does `hooks_state` (through `_merged`).
  `_is_guard`'s filename mention stays only where it belongs: picking the
  guard's groups out of the kit's own example. As built, these pure functions
  moved into a new module, `kitlib/guard_hooks.py`, as `guard_groups`,
  `bind`, `command_shapes` and `merged` (with `_owns`, `_without_guard` and
  `_split_interpreter`), because the round took `coordinator_guard.py` past
  the 1000-line module ratchet, whose rule is to decompose. File I/O,
  `hooks_state` and `enable_hooks` stay in the guard (D-023).
- **Pins (red first, TC-345):** the existing in-process opt-in test's mixed
  group gains `ruff check project-trajectory/scripts/coordinator_guard.py`,
  which must survive enable and re-enable unchanged. Its stale command
  becomes the example's own bare-`python` guard command, which must still be
  replaced by the bound one. `hooks_state` must read `on` after.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-317; TC-318; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-340; TC-341; TC-342 — the retention, relaunch, launcher, sign-in and adjudication paths are untouched by round 7 (O1 is the reader's quotedness inside a word, O2 the opt-in's ownership of commands); they run in their tiers unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D8; D9; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D44; D45; D46; D47; D48; D49; D50; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (through round 6, 70d69014) and not reopened by round 020's observations, which touch only the hooks' launch reading (D7/D10/D25, O1) and the hook opt-in with its test (D43/D51, O2).
