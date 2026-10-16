+++
id = "WI-928"
title = "The blackout hook stops reading the rare shell forms built for contrived findings, and keeps its quote-aware reading"
workstream = "process"
sr_refs = ["SR-237", "SR-229"]
specref = "docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Context

The owner ruled (coordinator-2026-10-15 D-011) that WI-834's blackout hook
grew shell-grammar forms for findings no agent or supported route produces:
a model call in a here-document's or here-string's substitution, a
PowerShell assignment to a property, index or typed-array target, PowerShell
dot-sourcing of a CLI, Bash `time -p`, and Bash `coproc`. Each came from one
review round, and two came from dispute sittings (025 and 031, both FIX).
The cause was a promise over an open input space: "a model CLI as any command
word", which sitting 025 read as "the word the shell's own grammar makes the
command". After that, every rare grammar form counted as stated behaviour.
The audit (the `specref`) has the cost and the per-finding reasons. The
original rationale for each form is in this row's planner notes.

The ruling keeps the quote-aware reading. It is the fix that stops a harmless
quoted mention, such as `echo 'pause; claude notes'`, from being denied while
the coordinator closes down. Also kept: the ordinary PowerShell capture
`$r = claude -p x`, which sitting 017 ruled in scope and the audit grades
plausible.

**This row removes. It adds no guard.** Removing these forms reopens nothing
a supported route reaches. Every kit-owned launch point already refuses
inside an armed window, before any shell text matters:
- the session service's admission refuses every launch except the wrap-up
  adjudication of an active claim;
- every claim route refuses, and the dispatcher holds;
- keep-warm sends no ping;
- a coordinator launch script calls `window-check`.

The hook covers only a model CLI that an agent types straight into its shell
tool. WI-834's ruling (f) made that stop encouraged, not enforced. After this
row, the hook still denies the forms an agent actually writes.

**The by-construction alternative is not in this row.** D-011 names it:
refuse model work at the launch point during a blackout instead of parsing
shell text. For every kit route this already exists. A CLI typed straight
into the agent's shell has no kit-owned launch point, so building the
alternative there would be new mechanism. It is not built (D-016).

## Deliverables

Each removal is one lane commit, in this order. Item 1 goes before item 4
because the dot-invocation reader checks the quoted-span field that item 4
deletes.

1. **Dot invocation goes.** Delete `coordinator_guard._invoked` and its call
   in `command_words`. A leading `.` is read as the command again, so the
   line is not a launch. `&` stays denied, because the reader already splits
   at it.
2. **The grammar table goes back to a flat set (`time -p` and `coproc`
   together).** `_GRAMMAR_WORDS`, `_NO_SHAPE` and `_past_grammar` exist only
   for `time`'s options and `coproc`'s NAME. They are replaced by one
   frozenset of reserved words that `_segment_command` skips: `!`, `{`, `}`,
   `if`, `then`, `else`, `elif`, `do`, `while`, `until` and `time`. `time`
   stays in the set, so plain `time claude` is still denied. `coproc` is not
   added to it: if it were, a coprocess named after a model CLI would be
   denied wrongly.
3. **Here bodies are data again.** In `kitlib/shell_line.py`, delete the
   expandable-body reader (`_expansions`), the quoted-delimiter test in
   `_redirect`, the read branch in `_heredoc_bodies`, and the `@"` read
   branch in `_here_string`. A here-document body is still found to its
   delimiter line and skipped, so the line after it is still read. A
   here-string is still lexed to its closing line, and an unclosed one is
   still unreadable.
4. **The assignment reading shrinks to the ordinary capture.** Delete the
   per-character quoted spans (`Word.spans`, `Word.quoted`, the span list in
   `_word`, and the span rebasing in `_tail`) and the chained-assignment
   recursion in `_right_hand`. A word records only where its first quoted
   piece starts, which is all the kept forms need. The plan picks the smaller
   of two readings, as long as it pins the kept set:
   - the current operator scan, with spans gone;
   - a variable-target reading like the one sitting 017 first approved.

   It must not add a check whose only job is to stop reading property or
   index targets. Those targets are outside the promise, and a reading may
   still catch them.
