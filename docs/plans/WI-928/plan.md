# WI-928 implementation plan: the blackout hook drops the rare shell forms

Spec: `docs/work/active/wi-928/WI-928-blackout-drops-rare-forms.md`. Specref:
`docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`
(ruling D-011; filing calls D-016).

DELTA: none

The architectural-delta answer: the WI removes recognition, and does none of
the four. It adds no state, no domain value, no input and no boundary. The
hook still reads the same IF-274 payload (`tool_input.command`) and answers in
the same IF-275 shape, and both rows stay unchanged. The only surface that
changes is `kitlib.shell_line.Word`, and it gets narrower: `spans` and
`quoted(i)` are replaced by one offset. Its only consumer is
`coordinator_guard.py` (grep: no other module or test imports `shell_line`
except the bootstrap manifest, which ships the file by path). No interface row,
domain or component split is owed.

## Cited registries (checked, unchanged unless a row says otherwise)

- SR rows, `docs/requirements/system-requirements.toml`: **SR-229**
  (claim admission respects a blackout pause; names no shell form) and
  **SR-237** (blackout pauses new model work; rests on the session service's
  admission at every kit launch point). Both are unchanged (Spine section).
- TCs verifying them, `docs/test/test-cases.toml`: TC-315, TC-316, TC-317
  (SR-229), TC-335, TC-336, TC-337, TC-338, TC-341 (SR-237), and **TC-339**
  (both, the only TC whose text this WI amends).
- Interfaces, `docs/requirements/interfaces.toml`: IF-274 (hook stdin payload)
  and IF-275 (hook stdout denial shape), both owned by
  `scripts/coordinator_guard` under CMP-008, both unchanged. IF-271
  (`claim_refusal`) is not crossed.
- Components, `docs/requirements/components.toml`: CMP-008 (W3 Autonomy)
  holds the guard; no component change.
