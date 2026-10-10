# WI-834 adjudication 005: dispute R4F1 (range 9bc1eb2a..705f8784)

Scope bound: PROCESS.md §6 "Review threat model". Review hunts defects in a
normal working environment: content agents write, supported configurations, and
regressions of supported behaviour. It excludes contrived reproductions, and it
names Forge mode's "bugs and fail-open, not malice" as the same bound.

## R4F1: Bash line continuation inside the here-document reader

**What I observed.** I called `kitlib/shell_line.segments` at 705f8784 with each
form. I also wrote each form, with `echo LAUNCHED<n>` in place of `claude -p x`,
to a file with LF endings and ran it in Git Bash on this host.

| Form | `segments` returns | Bash |
|---|---|---|
| `cat <<EOF⏎E\⏎OF⏎claude -p x` | `[['cat']]` | runs the command |
| `cat <<EOF⏎$\⏎(claude -p x)⏎EOF` | `[['cat']]` | runs the substitution |
| `cat <<E\⏎OF⏎$(claude -p x)⏎EOF` | `[['cat']]` | runs the substitution |
| `echo "$\⏎(claude -p x)"` (the builder's fourth site) | `[['echo', '$(claude -p x)']]` | runs the substitution |

The hook decides from these words (`coordinator_guard.command_words`, which
calls `shell_line.segments`). So all four are allowed inside an armed window.
The finding's facts hold, and the class reaches past the listed sites as the
builder says.

**What the reproduction needs.** I also probed the continuations an agent
actually writes. The lexer reads each one and the hook denies it:

- a continued argument list (`claude \⏎ -p x`);
- a continued `timeout` or `env` prefix;
- a continued pipe or `&&`;
- a continuation inside a `$( )`, in a double-quoted string or a here-document
  body;
- a body line continued before a substitution;
- a split `<<` and a split `&&`.

What stays open is narrower. A continuation fails open only when it splits a
multi-character token that the reader keys on: the `$(` opener, or a
here-document delimiter or delimiter word. No ordinary command needs `$` and
`(` on separate lines, or a delimiter broken across two lines. That input
exists only to get a launch past the hook. That is malice, which §6 puts out of
scope ("bugs and fail-open, not malice"); it is not a fail-open on content an
agent normally writes.

The spec's own coverage confirms this reading:

- The hook "is supervision within that coverage, not inspection of arbitrary
  shell programs".
- Script wrappers are not inspected. The round-2 plan records `bash -c '...'`,
  `eval '...'` and `pwsh -Command` as allowed by design.
- Ruling (f) makes the coordinator's stop encouraged, not enforced.

An agent set on evading the hook already has easier ways out, and the spec
accepts them. The fault is in this lane's own new lexer, so it is not a
regression of supported behaviour.

Per §6, this is dismissed in one recorded line and is not answered with code.
If the coordinator wants this class closed for later rounds, it should be done
at the lane's spine checkpoint, outside this ruling. The hook's coverage
statement could name continuations that split a token beside the uninspected
script wrappers.

RULING: R4F1 DISMISS out-of-scope a continuation fails open only when it splits a multi-character token (`$(`, a here-document delimiter or delimiter word), which no ordinary command does, so reproducing it needs deliberate evasion of the hook, the malice PROCESS §6 excludes; every natural continuation probed is read and denied, and the spec's supervision-not-inspection coverage already leaves `bash -c`/`eval` open
