# WI-834 adjudication 040: dispute R39F1 (range ed2533cb..b4f50470)

Scope bound: PROCESS.md §6 "Review threat model". Review covers a normal
working environment: content agents write, supported configurations, and
regressions of supported behaviour. It excludes contrived reproductions and
malice. Sitting 025 set the coverage line: a model CLI is covered when the
shell's grammar makes it the command word *this line runs*. Script bodies and
wrappers that take a command as an argument are outside it.

## R39F1: a PowerShell function definition is read as a launch

**What I observed.** At HEAD 73e78ae0 I called `command_words` and
`launch_reason` against this repository's `docs/agents.toml`.

| Command | Decision | Words read |
|---|---|---|
| PowerShell `function Invoke-Review { codex exec --model m - }` | deny | `['function', 'codex']` |
| PowerShell `function Invoke-Review { echo ok }` | allow | |
| PowerShell `function Invoke-Review { codex exec - }; Invoke-Review` | deny | |
| PowerShell `& { claude -p x }` | deny | |
| PowerShell `1..2 \| ForEach-Object { codex exec - }` | deny | |
| PowerShell `if ($x) { claude -p x }` | deny | |

In real PowerShell, `function Invoke-Review { cmd /c echo BODY-RAN }` defined
the function without running its body. The finding holds: the definition runs
nothing and is denied.

The cause is the round-1 reading (D-011). PowerShell's `{`/`}` are segment
boundaries, so a brace body reads as a statement. That same reading is what
correctly catches the executing blocks in the table: `& { … }`,
`ForEach-Object { … }` and `if (…) { … }`.

**Weighing it.** The defect is real and in scope, since helper functions are
ordinary PowerShell. But its cost/benefit is lopsided:
- **It fails closed.** Only inside an armed window, and only for a function
  whose body names a model CLI, does the session get told to wait until the
  window ends. Defining a model-wrapping helper during the one interval meant
  to pause model work buys almost nothing. The function can be defined after
  the window, and so can the call it would serve.
- **The fix touches the boundary that makes executing blocks read correctly.**
  Telling a deferred body (`function`/`filter` definitions) from an executing
  block (call operator, script-block arguments, `if`/`foreach`/`while` bodies,
  `try`) needs brace-depth tracking plus a classification of what each `{`
  belongs to. That is about 20 lines by the builder's estimate, in the reader
  this lane has re-opened round after round. A misclassification there would
  turn today's correct denials into silent launches, the fail-open this hook
  exists to prevent.
- **The fix trades a closed false denial for an open miss.** The define-and-call
  line `function X { codex … }; X` runs a model and is denied today. Under a
  bodies-as-data reading it would read only `X`. By sitting 025's line that
  form is a script body run through a wrapper name, outside coverage, but the
  fix would still give up a denial the hook gets right today to remove a
  denial it gets wrong.

A fail-closed over-denial of a rare, low-value action is cheaper to keep than
the change and its risk.

**Observation, outside this finding (not ruled).** The Bash reading is
inconsistent in the same area:
- `function f { claude -p x; }` is allowed, as the lane's own regression
  (`tests/test_blackout_window.py:552`) pins;
- `f() { claude -p x; }` is denied: the same class of fail-closed definition
  over-denial ruled on here;
- `function f { claude -p x; }; f` is allowed, though it runs claude. By
  sitting 025's line that is a script body behind a wrapper name, outside the
  declared coverage, so it is not a coverage defect.

If the owner later wants function bodies inspected or exempted consistently,
that is a coverage decision for both dialects together, not a per-round reader
patch.

RULING: R39F1 DISMISS not-worth-cost the over-denial is real but fails closed, only inside an armed window and only for a definition whose body names a model CLI, while the fix (brace-depth tracking to tell deferred function bodies from the executing blocks the same reading correctly denies) risks fail-open misreads at the hook's trust boundary and would give up today's denial of the define-and-call form, so it costs more than the rare deferral it removes
