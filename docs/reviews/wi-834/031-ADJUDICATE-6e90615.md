# WI-834 adjudication 031: dispute R30F1 (range 2e8b1980..a3658d32)

Scope bound: PROCESS.md §6 "Review threat model". Review covers a normal
working environment: content agents write, supported configurations, and
regressions of supported behaviour. It excludes contrived reproductions and
malice ("bugs and fail-open, not malice"). Sitting 025 drew the hook's coverage
line: a model CLI is covered when the shell's own grammar makes it the command
word.

## R30F1: the coprocess NAME is recognised only before `{`

**What I observed.** At HEAD 6e906157 I called `command_words` and
`launch_reason` against this repository's `docs/agents.toml`.

| Bash command | Decision | Words read |
|---|---|---|
| `coproc CLAUDE while true; do echo ok; break; done` | deny | `['claude', 'echo', 'break', 'done']` |
| `coproc WORK while claude -p x; do :; done` | allow | `['work', ':', 'done']` |
| `coproc WORK if codex exec -; then :; fi` | allow | |
| `coproc WORK until claude -p x; do :; done` | allow | |
| `coproc WORK { claude -p x; }` | deny | |
| `coproc WORK for i in 1; do claude -p x; done` | deny | |
| `coproc WORK ( claude -p x )` | deny | |
| `coproc claude -p x` | deny | |
| `coproc while claude -p x; ...` | deny | |
| `coproc WORK { sleep 1; }` | allow | |
| `coproc sleep 1` | allow | |

In real Bash, a named coprocess runs its compound command's condition
(`coproc WORK while echo COND-RAN >&2; ...` printed COND-RAN). A coprocess
named `CLAUDE` runs no model: it gave `ok`. The cause is the round-9 table
entry `"coproc": (frozenset(), frozenset({"{"}))`
(`coordinator_guard.py:901`). It treats a NAME as metadata only before `{`,
while Bash's grammar is `coproc [NAME] compound-command` for any compound
opener. The finding holds as written.

**Scope and cost.** Named coprocesses are rare in agent commands, and one named
after a model CLI is close to contrived, as the builder concedes. On how
ordinary the form is alone, this would sit near R4F1's line. Two facts decide
it otherwise:
- **Grammar.** These are Bash grammar, not wrappers: the model CLI is the
  command word of the loop's or `if`'s condition list, the same reading the
  hook already gives to `while claude ...` and `if codex ...` outside a
  coprocess. So they fall inside sitting 025's line.
- **The lane's own change.** Round 9 itself taught the reader coproc's NAME
  shape, but only half of it. That added a false denial the baseline did not
  have (`coproc CLAUDE while true; ...`) and left the condition launch
  unread. The defect is an internal inconsistency in a table entry this lane
  just wrote, not a new kind of inspection.

The fix completes that one cell. coproc's NAME openers become every
compound-command opener the reader keeps in a segment (`{`, `while`, `until`,
`if`, `for`, `select`, `case`, `[[`, `((`), with three TC-339 pins: the
condition launches, and a model-named coprocess that runs no model. That costs
less than the inconsistency it removes. The builder's stated residual,
`coproc NAME ( … )` reading NAME because the reader splits at `(`, still
reads the body. It over-denies only a model-named subshell coprocess, and is
acceptable as recorded.

**For later rounds.** With this cell, the reader carries Bash's coprocess
grammar whole. A further grammar-only form that no ordinary agent writes, and
that this lane did not just introduce, is R4F1's class (sitting 005). It should
be dismissed there rather than opened as another round.

RULING: R30F1 FIX round 9's coproc entry treats a NAME as metadata only before `{`, while Bash takes `coproc [NAME]` before any compound command, so `coproc WORK while claude -p x; ...`, `... if codex exec -; ...` and `... until claude ...` run a model unread and `coproc CLAUDE while true; ...` is newly over-denied; completing that one table cell with the reader's compound-command openers removes both, inside sitting 025's command-word line