5. **The bound, stated once.** `launch_reason`'s docstring lists what the
   hook reads, and states once the default for any other form and the
   residue (both in "The bound" below). The module docstrings of
   `shell_line.py` and `coordinator_guard.py` lose their sentences about
   the removed forms. LLR-300 and TC-339 are amended (Spine).
   `RESYNC_PACK.md` gets a new entry. The WI-834 entry stays as history.
6. **env's split string goes.** Delete `coordinator_guard._split_string` and
   its use in `_past_prefix`, so `env -S`, `-S'...'` and `--split-string`
   are no longer read as more of env's arguments. The plain `env` prefix and
   its options stay, because WI-834's Done-when names them.

### The bound (S3)

The hook's promise is an enumerated set with a declared default, over what
agents write and kit routes produce. Inside an armed window, the hook denies
a main session's line when its model-CLI command word is in one of these
places:
- at the start of a simple command;
- after `VAR=value` words;
- after the `timeout` and `env` prefixes with their options;
- after the flat reserved words;
- across `&&`, `||`, `;`, `|` and newlines;
- after PowerShell's `&`;
- in a `$(...)` or backtick substitution written in the line or inside
  double quotes;
- on the right of a PowerShell assignment to a variable, whether plain,
  typed, scoped, a comma list, or a compound operator such as `+=` or `??=`.

It also denies a line it cannot read. **Default: a form outside this set
gets no dedicated recognition. It may incidentally match the retained
reading, and carries no guarantee either way.** The enumerated forms are
the positive denial promise. The residue, each form under that default,
stated in `launch_reason`'s docstring:
- here-document and here-string bodies;
- property, index and chained assignment targets;
- dot invocation;
- options of reserved words;
- env's split string;
- `coproc`;
- wrapper commands (`sh -c`, `iex`, `Start-Process`, script files).

The rubric's "deny by default" construction for an open grammar is the
by-construction alternative, which is not built (D-016).

## Spine

- **LLR-300 (Approved): amended.** In `detail`, the sentence that begins
  "One quote-aware shell reading per dialect reads quoted assignments and env
  split strings as the shell does, reads a PowerShell assignment, recognised
  by an unquoted assignment operator wherever it stands ..." and ends "...
  and keeps quoted bodies as data;" is replaced by:

  > One quote-aware shell reading per dialect reads quoted values as the
  > shell does, and treats quoted separators, comments and here-document and
  > here-string bodies as data. It finds the model-CLI command word after
  > leading variable assignments, the timeout and env prefixes, the shell's
  > reserved words, the chain operators and the call operator, and in
  > substitutions written in the line or inside double quotes. It reads a
  > PowerShell assignment to a variable as running its right-hand command,
  > while a quoted or variable right-hand value stays data. A form outside
  > this list gets no dedicated recognition: it may incidentally match this
  > reading, and carries no guarantee either way.

  `code_symbol` drops `_invoked`. The rest of the cell is unchanged.
- **TC-339 (Approved): amended.**
  - `method`: "PowerShell assignments of any target form (property, index,
    array-type, scoped, comma list, chained), with the operator spaced or
    written against a word that holds a quoted piece, ... expandable and
    literal here bodies" becomes "PowerShell assignments to a variable
    (plain, typed, scoped, comma list, compound operator) with command,
    quoted and variable right-hand sides, here-document and here-string
    bodies".
  - `expected`: "PowerShell assignments whose right-hand side runs a model,
    and expandable bodies that launch a model are denied; quoted bodies and
    quoted or variable right-hand values are allowed" becomes "PowerShell
    assignments to a variable whose right-hand side runs a model are denied;
    here-document and here-string bodies and quoted or variable right-hand
    values are allowed".
  - `evidence` is unchanged: the same test functions stay, with shorter
    case lists.
- **SR-229 (Approved): unchanged.** It covers claims and the lease, and
  names no shell form.
- **SR-237 (Approved): unchanged.** Its "starting no model work inside the
  window" rests on the service's admission at every kit launch point. The
  hook is supervision.