- Runtime flows, `docs/runtime-flows.md`: Flow 5 ("The blackout window on
  both routes") draws the hook as "deny Agent, SendMessage, a model CLI" and
  names no shell form, so it stays as it is.

## Plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Dot invocation goes (deliverable 1) | D1; D3; SR-229; TC-339 | IF-274; IF-275 | |
| P2 | Grammar table back to one flat reserved-word set (deliverable 2) | D1; D2; D3; SR-229; TC-339 | IF-274; IF-275 | P1 |
| P3 | Here bodies are data again (deliverable 3) | D1; D3; SR-229; TC-339 | intra-module: `kitlib/shell_line.py` internals, no interface | P2 |
| P4 | Assignment reading shrinks to the ordinary capture (deliverable 4) | D1; D3; SR-229; TC-339 | IF-274; IF-275 (the `Word` narrowing is intra-module, no interface row) | P1; P3 |
| P5 | env's split string goes (deliverable 6) | D1; D3; SR-229; TC-339 | IF-274; IF-275 | P4 |
| P6 | The bound stated once in `launch_reason`; module docstrings trimmed (deliverable 5, prose) | D1; D4; SR-229 | intra-module: docstrings and comments only, no interface | P5 |
| P7 | LLR-300 and TC-339 amended (deliverable 5, spine) | D5; SR-229; SR-237; TC-339 | intra-module: registry text only, no interface | P6 |
| P8 | RESYNC_PACK entry (deliverable 5, resync) | D6; SR-229 | intra-module: prose only, no interface | P7 |
| P9 | The bar on the landing tip | D1; D2; D3; D7; SR-229; SR-237; TC-315; TC-316; TC-317; TC-335; TC-336; TC-337; TC-338; TC-339; TC-341 | IF-274; IF-275 | P8 |

Each of P1–P5 is one lane commit, in the spec's order (1, 2, 3, 4, then 6).
P6–P8 may be one commit or three; P9 is verification, not a commit.

### Per-step regression bar (applies to P1–P5)

Before each step, and again after it, run in the foreground:

    python -m pytest -q tests/test_blackout_window.py -k "quoted or hooks or unreadable or one_reading" -p no:cacheprovider

It is green before each step (the cases about to go are still recognised)
and green after (those cases were deleted in the same commit, and every kept
case still passes). A step whose code removal is committed without its pin
deletion goes red, so code and pins move together in one commit. No step adds
a test. **No test fails before the change, by design (D3):** a removal
promises no new behaviour, the kept cases pin what survives, and the removed
forms are deliberately not pinned as allowed. No case moves from
`QUOTED_DENIED` to `QUOTED_ALLOWED`.

## P1 — Dot invocation goes

`project-trajectory/scripts/coordinator_guard.py`:
- delete `_invoked` (it reads `words[0].spans`, which is why it goes before
  P4);
- `command_words`: `found = [_assigned(words) for words in found]`.

A leading `.` is then the command word (`command_name(".")` is `"."`), so the
line is not a launch. `&` stays denied because the reader splits at it
(`DENIED`'s `& "C:\Tools\codex.exe"` and `QUOTED_DENIED`'s
`& "C:\Program Files\codex.exe"` are the pins).

`tests/test_blackout_window.py`: delete from `QUOTED_DENIED` the comment and
the three cases `. claude -p x`, `. 'claude' -p x`, `$r = . claude -p x`;
delete from `QUOTED_ALLOWED` `. ./setup.ps1`.

## P2 — One flat reserved-word set

`coordinator_guard.py`:
- replace `_NO_SHAPE` and `_GRAMMAR_WORDS` (and their comment) with
  `_RESERVED_WORDS = frozenset({"!", "{", "}", "if", "then", "else", "elif",
  "do", "while", "until", "time"})` and a one-line comment: shell reserved
  words that stand before a command and are never one. `coproc` is not in it
  (a coprocess named after a model CLI would otherwise be denied);
- delete `_past_grammar`;
- `_segment_command`: the first branch becomes part of the skip branch:
  `if name in _RESERVED_WORDS or _ASSIGNMENT.match(words[i]) or not name:
  i += 1`. Its docstring loses "grammar words with their shapes
  (`_past_grammar`)" and says "reserved words".

`time claude` stays denied because `time` is in the set; `if true; then
claude -p x; fi` (kept) pins the set's ordinary use.

Tests: delete from `QUOTED_DENIED` the two comments and the eight cases
`time -p claude -p x`, `time -p codex exec -`, `time -- claude -p x`,
`time -p -- claude -p x`, `coproc claude -p x`, `coproc NAME { claude -p x; }`,
`coproc WORK while ...`, `coproc WORK if ...`; delete from `QUOTED_ALLOWED`
`time -p echo ok`, `coproc NAME { echo ok; }`,
`coproc CLAUDE while true; ...`. `function f { claude; }` stays.

## P3 — Here bodies are data again

`project-trajectory/scripts/kitlib/shell_line.py`:
- delete `_Scanner._expansions`;
- `_redirect`: drop `start` and the quoted-delimiter test; append
  `(target, match.group(1) == "<<-")` to `self._heredocs`;
- `_heredoc_bodies`: for each `(delimiter, tabs)`, call
  `self._heredoc_body(delimiter, tabs)` and discard the body (no read
  branch). The body is still found to its delimiter line, so the line after
  it is still read;
- `_here_string`: delete the `if quote == '"':` read branch. It still finds
  the closing line and raises `Unreadable` when there is none (the
  `UNREADABLE` list and LLR-300's closed unreadable list keep that).

Tests: delete from `QUOTED_DENIED` the five here-body cases
(`cat <<EOF\n$(\nclaude -p x\n)\nEOF`, `cat <<-EOF ...`, the backtick
body, `x="$(cat <<EOF ...)"`, `Write-Output @"\n$(...)\n"@`); delete from
`QUOTED_ALLOWED` the four controls `cat <<"EOF"`, `cat <<\EOF`,
`cat <<-'EOF'`, `Write-Output @'\n$(claude -p x)\n'@`; delete from
`test_the_one_reading_keeps_quoted_text_in_its_word` the assertion that
`cat <<EOF\n'$(claude -p q)'\nEOF` reads `["claude", "-p", "q"]`. Kept: the
body-is-data assertion just above it, the `cat > notes.md <<'EOF' ... EOF\nclaude -p x`
denial (line after a body), and the quoted-separator cases `cat > handoff.md <<'EOF'`,
`git commit -m "$(cat <<'EOF' ...)"`, `git commit -m @'...'@`.

## P4 — The assignment reading shrinks to the ordinary capture

**The choice between the spec's two readings: the current operator scan, with
spans gone.** It is the smaller change: it keeps `_assigned`, `_operator_end`
and `_tail` in shape and replaces a span list with one offset, while a
variable-target reading would add a new target grammar (a regex for typed,
scoped and comma-list targets) to pin the same kept set. It adds no check
whose job is to stop reading property or index targets; it may still catch
some, which the declared default allows.

`kitlib/shell_line.py`:
- `Word`: delete `spans` and `quoted`; add the class attribute
  `quote_start = None`, the offset where the word's first quoted piece
  starts; `opens_quoted` becomes `return self.quote_start == 0`;
- `_word`: track only the first quoted piece's start
  (`if quoted and start is None: start = size`) and set
  `word.quote_start = start`; its docstring says so;
- the module docstring's `spans` paragraph is rewritten in P6.

`coordinator_guard.py`:
- `_operator_end`: the first `_PS_OPERATOR` match that ends at or before
  `word.quote_start` (any match when it is None), else None. So
  `$x -match 'a=claude'` finds none (its quote starts at 0) and
  `$r='claude -p x'` finds the `=` ending at 3, its quote's start;
- `_tail`: `shell_line.Word(word[at:])` with `quote_start` rebased to
  `word.quote_start - at` when set (never negative, because the operator ends
  at or before it);
- `_right_hand`: delete the chained-assignment recursion; a right-hand side
  opening with a quoted piece or with `$` is a value (`return []`);
- `_assigned`'s docstring: drop "(standalone, or written against a word)"
  wording that described per-character quotedness, keep "unquoted
  operator before any quoted piece of its word".

Kept pins this must hold (all in today's lists, all green before):
`$response = claude -p x`, `[string]$r = claude -p x`, `$a, $b = claude -p x`,
`$r += claude -p x`, `$env:X = claude -p x`, `$r ??= codex exec -`,
`$r=claude -p x` denied; `$env:FOO = 'a b'; claude -p x` denied (second
statement); `$r = 'claude -p x'`, `$r = "claude -p x"`, `$r='claude -p x'`,
`$r = $other`, `echo a = claude`, `$x -match 'a=claude'` allowed.

Tests: delete from `QUOTED_DENIED` the two comments and the eleven cases
`$result.Answer = ...`, `$answers[0] = ...`, `[string[]]$answers = ...`,
`$a.b[1].c = ...`, `[System.Collections.Generic.List[string]]$l = ...`,
`$h['k=v'] = ...`, `$r =claude -p x`, `$a = $b = claude -p x`,
`$h['answer']=claude -p x`, `$o.'Answer'=claude -p x`, `$o."A"=claude -p x`;
delete from `QUOTED_ALLOWED` `$result.Answer = "claude -p x"` and
`$answers[0] = 'claude -p x'`. Trim the comment above sitting 017's table to
name only that table.

## P5 — env's split string goes

`coordinator_guard.py`:
- delete `_split_string`;
- `_past_prefix` returns the index only (no split branch); its docstring
  loses the split string;
- `_segment_command`: `i = _past_prefix(words, i + 1, name)` (the
  recursion into `["env"] + split` goes);
- `_OPTION_ARGS`' comment loses "(env's split string is read by
  `_split_string`)".

The plain `env` prefix and its options stay (`env -u BAR FOO=1 claude -p x`
in `DENIED` is WI-834's Done-when pin).

Tests: delete from `QUOTED_DENIED` `env -S 'claude -p x'`,
`env --split-string='FOO=1 codex exec -'`, `env -i -S'claude -p' x`; the
comment above `QUOTED_DENIED` loses "env's split string is itself a command
line" and "a here-document body" (P3's removal).

## P6 — The bound, stated once

`coordinator_guard.launch_reason`'s docstring replaces "naming a model CLI as
any command word" with the enumerated set of "The bound" (start of a simple
command; after `VAR=value`; after `timeout`/`env` and their options; after
the flat reserved words; across `&&`, `||`, `;`, `|`, newlines; after
PowerShell's `&`; in `$(...)` or backtick substitutions in the line or inside
double quotes; on the right of a PowerShell assignment to a variable, plain,
typed, scoped, comma list or compound operator), the unreadable-line denial,
the default ("a form outside this set gets no dedicated recognition: it may
incidentally match the retained reading, and carries no guarantee either
way"), and the residue list (here-document and here-string bodies; property,
index and chained assignment targets; dot invocation; options of reserved
words; env's split string; `coproc`; wrapper commands such as `sh -c`, `iex`,
`Start-Process` and script files). It keeps the `model_clis` and D-010
sentences.

Other docstrings lose their sentences about removed forms and **restate no
residue** (D4):
- `command_words`: "the shell's reserved words" for "grammar words", drop
  "and env's split string"; point to `launch_reason` for the bound;
- `shell_line` module docstring: "here-document bodies (to their delimiter
  line)" becomes "here-document bodies, passed over as data to their
  delimiter line"; the `@"` here-string is listed as data; delete the
  paragraph on expandable bodies (REVIEW-A round 2) and rewrite the `spans`
  paragraph as "each word is a `Word`: its text plus `quote_start`, where its
  first quoted piece starts, which tells PowerShell's `$r = 'claude'` (a
  value) from `$r = claude` (a command)". The WHY paragraph's historical
  `env -S` example is replaced by the quoted-assignment and quoted-semicolon
  examples it already has;
- the `_PS_OPERATOR` comment loses "so property, index, typed, scoped and any
  other target form is covered".

Check for D1 and D4 after P6 (from the lane root):

    git grep -n -e _invoked -e _GRAMMAR_WORDS -e _past_grammar -e _NO_SHAPE -e _expansions -e "\.spans" -e "\.quoted(" -e _split_string -- project-trajectory/

must print nothing (it prints matches on trunk, so it fails before the
change). For D4, `git grep -n -i "coproc\|dot invocation\|split string" --
project-trajectory/scripts` must hit only `launch_reason`'s docstring (the
WI-834 RESYNC entry is history and stays; the new entry in P8 names no
residue).

## P7 — LLR-300 and TC-339 amended

`docs/requirements/low-level-requirements.toml`, `[design.LLR-300]`:
- `detail`: replace the span from "One quote-aware shell reading per dialect
  reads quoted assignments and env split strings as the shell does, ..."
  through "... and keeps quoted bodies as data;" with the spec's block
  verbatim, its last sentence ending "...carries no guarantee either way.";
  the following " window_check exits nonzero inside it." stays as is (flag
  for the sitting: after the new sentences, "it" reads less clearly as the
  window; the spec says the rest of the cell is unchanged, so the plan does
  not reword it);
- `code_symbol`: drop `/_invoked`; nothing else.

`docs/test/test-cases.toml`, `[test.TC-339]`: `method` and `expected` take
the spec's replacements verbatim; `evidence` unchanged (the same test
functions remain).

Edit the cells byte-exactly (one guarded replace per cell, asserting the old
span occurs once, LF kept). SR-229, SR-237, IF-274 and IF-275 are not edited.
Status handling of the two Approved rows follows the in-lane spine
reference; both rows are judged at the lane's checkpoint sitting. WI-926 may
also edit LLR-300's `code_symbol`: whichever lands second rebases its cell
edit.

Then:

    python project-trajectory/scripts/check_trajectory.py --strict
    python project-trajectory/scripts/trace.py --strict-integrity

both clean.

## P8 — RESYNC_PACK entry

Append to `project-trajectory/RESYNC_PACK.md`, after the last `###` entry
and before "## 5. Promotion", an entry in the pack's shape:

- heading `### The blackout hook stops recognising rare shell forms [since <sha>]`,
  `<sha>` the trunk commit the lane is based on
  (`git merge-base HEAD <trunk>`), re-anchored if the lane is rebased before
  landing, with the "*(Anchored at the preceding commit...)*" line;
- **What changed**: the hook's shell reading keeps its quote-aware reading
  and the ordinary PowerShell capture, and drops dedicated recognition of the
  forms D-011 ruled contrived; it points to `launch_reason`'s docstring for
  the bound rather than restating the residue (D4), and names none of the D1
  symbols;
- **Kit-owned files — overwrite:** `scripts/coordinator_guard.py` and
  `scripts/kitlib/shell_line.py`;
- **What to do**: overwrite them; the change shows only once an adopter arms
  a blackout window (`[policies] blackout`); nothing needs migrating (no
  registry, setting or record format changes). The WI-834 entry stays as
  history.

## P9 — The bar on the landing tip

From the lane root on the landing tip:

    run.cmd smoke

(the smoke tier, `trace.py --strict`, `check_trajectory.py --strict`,
`check_docs.py --stale`, then `scripts/check_smoke_budget.py --mode enforce`,
the 60 s budget), and

    python -m pytest -q tests/test_blackout_window.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_bootstrap.py

(`test_bootstrap.py` because the manifest still ships `shell_line.py`; the e2e
module is in `SLOW_MODULES`, so it runs here and not in the smoke tier). Paste
the real output. The test count of the smoke tier does not change: only list
entries and one assertion go, no test function.

TCs this bar runs, all unchanged in text except TC-339:
- TC-339: `test_blackout_window.py`'s hook, quoted, unreadable and
  one-reading tests, the amended verification of this WI;
- TC-315, TC-316, TC-317 (SR-229): `test_coordinator_guard.py`,
  `test_blackout_window.py`, `test_coordinator_guard_e2e.py` (and
  `test_session_keep.py` for TC-317 via the smoke tier) run as regressions;
  the hook payload and denial shape they drive are unchanged;
- TC-335, TC-336, TC-337, TC-338, TC-341 (SR-237): `test_blackout_window.py`
  window, launch-boundary, loop, dispatcher and keep-warm tests run as
  regressions; this WI touches none of those routes, which is the spec's
  ground for SR-237 staying unchanged.

D1 is re-checked here with the `git grep` of P6, D2 by reading
`_RESERVED_WORDS` (contains `time`, not `coproc`), D3 by the lists matching
the spec's kept and deleted inventories.
