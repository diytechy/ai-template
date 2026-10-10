# WI-834 rework round 9: coverage plan

Answers `docs/reviews/wi-834/028-REVIEW-A-72615c7.md` (F1, its one
`[MAJOR]` line). Planned at lane tip 2e8b1980. Decision D-025 answers it
with code under dispute sitting 025's ruled line
(`025-ADJUDICATE-22cf09c.md`, D-024): the hook covers the word the shell's
own grammar makes the command. `time` and its options are grammar, so the
timed command is the command word.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1 (D-025, under sitting 025's line): a Bash grammar word's own options (`time -p`, `time --`) are passed over, so the timed command is read as the command word | F1; D7; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | The round's regression bar: the hook-reading pins re-run with R1's added; the item's retention, relaunch and readiness SRs re-run unchanged in the smoke bar | SR-227; SR-230 | intra-module (no seam changes in this row) | R1 |

## R1 (F1)

- **Confirmed** on the real code path, at tip 2e8b1980, by calling
  `coordinator_guard.command_words` (the reading `launch_reason` and so
  `hook` use):

  ```text
  'time -p claude -p x'      -> ['-p']       review form
  'time -p codex exec -'     -> ['-p']       review form
  'time -- claude -p x'      -> ['--']
  'time -p -- claude -p x'   -> ['-p']
  'time -p ! claude -p x'    -> ['-p']
  'if ! time -p claude; then :; fi' -> ['-p', ':', 'fi']
  'time claude -p x'         -> ['claude']   (denied today)
  'coproc claude -p x'       -> ['coproc']
  ```

  The reviewer reproduced the same through `hook()` and the shipped
  stdin/stdout hook CLI.
- **Class:** a grammar word's own options read as the command word.
  `_segment_command` passes over a word in the flat `_RESERVED` set and
  then reads the next word as the command, whatever it is. Bash's grammar
  is `time [-p] [--] pipeline` (`-p` the POSIX output format, `--` ending
  the options), so `-p` / `--` is taken as the command.
- **The grammar words that stand before a command word** (D-025 asks for the
  set derived from the shell's grammar, not `time -p` alone). From bash's
  reserved words: `!`; `time` (options `-p`, `--`); `{`; `if`, `then`,
  `elif`, `else`; `while`, `until`, `do`; `coproc` before a simple command
  (`coproc claude -p x` runs `claude`). `}` is in today's set and stays
  (it is never a command). `case`, `for`, `select`, `in`, `function`,
  `[[` take words or a name, not a command: the reader already finds the
  command after `case ... a)` and `do`, and their own first words are not
  model CLIs. `coproc NAME { claude; }` runs its body as a coprocess, so
  it is grammar inside sitting 025's line: after `coproc`, a word followed
  by a compound-command opener is the coprocess's NAME. The reader splits
  at `(` but not at `{` (`coproc N { claude -p x; }` is one segment,
  `coproc N ( claude -p x )` is `[coproc N]` then `[claude -p x]`), so
  only the `{` NAME skip is needed; the `(` body is already its own simple
  command. `function f { claude; }` defines a function and runs nothing, so
  it stays allowed (see Excludes). PowerShell's grammar before a command word (the `&` and
  `.` invocation operators, the assignment operators) was built in rounds
  016-024 and is not touched.
- **Sites** (every reader of `_RESERVED`, found by
  `rg -n "_RESERVED\b" project-trajectory scripts tests`): one,
  `coordinator_guard.py` `_segment_command`. No other module or test holds
  its own copy of the list (`trace.py`'s `_RESERVED_APPROVAL_SCOPES` is an
  unrelated name).
- **Owning boundary:** one declared table in `coordinator_guard.py`,
  `_GRAMMAR_WORDS`: each grammar word that stands before a command word,
  mapped to its shape, the option words it takes and the openers before
  which one word is its NAME (`time`: options `-p`, `--`; `coproc`: a NAME
  before `{`; the others: nothing). One helper, `_past_grammar`, reads the
  table and returns the index past a grammar word and its shape's words;
  `_segment_command` calls it and reads the next word as usual.
  `_RESERVED` goes away. The PowerShell branch, the `timeout` / `env`
  prefixes and every wrapper form stay as they are.
- **Pins (red first),** in TC-339's existing `QUOTED_DENIED` /
  `QUOTED_ALLOWED` tables (no new test, the smoke membership budget):
  `time -p claude -p x`, `time -p codex exec -`, `time -- claude -p x`,
  `time -p -- claude -p x`, `coproc claude -p x`,
  `coproc NAME { claude -p x; }` denied; `time -p echo ok`,
  `coproc NAME { echo ok; }`, `function f { claude; }` allowed.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-317; TC-318; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-340; TC-341; TC-342; TC-343; TC-344; TC-345 — the retention, relaunch, sign-in, adjudication, readiness and hook opt-in paths are untouched by round 9 (F1 is the hook's launch reading only); they run in their tiers unchanged.
Excludes: F1 — the wrapper forms (Start-Process, Invoke-Expression/iex, cmd /c, sh -c, exec, command, builtin, nohup, xargs, script files) take a command as an argument, so they are outside the declared any-command-word coverage by dispute 025's ruling (D-024); not changed. `function NAME { ... }` defines a function and runs nothing, so it is not a launch; it is pinned allowed so the reading is deliberate.
Excludes: D1; D2; D3; D4; D5; D6; D8; D9; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D43; D44; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (through round 8 and sitting 025) and not reopened by round 028, which reopens only the hooks' launch reading (D7/D10/D25, F1).