- **IF-274 and IF-275 (Drafted): unchanged.** Neither the payload nor the
  response shape changes, and IF-275's text names no form.

Both amended rows are judged at the lane's checkpoint sitting.

## Tests

All pins are in `tests/test_blackout_window.py` (grep shows no other test
names these forms).

- **Deleted from `QUOTED_DENIED`:**
  - here bodies: the five here-document and here-string substitution cases;
  - assignments: `$result.Answer`, `$answers[0]`, `[string[]]$answers`,
    `$a.b[1].c`, `[System.Collections.Generic.List[string]]$l`,
    `$h['k=v']`, `$r =claude`, `$a = $b = claude`, `$h['answer']=claude`,
    `$o.'Answer'=claude`, `$o."A"=claude`;
  - dot invocation: `. claude -p x`, `. 'claude' -p x`, `$r = . claude -p x`;
  - `time`: the four `time -p` and `time --` cases;
  - `coproc`: the four coproc cases.
- **Deleted from `QUOTED_ALLOWED`** (each was there only as a control for a
  removed reading): the four quoted-delimiter and `@'` here-body controls,
  `$result.Answer = "claude -p x"`, `$answers[0] = 'claude -p x'`,
  `. ./setup.ps1`, `time -p echo ok`, `coproc NAME { echo ok; }` and
  `coproc CLAUDE while true; ...`.
- **Deleted from `test_the_one_reading_keeps_quoted_text_in_its_word`:** the
  assertion that reads `$(claude -p q)` out of an unquoted here-document
  body. The body-is-data assertion just above it stays.
- **Kept, unchanged, as regression pins:** `DENIED`, `ALLOWED`, `UNREADABLE`
  and every other `QUOTED_*` case. That includes:
  - `FOO="two words" claude`, the `timeout` and `env -u` prefixes,
    `out=$(claude -p q)` and `echo "$(codex exec -)"`;
  - the line after a quoted here-document body;
  - sitting 017's assignment table, with `??=` and `$r=claude`;
  - the quoted and variable right-hand values;
  - `echo a = claude` and `$x -match 'a=claude'`;
  - `function f { claude; }`;
  - every quoted-separator case.
- **Deleted with env's split string (deliverable 6):** the three `env -S`
  cases (`env -S 'claude -p x'`, `env --split-string='FOO=1 codex exec -'`,
  `env -i -S'claude -p' x`).

No test is inverted. Removed forms are not pinned as allowed, so they stay
outside the promise rather than becoming new promises.

## Done-when

- On the landing tip, none of these names appears in `project-trajectory/`:
  `_invoked`, `_GRAMMAR_WORDS`, `_past_grammar`, `_NO_SHAPE`,
  `_expansions`, `.spans`, `.quoted(`, `_split_string`. Each one is present on today's trunk, so the check
  fails before the change.
- `_segment_command` skips one flat frozenset of reserved words. That set
  contains `time` and does not contain `coproc`.
- Every kept case listed under Tests passes, and every case listed as
  deleted is gone from the file. The kept cases pass before the change too,
  because a removal promises no new behaviour. They pin that the quote-aware
  reading and the ordinary capture survive. None of the removals has a
  behaviour test that fails before the change: what changes is that a rare
  form loses its dedicated recognition, and the row deliberately does not
  pin that.
- `launch_reason`'s docstring states the enumerated set, the default and
  the residue, as in "The bound". No other file restates the residue.
- LLR-300 and TC-339 carry the amended text, judged at the lane's checkpoint
  sitting. `check_trajectory.py --strict` and `trace.py --strict-integrity`
  are clean.
- `RESYNC_PACK.md` has a new entry anchored at a trunk commit. It names
  `scripts/coordinator_guard.py` and `scripts/kitlib/shell_line.py` as
  kit-owned files to overwrite, says the change shows only once an adopter
  arms a blackout window, and says nothing needs migrating.
- The bar is green on the landing tip: the smoke tier and the smoke budget
  check, plus `tests/test_blackout_window.py`,
  `tests/test_coordinator_guard.py`, `tests/test_coordinator_guard_e2e.py`
  and `tests/test_bootstrap.py` (the MAPPING still ships `shell_line.py`).

