# WI-834 rework round 2: coverage plan

Answers `docs/reviews/wi-834/002-REVIEW-A-9bc1eb2-narrow.md` (F1..F3: the three
lines under its "Findings:" heading, in the order written; plan_coverage reads
the same three).

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1: the shell-line lexer keeps a here-document's delimiter quote kind and a here-string's quote kind, and reads the substitutions in an expandable body | F1; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | The round's regression bar: the hook's quoting pins, the unreadable-line refusal and the guard's lease and route regressions re-run unchanged | SR-229; SR-227; SR-230; TC-315; TC-316; TC-317; TC-318; TC-321; TC-340; TC-341 | intra-module (no seam changes in this row) | R1 |

## R1 (F1)

- **Confirmed** on the real code path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-leg03/wi834-f1-probe.py`
  drives `coordinator_guard.hook` with a `PreToolUse` payload, the context
  guard off (`context_guard_pct = 0`, `guard_config(root).enabled` is False)
  and the clock inside an armed `12:00-19:00` window, against this lane's guard
  and the base guard (`git show a2c94eed:...coordinator_guard.py`):

  ```text
  F1-bash  unquoted heredoc <<EOF        base_denied=True  current_denied=False segments=[['cat']]
  F1-pwsh  @"..."@ here-string           base_denied=True  current_denied=False segments=[['Write-Output', '$(\nclaude -p x\n)']]
  ```

  A Bash unquoted here-document and a PowerShell double-quoted here-string
  both execute `$( )` in their bodies; the lane's guard reads neither body and
  allows the launch the base guard denied.
- **Class:** the hook's shell reader treats text the shell will expand as
  inert data.
- **Sites in the class** (all in `project-trajectory/scripts/kitlib/shell_line.py`):
  - (a) `_Scanner._redirect` (:143-151): the here-document target is read by
    `_word()`, which strips its quotes, so `<<EOF` and `<<'EOF'` (`<<"EOF"`,
    `<<\EOF`, `<<E"O"F`) record the same `("EOF", tabs)` entry; the
    delimiter's quote kind, the one fact that decides whether the body
    expands, is lost here and cannot be recovered downstream;
  - (b) `_Scanner._heredoc_bodies` (:153-164): every body is passed over
    unread, expandable or not. Probed: `<<EOF` with a `$( )` body, `<<-EOF`
    with a tab-indented `$( )` body, `<<EOF` with a backtick body, `<<EOF`
    with `${x:-$( )}`, and `cat <<EOF | sh` with a `$( )` body all read
    `[['cat']]` (or `[['cat'], ['sh']]`) and are allowed;
  - (c) `_Scanner._here_string` (:265-272), reached from `_piece` (:175-176)
    by `_HERE_STRING` (:52): `@"` and `@'` bodies alike are returned as one
    inert word; a `$( )` in a `@"` body is never appended to `nested`.
- **Probed and not in the class** (current behaviour, same probe; each is
  already read, or is literal to the shell too):
  - read and denied: unquoted `$( )`; unquoted backticks; Bash `"$( )"` and
    `` "` `" ``; `${x:-$( )}`; `<<< "$( )"`; process substitution `<( )` and
    `>( )` (the `<`/`>` is a redirection, the `(` an operator, so the inner
    command is its own segment); `$"...$( )"`; `{ ...; }` groups; PowerShell
    `"$( )"`, unquoted `$( )`, `@( )` and `& { }` script blocks; `env -S`;
  - literal to the shell and correctly allowed: `<<'EOF'`, `<<"EOF"`,
    `<<\EOF`, `<<E"O"F`, `<<-'EOF'`; Bash `'$( )'` and `$'$( )'`; PowerShell
    `'$( )'`, `` "`$( )" `` and `@'...'@`.
