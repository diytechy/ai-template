# WI-834 checkpoint sitting 023 (99601ff5)

## amendment

The six rows record the lane's answers to rounds 016 to 020:
- the PowerShell assignment reading (dispute 017's FIX for R16F1);
- the guard's interpreter, bound for the hooks, the relaunch launchers and the
  injected instructions (round 016 F2);
- the hook opt-in, which now writes machine-local settings and owns only the
  guard's own commands (round 018 F2, round 020 O2).

What I observed at 99601ff5:
- **Code against the text:** I read the diff since 520a4cdc in
  `coordinator_guard.py`, `kitlib/guard_hooks.py`, `kitlib/shell_line.py`,
  `scripts/coordinator-relaunch.{sh,cmd}`, both dev-setup templates and
  `gitignore.template`.
- **Test suites:** the blackout, run/dev-setup, guard, guard-e2e and
  evidence-join suites gave `214 passed, 4 skipped`. The skips are three
  pseudo-terminal cases and one POSIX-only case.
- **The older-Python test ran for real:** this host has a Python below 3.11,
  and the installed hook still denied with it first on PATH. The scaffold
  git-ignore test, the bound GUARD test and the merge tests also passed.
- **A probe of 23 PowerShell forms against `launch_reason`** matched the new
  LLR-300 text with no mismatch:
  - denied: the plain, property, index, typed, array-typed, scoped,
    environment, comma-list and chained assignments, `+=` and `??=`, and an
    operator written against a word;
  - allowed: quoted and variable right-hand values, a quoted `=` inside an
    index, comparisons, and a non-model command.

- [MEANING] LLR-322 Detail -> consent merges the guard's hook groups into the project settings, keeping existing hooks -> consent merges into the machine-local `.claude/settings.local.json` only, each command bound to the floor-resolved interpreter running the opt-in; the guard owns only commands of the example's exact shape (its interpreter word, or a bound absolute path, then the guard script and subcommand), so other commands, even ones naming the guard file, keep their group and configuration, and a group drops only when it empties; the committed settings are never written; re-runs are idempotent -> a different target file, an interpreter binding, and a new ownership rule; blessed: `kitlib/guard_hooks.py` (`bind`, `_owns`, `merged`) and `enable_hooks` match it word for word, and machine-local is right for a file that names this machine's interpreter
- [MEANING] TC-345 Expected, Method -> verify consent enables the hooks keeping existing ones, a decline changes nothing, and a guard-less example changes nothing -> also verify the machine-local target and binding, command-level ownership (a user command in a guard group, one naming the guard file, keeps its place and matcher; an older bare-`python` guard command is replaced), an idempotent re-run, an installed hook denying with an older Python first on PATH, and the file being git-ignored -> new asserted cases; blessed (`test_an_installed_hook_denies_with_an_older_python_first` ran with a real sub-floor Python here; the git-ignore and merge tests passed)
- [MEANING] LLR-300 Detail -> the quote-aware reading treats a PowerShell assignment's target as the command word -> a PowerShell assignment, recognised by an unquoted operator wherever it stands, runs its right-hand command whatever its target; quoted or variable right-hand values stay data; a chained assignment runs its final command -> a new denial class (dispute 017's FIX); blessed: the 23-form probe matches it exactly. "whatever its target" fits the code's leading-`$`-or-`[` test, because every PowerShell assignment target opens with one
- [MEANING] TC-339 Expected, Method -> verify quote-aware words, expandable bodies and unreadable lines -> also verify PowerShell assignments of every target form, spaced or written against a word that holds a quoted piece, with command, quoted and variable right-hand sides -> new asserted cases pinning LLR-300's reading; blessed
- [MEANING] LLR-301 Detail -> each relaunch launcher enters the root and starts claude -> it first resolves one interpreter by RUNNING its .venv candidate(s), then its dev-setup's runtime search, taking the first that reports 3.11+ with its own path; it exits nonzero with guidance when none resolves, and runs window_check on that interpreter -> a new resolution step and a new failure exit; blessed: `coordinator-relaunch.sh` and `.cmd` match it, and their lists equal this repo's `scripts/dev-setup.{sh,ps1}` searches, pinned by `test_each_run_launcher_searches_what_its_dev_setup_searches` (POSIX has two .venv entries where the text says "candidate", a wording nicety that changes no obligation)
- [MEANING] TC-340 Expected -> verify no request inside the window and a cancellation at the holder's exit -> also verify the guard command in injected instructions runs on the hook's own interpreter -> a new asserted case; blessed (`test_the_injected_guard_command_names_the_hooks_own_interpreter` asserts that `GUARD` opens with `sys.executable`)

VERDICT: MEANING rows=6

The act re-attests LLR-300, LLR-301, LLR-322, TC-339, TC-340 and TC-345.

Observation, not a return: LLR-301's new resolution clause is verified by a
test cited under TC-342, whose relaunch-script cases compare the candidate
lists. Neither LLR-301's own TC-318 nor TC-340 cites it. A later spine pass may
add that test to TC-318's evidence, so the arm is reachable from its own row.

SITTING: JUDGED kinds=amendment
