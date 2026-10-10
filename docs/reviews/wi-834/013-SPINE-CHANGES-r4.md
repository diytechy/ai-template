# WI-834 round 4: spine change list (answers 012 F1)

The builder changed no registry row's text. These are the row-text changes
round 4's fix (D-017: one interpreter, resolved by the run launcher and handed
to the readiness operation) makes owed, for the spine author to reconcile at
the lane's checkpoint. The only cells the builder touched are trace cells:
TC-342's and TC-343's `evidence` (listed at the end).

## LLR-047, `detail`

- **Current (the launcher sentences, after the run_menu description):** "The
  no-argument run launchers change to the repository root and invoke
  dev-setup's --for-run/-ForRun readiness operation once before the menu; a
  nonzero result prints guidance and leaves the menu unopened. Direct and
  --list forms bypass that operation and, on Windows, the closing pause;
  run.command delegates to run.sh so it does not duplicate the operation, and
  non-interactive menu input remains available after it."
- **Proposed:** "Every run launcher form resolves one interpreter by running
  each candidate (the repository's virtual-environment interpreter, then the
  same ordered list dev-setup's own runtime search uses) and taking the first
  that reports Python 3.11 or later, as that interpreter's own executable
  path, and runs the menu on exactly it. The
  no-argument launchers change to the repository root and invoke dev-setup's
  --for-run/-ForRun readiness operation once before the menu, handing it that
  interpreter (none when none resolved); a nonzero result prints guidance and
  leaves the menu unopened. Direct and --list forms bypass that operation and,
  on Windows, the closing pause, and exit 1 with guidance when no interpreter
  resolved; run.command delegates to run.sh so it does not duplicate the
  operation, and non-interactive menu input remains available after it."
- **Why:** 012 F1. The launcher's existence/runnability-only choice is
  replaced by one floor-probed resolution that both the readiness step and the
  menu consume; the direct and list forms no longer start the menu on a
  sub-floor interpreter. The coordinator's follow-up (same class) added the
  candidate-list clause: a launcher searching fewer interpreters than its
  dev-setup let the standalone check report a runtime that run then refused.
  The run_menu sentences and the rationale stay.

## LLR-320, `detail`

- **Current:** "The --for-run/-ForRun operation reports workstation readiness
  first, then offers each missing setup item only at an interactive terminal;
  without one it offers nothing and does not consume menu input. It exits 0
  when the runtime is ready after the offers and otherwise exits 1 with the
  step to take. The standalone --check/-Check operation reports only, performs
  no offer or write, and exits 0."
- **Proposed:** "The --for-run/-ForRun operation reports workstation readiness
  first, then offers each missing setup item only at an interactive terminal;
  without one it offers nothing and does not consume menu input. Its runtime
  is the interpreter the launcher hands it, never one it searches for: it
  exits 0 when that interpreter satisfies the runtime floor and otherwise,
  including when none is handed, exits 1 with the step to take. The
  standalone --check/-Check operation reports only, performs no offer or
  write, and exits 0."
- **Why:** 012 F1. "Ready after the offers" was answered by the readiness
  step's own interpreter search, so its exit 0 could speak for an interpreter
  the menu never runs. An interpreter installed by an offer is not the one the
  launcher resolved, so it counts from the next run (D-017).
- `code_symbol` (`detect_runtime/interactive/maybe_install;FindPython/Interactive/MaybeInstall`)
  is unchanged: the handed-interpreter branch lives inside `detect_runtime` and
  `FindPython`.

## IF-292, `data`

- **Current:** "bare run invokes --for-run/-ForRun once from the repository
  root before its menu"
- **Proposed:** "bare run invokes --for-run/-ForRun once from the repository
  root before its menu, passing as --python/-Python the interpreter it
  resolved for the menu (omitted when none resolved)"
- **Why:** the invocation now carries the resolved interpreter; the owner
  headers (`dev-setup.template.sh` / `.ps1`, `# Contract IF-292:`) already say
  so. The spine author decides whether this is `version = "v2"` (the row is
  Drafted, never approved).

## IF-293, `data`

- **Current:** "0 runtime ready; nonzero after setup guidance leaves the
  bare-run menu unopened"
- **Proposed:** "0 the handed interpreter satisfies the runtime floor; nonzero
  (none handed included) after setup guidance leaves the bare-run menu
  unopened"
- **Why:** the result now speaks for the interpreter the menu runs on; the
  owner headers' `# Contract IF-293:` bodies say so.

## TC-342, `method` and `expected`

- **Current method:** "Run bare, direct and list launchers against a scaffold
  and the repository with varied readiness results."
- **Proposed method:** "Run bare, direct and list launchers against a scaffold
  and the repository with varied readiness results, observing the interpreter
  handed to the readiness step and the one the menu runs on, and with only
  sub-floor interpreters first on PATH; compare each launcher's candidate
  list with its dev-setup's runtime search."
- **Current expected:** "A bare run checks once before its menu and stops on a
  missing runtime; direct and list forms do not check or pause."
- **Proposed expected:** "A bare run checks once before its menu, handing the
  check the interpreter the menu then runs on, and stops on a missing runtime;
  direct and list forms do not check or pause; with no 3.11+ interpreter no
  form starts the menu; each launcher searches the same interpreters, in the
  same order, as its dev-setup."
- **Why:** the two new pins (evidence below) verify the one-interpreter
  relationship and the sub-floor refusal.

## TC-343, `method` and `expected`

- **Current method:** "Run the readiness operation with interactive and
  non-interactive input, a missing runtime, and piped menu input; also run the
  standalone check. At a terminal, drive each missing-item offer through
  consent; drive standalone check at a terminal."
- **Proposed method:** append "Run it with and without a handed interpreter
  while a 3.11+ is on PATH."
- **Current expected:** "The operation reports before offering, offers nothing
  without a terminal, preserves piped menu input, and exits with guidance when
  the runtime remains missing; standalone check is read-only and exits 0. At a
  terminal each missing item is offered consent-first, while standalone check
  offers and writes nothing."
- **Proposed expected:** append "Without a handed interpreter it reports the
  runtime missing and exits 1 although one is installed; with one that
  satisfies the floor it exits 0."

## SR-046 and SR-032: no change

SR-046's acceptance ("A no-argument launch runs its readiness step once from
the repository root before the menu and, if the runtime remains missing, exits
with guidance; a direct or discovery launch skips that step and any closing
pause") stays true and capability-level; the reviewer asked to retain it. The
interpreter resolution is an LLR-047 decision (R2: no concrete carrier at SR).
SR-032 is unchanged.

## Trace cells the builder updated (not row text)

- TC-342 `evidence`: appended
  `tests/test_run_devsetup.py::test_a_bare_run_hands_the_check_the_interpreter_its_menu_runs_on;
  tests/test_run_devsetup.py::test_no_form_of_run_starts_the_menu_below_the_floor;
  tests/test_run_devsetup.py::test_each_run_launcher_searches_what_its_dev_setup_searches`.
- TC-343 `evidence`: appended
  `tests/test_run_devsetup.py::test_the_check_for_run_checks_only_the_interpreter_it_is_handed`.