- **Probed, out of the class** (the text is quoted data to this shell and
  is executed only by a second interpreter or a wrapper command; base and
  current guard both allow them, so no regression of this lane): `bash -c
  '...'`, `sh -c "..."`, `eval '...'`, `pwsh -Command "..."`,
  `Invoke-Expression '...'`, `cmd /c claude`, and the wrapper commands
  `nohup`, `exec`, `command`, `xargs`. The guard reads only the declared
  `timeout`/`env` prefixes and does not read scripts (`command_words`
  docstring; LLR-300's declared launch forms). Surfaced to the coordinator
  as a separate observation, not planned here.
- **Searches:**
  - `rg -n "_heredocs|_heredoc_bodies|_here_string|_HERE_STRING" project-trajectory/scripts/kitlib/shell_line.py`
    -> :52, :94, :139, :149-150, :153-164, :175-176, :265-272 (sites a, b, c);
  - `rg -n "def _redirect|def _word|def _double|def _substitution|def _backtick" project-trajectory/scripts/kitlib/shell_line.py`
    -> the readers that do act on substitutions (`_double`, `_substitution`,
    `_backtick`), which an expandable body reuses;
  - `rg -n "shell_line|segments\(" project-trajectory/scripts` -> the only
    consumers are `coordinator_guard.command_words` (:960) and
    `_split_string` (:1011); no other reader of a command line exists;
  - `rg -n "here|<<" tests/test_blackout_window.py` -> the existing pins
    (:385, :395, :396, :445) cover quoted here-documents and one unquoted body
    holding a lone `'`, none an expandable body with a substitution.
- **Owning boundary:** the lexer, `kitlib/shell_line.py`. `_redirect` records
  whether the delimiter word carried any quoting (POSIX: any quote or
  backslash in it makes the body literal); `_heredoc_bodies` reads an
  expandable body as the shell reads it, where `$( )`, backticks and `\`
  act and quotes are literal (so `cat <<EOF\n'; x\nEOF` stays one command, as
  the :445 pin requires), appending its substitutions to `nested`;
  `_here_string` does the same for a `@"` body and keeps `@'` literal. An
  unclosed substitution in an expandable body raises `Unreadable`, refused
  under the existing decision D-010.
- **Why a guard cannot end the class instead:** the quote kind of a
  here-document delimiter exists only at the moment `_redirect` reads the
  target word; `_word()` strips it, and every consumer downstream (the
  guard's `command_words`, its `env -S` reader) receives only `[['cat']]`.
  A check added in `coordinator_guard` would have to re-read the raw line
  with a second, quote-blind reader beside the lexer: it would either deny
  every here-document (re-opening the literal-body over-denial that round
  1's F1 fixed, failing the `QUOTED_ALLOWED` pins) or re-implement the
  lexer's quoting, so two readers would decide one line and can disagree.
  Only the lexer can make an expandable body unreadable-as-data.
- **Pins (red first):** added to the existing parametrised lists in
  `tests/test_blackout_window.py`, not new tests (the smoke tier's
  membership budget):
  - `QUOTED_DENIED`: the reviewer's two F1 commands; `<<-EOF` with a
    tab-indented `$( )`; `<<EOF` with a backtick body; an unquoted
    here-document inside a `$( )`;
  - `QUOTED_ALLOWED`: `<<"EOF"`, `<<\EOF` and `<<-'EOF'` bodies holding
    `$(claude -p x)`, and a `@'...'@` body holding `$(claude -p x)`;
  - `test_the_one_reading_keeps_quoted_text_in_its_word`: an expandable
    body's substitution is read as a further command, and the :445 lone-quote
    body still reads `[["cat"], ["next"]]`.

## R2 (regression bar)

- **Class:** none new; the hook's other readings must not move.
- **Sites:** the unchanged `QUOTED_DENIED` / `QUOTED_ALLOWED` / `UNREADABLE`
  pins, `tests/test_coordinator_guard.py`, `tests/test_coordinator_guard_e2e.py`,
  and the blackout relaunch-cancellation, close-down and retention tests
  (SR-230's TC-318 / TC-340, SR-227's TC-321 / TC-341), which the lexer
  change must not move.
- **Search:** `rg -n "def test_" tests/test_blackout_window.py tests/test_coordinator_guard.py`.
- **Owning boundary:** unchanged; re-run, no edit.

## Exclusions

Excludes: F2 — dismissed: docs/reviews/wi-834/003-ADJUDICATE-f95988a.md#R2F2
Excludes: F3 — spine text (LLR-300's and TC-339's wording of the unreadable-shell-line refusal): the spine author reconciles it at the lane's checkpoint (coordinator-cycle skill §3); this builder does not touch the registries.
Excludes: TC-266; TC-267; TC-268; TC-303; TC-322; TC-323; TC-324; TC-329; TC-330 — their modules (session_keep, the adjudicator token, the sign-in probe) are untouched by this round; they run in the smoke tier unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D7; D8; D9; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D43; D44; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's first build round (785a004d) and its round-1 rework (9bc1eb2a), and not reopened by this round's REVIEW-A; this round reopens only F1 (D10's shell-line reading, D25's guard-off hook denial).
