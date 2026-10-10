# WI-834 checkpoint sitting 015 (113d75c1)

## amendment

The four rows describe one design change, which answers review 012 F1. The run
launcher now resolves a single interpreter that meets the 3.11 floor. It hands
that interpreter to dev-setup's readiness check, and the menu runs on it. The
check no longer searches for a runtime of its own.

What I observed:
- I read `run.template.sh`, `run.template.cmd`, `dev-setup.template.sh` and
  `dev-setup.template.ps1`, plus their diff since 6edd9a38. Each matches the
  new LLR text.
- `tests/test_run_devsetup.py`, `tests/test_evidence_join.py` and
  `tests/test_run_menu.py` gave `68 passed, 5 skipped`. The skips are three
  pseudo-terminal cases, one POSIX-only case and one documented Windows-only
  limit.
- The four new tests the TCs cite all ran on this host and passed: the handed
  interpreter (run.sh, run.command, run.cmd), no menu below the floor (both
  launcher families, all three forms), the launcher and dev-setup searching the
  same candidate list (templates and this repo), and the check using only the
  handed interpreter (sh and ps1).

- [MEANING] LLR-320 Detail -> --for-run finds a runtime itself and exits 0 when one is ready after the offers -> --for-run uses only the interpreter the launcher hands it and never searches; it exits 0 only when that interpreter meets the floor, and exits 1 when none is handed even with a 3.11+ interpreter on PATH -> the runtime's source changed, and so did an exit condition: an implementation that searched PATH would now fail, and a runtime installed during the offers no longer turns the result to 0, which ends in a "run again"; blessed: it is the only way to guarantee that the floor checked is the floor the menu runs on (an interpreter installed mid-run is not the launcher's resolved one, and a fresh install is often not on the running shell's PATH anyway); SR-046's "if the runtime remains missing" reads as no runtime the launcher can run on, and the guidance says to run again
- [MEANING] TC-342 Expected, Method -> verify the bare run checks once and stops on a missing runtime, and the direct and list forms neither check nor pause -> also verify the check is handed the menu's own interpreter, no form starts the menu without a 3.11+ interpreter (only sub-floor ones first on PATH), and each launcher's candidates equal its dev-setup's search, in order -> three new asserted cases; blessed (cited by `test_a_bare_run_hands_the_check_the_interpreter_its_menu_runs_on`, `test_no_form_of_run_starts_the_menu_below_the_floor` and `test_each_run_launcher_searches_what_its_dev_setup_searches`, all observed passing)
- [MEANING] TC-343 Expected, Method -> verify the readiness operation's report, offers, exits and the read-only check -> also verify that with no handed interpreter it reports the runtime missing and exits 1 even with 3.11+ on PATH, and that a handed floor-satisfying one exits 0 -> a new asserted case pinning LLR-320's no-search rule; blessed (`test_the_check_for_run_checks_only_the_interpreter_it_is_handed`, sh and ps1, observed passing)
- [MEANING] LLR-047 Detail -> the no-argument launchers run the readiness step before the menu; the direct and list forms bypass it -> every form resolves one interpreter by running its .venv candidates, then dev-setup's own candidates, taking the first that reports 3.11+ as its executable path, and runs the menu on exactly that path; the bare form hands it to the check; the direct and list forms exit 1 with guidance when none resolves -> a new resolution rule and a new exit case for the direct and list forms; blessed (it matches both launcher templates; probing by running rather than by existence, and sharing dev-setup's list, are what TC-342's new cases pin)

VERDICT: MEANING rows=4

The act re-attests LLR-047, LLR-320, TC-342 and TC-343.

SITTING: JUDGED kinds=amendment
