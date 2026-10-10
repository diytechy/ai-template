# WI-834 round 5: spine change list (answers 016 F1 and F2)

The builder changed no registry row's text. These are the row-text changes
round 5's build makes owed, for the spine author to reconcile at the lane's
checkpoint. F1 is built as sitting 017 ruled it (D-020), F2 as the owner ruled
it (D-019); the builder's construction choices are D-021. The trace cells the
builder touched are listed at the end.

## LLR-300, `detail` (F1): one clause added, optional

- **Current, the reading sentence:** "One quote-aware shell reading per
  dialect reads quoted assignments and env split strings as the shell does,
  treats quoted separators as data, reads substitutions in unquoted
  here-document and double-quoted PowerShell here-string bodies, and keeps
  quoted bodies as data; window_check exits nonzero inside it."
- **Proposed:** "One quote-aware shell reading per dialect reads quoted
  assignments and env split strings as the shell does, reads a PowerShell
  assignment's right-hand command as a command word while a quoted or
  variable right-hand value stays data, treats quoted separators as data,
  reads substitutions in unquoted here-document and double-quoted PowerShell
  here-string bodies, and keeps quoted bodies as data; window_check exits
  nonzero inside it."
- **Why:** 016 F1, ruled FIX by sitting 017. The sitting found the row's
  "model-CLI command word" already covers the case, so the change is optional
  clarity and needs re-attestation only if adopted.

## LLR-301, `detail` (F2, D-019)

- **Current, the launcher sentence:** "Each launcher enters the declared
  root, exports the token as PT_COORDINATOR_TAKE for the successor's
  SessionStart take, and starts claude with the prompt as one argument: the
  POSIX one in a new terminal, the Windows one through exec_claude, which
  invokes claude with the extracted prompt."
- **Proposed:** "Each launcher enters the declared root, runs the guard's
  steps on one interpreter it resolves by running each candidate and taking
  the first that reports Python 3.11 or later (exiting nonzero with the step
  when none does), exports the token as PT_COORDINATOR_TAKE for the
  successor's SessionStart take, and starts claude with the prompt as one
  argument: the POSIX one in a new terminal, the Windows one through
  exec_claude, which invokes claude with the extracted prompt."
- **Why:** 016 F2 class, site (d). A bare `python` / `python3` let an older
  interpreter crash `window-check`, so every relaunch failed.

## LLR-322, `detail` (F2, D-019)

- **Current:** "When the shipped coordinator-hook example declares guard hooks
  and the current settings leave them off, an interactive consent may enable
  them by merging the guard hooks into the settings while preserving existing
  hooks and unrelated settings. A declined offer changes neither
  configuration nor credentials, and an example with no guard hooks creates
  no settings change."
- **Proposed:** "When the shipped coordinator-hook example declares guard hooks
  and the machine-local settings leave them off, an interactive consent may
  enable them by merging the guard hooks into the machine-local settings,
  each command bound to the floor-resolved interpreter that runs the opt-in,
  while preserving existing hooks and unrelated settings; the committed
  project settings are never written, and a re-run is idempotent. A declined
  offer changes neither configuration nor credentials, and an example with no
  guard hooks creates no settings change."
- **Why:** 016 F2: a bare `python` hook crashed on tomllib under an older
  first-on-PATH interpreter and so denied nothing. The owner ruled binding at
  opt-in, machine-local (D-019, superseding D-001's target file).

## IF-280, `data` (F2): optional

- **Current:** "take | request-relaunch --handoff | handback --handoff |
  release --reason | clear --reason | status | window-check | hooks --example E
  [--enable]"
- **Proposed:** no change to the argument list. The owner header's
  `Contract IF-280:` body (coordinator_guard.py) now says `hooks` reads and
  writes the machine-local `.claude/settings.local.json`, each hook bound to
  the interpreter the command runs on. The spine author decides whether the
  row's data should name the file.

## TC-339, `method` and `expected` (F1)

- **Current method, its second sentence:** "Exercise quote-aware shell
  reading, expandable and literal here bodies, and unreadable-line denial."
- **Proposed:** "Exercise quote-aware shell reading, PowerShell assignments
  with command, quoted and variable right-hand sides, expandable and literal
  here bodies, and unreadable-line denial."
- **Current expected, its second sentence:** "Quote-aware words and
  expandable bodies that launch a model are denied; quoted bodies are
  allowed; unreadable shell input is denied."
- **Proposed:** "Quote-aware words, PowerShell assignments whose right-hand
  side runs a model, and expandable bodies that launch a model are denied;
  quoted bodies and quoted or variable right-hand values are allowed;
  unreadable shell input is denied."

## TC-340, `expected` (F2, site f)

- **Current:** "No request is written during blackout and an existing request
  is cancelled at holder exit."
- **Proposed:** append "; the guard command the instructions name runs on the
  hook's own interpreter."

## TC-345, `method` and `expected` (F2)

- **Current method:** "Decline and accept the interactive coordinator-hook
  offer with existing settings, and run the hook command against examples
  with and without guard hooks."
- **Proposed method:** append "Run an installed hook with a real Python below
  the floor first on PATH, where one is installed, and check the scaffold's
  git ignore list."
- **Current expected:** "Consent enables the coordinator hooks by preserving
  existing settings and hooks; denial changes no configuration or credential;
  and an example without guard hooks changes nothing."
- **Proposed expected:** "Consent enables the coordinator hooks in the
  machine-local settings, bound to the opt-in's interpreter, by preserving
  existing settings and hooks and never writing the committed project
  settings; a re-run changes nothing; an installed hook still denies with an
  older Python first on PATH; the machine-local file is git-ignored; denial
  changes no configuration or credential; and an example without guard hooks
  changes nothing."

## Trace cells the builder updated (not row text)

- LLR-300 `code_symbol`: `command_words/_assigned` (the new tagged function in
  coordinator_guard.py) and `segments/Unreadable/Word` (the new tagged class
  in kitlib/shell_line.py).
- TC-340 `evidence`: appended
  `tests/test_run_devsetup.py::test_the_injected_guard_command_names_the_hooks_own_interpreter`.
- TC-345 `evidence`: appended
  `tests/test_run_devsetup.py::test_an_installed_hook_denies_with_an_older_python_first;
  tests/test_run_devsetup.py::test_a_scaffold_keeps_the_machine_local_settings_out_of_git`.
- TC-339 and TC-342 `evidence`: unchanged names. F1's cases joined the
  existing QUOTED_DENIED / QUOTED_ALLOWED tests, and the relaunch pairs
  joined the existing parity test.
