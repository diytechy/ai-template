# WI-834 rework round 1: coverage plan

Answers `docs/reviews/wi-834/001-REVIEW-A-785a004.md` (F1..F5 in the order written).

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1: one quote-aware interpretation of a shell command line at the hook's input boundary (class, sites and boundary below) | F1; D10; D25; SR-229; TC-339; TC-316; TC-317; TC-315 | IF-274; IF-275 | |
| R2 | F3: the review-next / rework-verdict pause scenario through the real route, and a test comment that claims only what it asserts | F3; D15; D19; D24; SR-227; TC-336; TC-321 | IF-246; IF-283 | |
| R3 | The round's regression bar: the unchanged relaunch-cancellation, close-down and retention regressions re-run | SR-230; SR-227; TC-318; TC-340; TC-341 | intra-module (no seam changes in this row) | R1; R2 |

## R1 (F1)

- **Class:** the hook interprets a shell command line without the shell's quoting.
- **Sites** (all in `project-trajectory/scripts/coordinator_guard.py`):
  - (a) `command_words` splits segments with the quote-blind `_SEGMENT_BREAK` regex (:869, :939), so a quoted `;` is a boundary;
  - (b) `command_words` tokenizes each segment with the `_TOKEN` regex (:870, :941), which keeps quotes inside words and splits a quoted assignment value (`FOO="two words"` reads command `words`);
  - (c) `_segment_command` / `_past_prefix` (:946, :960, `_OPTION_ARGS` :874) skip `env -S` / `--split-string`'s argument instead of reading it as the command line it is;
  - (d) `command_name` (:916) strips quote characters itself, a second ad hoc unquoting;
  - (e) `model_clis` (:909) tokenizes each `cmd_template` with the same `_TOKEN` regex instead of the kit's one template reader `agent_session.split_cmd` (re-exported by `agent_common`), so a JSON-array template names no CLI.
- **Searches:**
  - `rg -n 'tool_input|get\("command"\)' project-trajectory scripts .claude` -> only `launch_reason` (:892-895) reads a command line;
  - `rg -n '_SEGMENT_BREAK|_TOKEN\b|findall\(' project-trajectory/scripts/coordinator_guard.py` -> sites a, b, e;
  - `rg -n 'def command_name|def _segment_command|def _past_prefix|_OPTION_ARGS' project-trajectory/scripts/coordinator_guard.py` -> sites c, d;
  - `rg -ln PreToolUse project-trajectory/scripts` -> coordinator_guard.py and subagent_gate.py (subagent_gate reads no command: not a site);
  - `rg -n cmd_template project-trajectory/scripts` -> every other reader goes through `agent_session.split_cmd`; `model_clis` is the one exception.
- **Owning boundary:** one quote-aware lexer at the hook's input boundary, per tool dialect (POSIX quoting for Bash; PowerShell's quoting for PowerShell), yielding unquoted words and unquoted operators; `command_words`, the prefix reader and `env -S` consume only its output; `model_clis` reads templates through `split_cmd`. An unreadable line (an unbalanced quote) is a recorded decision in `docs/decisions/wi-834.toml`.
- **As built:** the lexer is `project-trajectory/scripts/kitlib/shell_line.py` (`segments`, `Unreadable`), a separate module because the guard would otherwise pass the 1000-SLOC module ratchet (decision D-011); the guard keeps the command-word reading; the unreadable-line refusal is decision D-010.
- **Pins (red first):** Sol's three cases, the declared prefix and chain forms with quoted values, and the PowerShell quoting cases, in `tests/test_blackout_window.py`.

## R2 (F3)

- **Class:** a blackout test whose comment claims scenario coverage its assertions do not check.
- **Sites:** `tests/test_blackout_window.py:475-487` (`test_a_review_next_or_rework_lane_pauses_at_its_obligation`: claims the handoff names the obligation and a wrap-up verdict asked for the rework; it only makes three refused service calls).
- **Search:** `rg -n -i 'handoff|pause point|rework|review-next' tests/test_blackout_window.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_session_service.py` -> the other hits write a handoff for the relaunch tests, whose assertions check what they claim; :390 checks the close-down text.
- **Owning boundary:** the scenario test through the real route as far as the kit's code carries it: a primary checkout holding the active claim, a lane worktree with committed finished-step evidence, `coordinator_adjudicate`'s wrap-up dispute call admitted inside the window and returning a FIX ruling, the rework BUILD/REVIEW refused by the session service and the builder's `Agent` call denied by the hook until the window ends, then admitted. Writing and reading the handoff is the coordinator's prose, not code; the comment is corrected to claim only what is asserted.

## Exclusions

Excludes: F2; F4; F5 — spine-text findings (SR-227's blackout exception, SR-229's and SR-230's scoping): the spine author reconciles them at the lane's checkpoint (coordinator-cycle skill §3); this builder does not touch the registries.
Excludes: TC-266; TC-267; TC-268; TC-303; TC-322; TC-323; TC-324; TC-329; TC-330 — their modules (session_keep, the adjudicator token, the sign-in probe) are untouched by this round; they run in the smoke tier unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D7; D8; D9; D11; D12; D13; D14; D16; D17; D18; D20; D21; D22; D23; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D43; D44; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's first build round (785a004d) and passed in REVIEW-A's done-when table; this round reopens only F1 and F3.
