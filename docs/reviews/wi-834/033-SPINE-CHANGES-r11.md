# WI-834 round 11: spine change list

Row text owed by round 11 (`033-PLAN-r11.md`, F1). No registry row was
edited; the coordinator applies these. LLR-320 needs no change: its
`module` is the template dev-setups, which round 11 leaves unchanged, and
its detail ("offers each missing setup item only at an interactive
terminal") already holds for this repository's Windows dev-setup now.

## TC-343, `evidence`

- **Current:** `tests/test_run_devsetup.py::test_the_check_for_run_offers_nothing_without_a_terminal; tests/test_run_devsetup.py::test_piped_menu_input_survives_the_check; tests/test_run_devsetup.py::test_a_bare_run_cmd_stops_with_the_step_when_the_runtime_stays_missing; tests/test_run_devsetup.py::test_at_a_terminal_each_missing_item_is_offered_consent_first; tests/test_run_devsetup.py::test_the_standalone_check_at_a_terminal_offers_and_writes_nothing; tests/test_run_devsetup.py::test_the_check_for_run_checks_only_the_interpreter_it_is_handed; tests/test_run_devsetup.py::test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu`
- **Proposed:** `tests/test_run_devsetup.py::test_the_check_for_run_offers_nothing_without_a_terminal; tests/test_run_devsetup.py::test_piped_menu_input_survives_the_check; tests/test_run_devsetup.py::test_a_bare_run_cmd_stops_with_the_step_when_the_runtime_stays_missing; tests/test_run_devsetup.py::test_at_a_terminal_each_missing_item_is_offered_consent_first; tests/test_run_devsetup.py::test_the_standalone_check_at_a_terminal_offers_and_writes_nothing; tests/test_run_devsetup.py::test_the_check_for_run_checks_only_the_interpreter_it_is_handed; tests/test_run_devsetup.py::test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu; tests/test_run_devsetup.py::test_at_a_windows_console_the_missing_runtime_is_offered_consent_first`
- **Why:** the new Windows pin drives the missing-runtime offer at a real
  console, decline and accept, for this repository's and the template's
  PowerShell readiness operations (round 032 F1).

## TC-343, `method` (optional)

- **Current:** `Run the readiness operation with interactive and non-interactive input, a missing runtime, and piped menu input; also run the standalone check. At a terminal, drive each missing-item offer through consent; drive standalone check at a terminal. Run the readiness operation with and without a handed interpreter while a Python 3.11+ interpreter is on PATH. Run it, and the standalone check, with a working runtime and no Git on PATH.`
- **Proposed:** `Run the readiness operation with interactive and non-interactive input, a missing runtime, and piped menu input; also run the standalone check. At a terminal, drive each missing-item offer through consent, on Windows in a real console for the missing-runtime offer of both PowerShell readiness operations; drive standalone check at a terminal. Run the readiness operation with and without a handed interpreter while a Python 3.11+ interpreter is on PATH. Run it, and the standalone check, with a working runtime and no Git on PATH.`
- **Why:** says where the Windows interactive coverage now runs. The current
  wording ("drive each missing-item offer through consent") already
  covers it, so this cell is optional, and leaving it saves a
  re-attestation.
