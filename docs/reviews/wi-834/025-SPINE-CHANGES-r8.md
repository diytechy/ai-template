# WI-834 round 8: spine change list (answers round 024 F1, F2)

The builder changed no registry row's text. F1 is built as sitting 025 ruled
it (D-024), and F2 per the plan's owning boundary. The trace cells the builder
touched are listed at the end.

## TC-339: no change

F1's three denied forms and the allowed dot-sourced script joined TC-339's
existing QUOTED_DENIED / QUOTED_ALLOWED tests. Sitting 025 found the dot
inside the declared "any command word" coverage, and the reconciled TC-339
text already says "declared main-session launch forms" and "quote-aware
words", so its wording need not change.

## LLR-300: no change

As for TC-339: "a Bash/PowerShell model-CLI command word" already covers the
word after the dot, as sitting 025 ruled. The new tagged `_invoked` is a
`code_symbol` trace cell only (below).

## LLR-320, `detail` (F2)

- **Current, its first sentence:** "The --for-run/-ForRun operation reports
  workstation readiness first, then offers each missing setup item only at an
  interactive terminal; without one it offers nothing and does not consume
  menu input."
- **Proposed:** "The --for-run/-ForRun operation reports workstation
  readiness first, querying a workstation tool only once it is found present
  and reporting an absent one as missing, so an absent tool never ends the
  report before its runtime result; it then offers each missing setup item
  only at an interactive terminal, and without one it offers nothing and does
  not consume menu input."
- **Why:** 024 F2. Without Git, the PowerShell report threw at its
  `git config` query and exited 1 before its runtime result, so a bare run
  reported a missing runtime and the standalone check broke its exit-0
  contract.

## TC-342, `method` and `expected` (F2)

- **Current method:** "Run bare, direct and list launchers against a scaffold
  and the repository with varied readiness results, observing the interpreter
  handed to the readiness step and the one the menu runs on, and with only
  sub-floor interpreters first on PATH; compare each launcher's candidate list
  with its dev-setup's runtime search."
- **Proposed method:** append "Run a bare Windows launcher on a scaffold and
  on the repository with a working runtime and no Git on PATH."
- **Current expected:** "A bare run checks once before its menu, handing the
  check the interpreter the menu then runs on, and stops on a missing
  runtime; direct and list forms do not check or pause; with no Python 3.11+
  interpreter no form starts the menu; each launcher searches the same
  interpreters, in the same order, as its dev-setup."
- **Proposed expected:** append "; without Git a bare run still reaches its
  menu."

## TC-343, `method` and `expected` (F2)

- **Current method:** "… Run the readiness operation with and without a
  handed interpreter while a Python 3.11+ interpreter is on PATH."
- **Proposed method:** append "Run it, and the standalone check, with a
  working runtime and no Git on PATH."
- **Current expected:** "… with one that satisfies the floor it exits 0."
- **Proposed expected:** append "Without Git, the operation reports git
  missing and still exits 0 with a runtime, and the standalone check exits 0."

## Trace cells the builder updated (not row text)

- LLR-300 `code_symbol`: `…/command_words/_assigned/…` became
  `…/command_words/_assigned/_invoked/…` (the new tagged function).
- TC-342 `evidence`: appended
  `tests/test_run_devsetup.py::test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu;
  tests/test_run_devsetup.py::test_without_git_this_repos_check_and_run_still_work`.
- TC-343 `evidence`: appended
  `tests/test_run_devsetup.py::test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu`.
