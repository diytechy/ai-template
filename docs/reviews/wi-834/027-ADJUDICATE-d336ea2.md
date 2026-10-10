# WI-834 checkpoint sitting 027 (d336ea2b)

## amendment

The three rows record the lane's answer to round 024 F2: a workstation without
Git must still get its readiness report and reach the menu. The fault was in
the PowerShell dev-setup. Under `ErrorActionPreference = "Stop"`, calling the
absent `git` threw before the runtime result. The fix (2ca10961) queries Git,
the pre-commit floor and its wiring only once `Have "git"` is true, in both
`dev-setup.template.ps1` and this repo's `scripts/dev-setup.ps1`.

What I observed at d336ea2b:
- `test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu`
  and `test_without_git_this_repos_check_and_run_still_work` ran on this
  Windows host and passed.
- The run/dev-setup, blackout, evidence-join and run-menu suites gave
  `151 passed, 5 skipped`. The skips are pseudo-terminal, POSIX-only and
  documented Windows-only cases.
- I also ran the POSIX template with no `git` on PATH, which no test covers.
  `--check` and `--for-run --python <3.11+>` each reported git `[missing]`,
  finished the report, and exited 0.

- [MEANING] LLR-320 Detail -> --for-run reports, offers at a terminal only, and exits on the handed interpreter -> also: it queries a workstation tool only once found present and reports an absent one missing, so an absent tool never ends the report before its runtime result -> a new robustness obligation that the PowerShell template failed before 2ca10961 (an absent git ended the report); blessed: both families now meet it, as observed above
- [MEANING] TC-342 Expected, Method -> verify the bare-run, direct and list forms, the handed interpreter, the floor and the candidate lists -> also verify that without Git a bare run still reaches its menu, by running a bare Windows launcher, on a scaffold and on this repo, with a runtime and no Git -> a new asserted case; blessed (both Git-less tests passed here)
- [MEANING] TC-343 Expected, Method -> verify the readiness operation's report, offers, exits and handed-interpreter rule -> also verify that without Git the operation reports git missing and still exits 0 with a runtime, and the standalone check exits 0 -> a new asserted case pinning LLR-320's new clause; blessed

VERDICT: MEANING rows=3

The act re-attests LLR-320, TC-342 and TC-343.

Observation, not a return: LLR-320 says the operation queries a workstation
tool "only once it is found present". The PowerShell template does exactly
that. The POSIX template still runs `git config --get core.hooksPath` without a
presence check. It meets the clause's stated outcome only through shell
semantics: a failed `$(…)` inside a `[ ]` test or an `if` condition, with
stderr discarded, does not end a `set -e` script. The observable obligation
holds (verified above), and no test covers the POSIX Git-less path. A later
pass may either guard the POSIX query the same way or word the clause by its
outcome alone. TC-343's Method names no shell family, while its evidence is
Windows-only.

SITTING: JUDGED kinds=amendment
