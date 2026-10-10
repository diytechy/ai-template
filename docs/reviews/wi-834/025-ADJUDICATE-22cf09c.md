# WI-834 adjudication 025: dispute R24F1 (range ed2533cb..5d0a27eb)

Scope bound: PROCESS.md §6 "Review threat model". Review covers a normal
working environment: content agents write, supported configurations, and
regressions of supported behaviour. It excludes contrived reproductions and
malice ("bugs and fail-open, not malice").

## R24F1: PowerShell's dot invocation hides the command from the blackout hook

**What I observed.** At HEAD 22cf09c9 I called `coordinator_guard.launch_reason`
against this repository's `docs/agents.toml`.

| PowerShell command | Decision | Segments |
|---|---|---|
| `claude -p x` | deny | |
| `& claude -p x` | deny | |
| `& 'claude' -p x` | deny | |
| `$r = & claude -p x` | deny | |
| `. claude -p x` | allow | `[['.', 'claude', '-p', 'x']]` |
| `. 'claude' -p x` | allow | |
| `$r = . claude -p x` | allow | |

The reader splits on `&` as an operator. `.` stays a word, and
`_segment_command` takes it as the executable. In a real PowerShell session,
`. cmd /c echo DOT-RAN`, `$r = . cmd /c echo DOT-CAPTURED` and
`. 'cmd' /c echo ...` each ran the native command, and the second captured its
output. The finding holds as written.

**Where the line falls.** This class has now come back once per round, so the
ruling states the line it draws as well as the form it rules on. The approved
coverage (Part B Done-when, LLR-300, IF-275) is a model CLI "as any command
word", after the declared `timeout`, `env` and `VAR=value` prefixes and across
the declared chain operators. "Script wrappers are not inspected", and "the
hook is supervision within that coverage, not inspection of arbitrary shell
programs". The test is therefore which word the shell's own grammar makes the
command.

- **Inside the coverage: invocation operators.** In PowerShell's grammar, `&`
  and `.` are invocation operators, not commands. In `. claude -p x` the
  command element is `claude`, exactly as in `& claude -p x`, which is already
  denied. Treating `.` as the command is a misreading of the line, not a
  wrapper the hook declines to inspect.
- **Outside the coverage: commands that take a command as an argument.**
  `Start-Process claude`, `iex '…'`, `cmd /c claude`, `sh -c '…'`, Bash
  `exec`, `command`, `builtin`, `nohup` and `xargs`, and every script file. In
  each of these, the shell's command word is the wrapper and the model CLI is
  its argument. The approved text excludes them, beside the two prefixes it
  names (`timeout`, `env`), and the guard's `window-check` exists for
  launchers that wrap a model. Expanding that list would mean inspecting
  wrappers, an owner-level change to the coverage, not a defect against it.
  Findings against wrapper forms should be dismissed by this ruling's line, not
  reopened round by round.

**Scope and cost.** `. claude` is rarer than R16F1's `$r = claude`, as the
builder concedes. But it bends no grammar: it is not R4F1's token split. It is
a documented invocation form whose command word is the model CLI, so it falls
inside the declared coverage, and the reader already honours its sibling `&`.
The fix stays in the PowerShell branch of the one reading boundary: a leading
unquoted `.` is an invocation operator, so the next word is the command, with
the same quoting rules `&` gets. A quoted `'.'` stays data. That is about 5
lines plus the four TC-339 cases (direct, quoted name, captured, and a
dot-sourced script that stays allowed). The approved row text already covers
it ("any command word"), so no re-attestation is owed unless the TC-339 wording
changes.

RULING: R24F1 FIX the PowerShell reader takes the dot invocation operator as the command word, so `. claude -p x`, `. 'claude' -p x` and `$r = . claude -p x` run a model through the armed blackout hook while their `&` siblings are denied; `.` is grammar like `&`, leaving `claude` the command word inside the declared any-command-word coverage, and wrapper commands that take a command as an argument (Start-Process, iex, cmd /c, sh -c, exec, command, builtin, nohup, xargs) stay outside it as the approved text already says