## Scope answers

- **S1, the deliverables.** Four removals could each land alone: dot
  invocation; the grammar table (`time -p` and `coproc` must go together,
  because one table and one helper exist only for the two); here bodies; and
  the assignment machinery. The row keeps them together on purpose:
  - all four edit the same two modules and the same two test lists;
  - all four touch the one LLR-300 `detail` cell and the one TC-339
    `method`/`expected` pair, and owe one RESYNC entry;
  - four rows would mean four critiques and four checkpoint sittings on one
    cell.

  They land as one lane commit each, in the order 1, 2, 3, 4 (1 before 4,
  see Deliverables), then deliverable 6, env's split string.
- **S2, authority over a hold, act or gate.** None. No file gains authority.
  The hook's denial is narrowed, not handed to a file, so the row needs no
  `## Trust` section.
- **S3, closed coverage.** See "The bound": an enumerated set with a declared
  default (no dedicated recognition, no guarantee either way), over what
  agents write and kit routes produce, with the residue stated once.
  Deny-by-default, the by-construction alternative, is not built (D-016).
- **S4, the planning need.** `single`: the row promises behaviour over an
  input space (shell lines), and deliverable 4 leaves the plan a choice
  between two readings.
- **S5, the architectural delta.** Removal only. It adds no state, domain
  value, input or boundary. `shell_line.Word`'s public surface narrows
  (`spans` and `quoted` go). Its only consumer is `coordinator_guard.py`
  (grep).
- **S6, dependencies.** `needs = []`. WI-926 (queued) also edits
  `coordinator_guard.py` (the hook opt-in functions and `kitlib/guard_hooks.py`)
  and may amend LLR-300's `code_symbol`. The functions are different and the
  cell is shared, so whichever row lands second rebases its cell edit. No
  new package, tool or service.
- **B1, no hidden deliverable.** Context commits to nothing the Done-when
  leaves out. The alternative is explicitly left out.
- **B2, the minting rule.** No split is proposed: one row (D-016).
- **B3, a consumer that re-derives a decision.** None.
- **B4, owner-dependent work.** None beyond the lane's normal checkpoint
  sitting.

## Calls ruled at filing

The owner's rulings, coordinator-2026-10-15 D-016 (each as recommended):

1. **env's split string** (`env -S '...'`, `--split-string`) goes with the
   grammar forms, as deliverable 6, with its three pins deleted and
   LLR-300's first sentence dropping "and env split strings". The plain
   `env` prefix stays, because WI-834's Done-when names it.
2. **Chained assignment and an operator written against the right-hand
   side** (`$a = $b = claude`, `$r =claude`) go with deliverable 4, as
   drafted. Sitting 017's ordinary capture stays.
3. **The by-construction alternative** (refuse model work at the launch
   point instead of parsing shell text) is not built: every kit launch point
   already refuses inside an armed window, and the hook stays supervision
   under WI-834's ruling (f).
4. **S1:** one row, one lane commit per removal in the drafted order (dot
   invocation before the assignment reading, whose quoted spans it reads).

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-16; CHANGES-REQUESTED, one finding):

- **S3, MAJOR: adopted.** Deliverable 4 let the retained assignment reading
  catch property or index targets, while "The bound" and the proposed
  LLR-300 text said every other form is "not read and not denied". One
  recognizer-level rule replaces that default everywhere it was stated.
  "The bound" reads "Default: a form outside this set gets no dedicated
  recognition. It may incidentally match the retained reading, and carries
  no guarantee either way." and "The enumerated forms are the positive
  denial promise. The residue, each form under that default, stated in
  `launch_reason`'s docstring"; the proposed LLR-300 sentence reads "A form
  outside this list gets no dedicated recognition: it may incidentally
  match this reading, and carries no guarantee either way"; deliverable 5's
  docstring contract "states once the default for any other form and the
  residue"; S3 reads "a declared default (no dedicated recognition, no
  guarantee either way)"; and the Done-when reads "a rare form loses its
  dedicated recognition".
